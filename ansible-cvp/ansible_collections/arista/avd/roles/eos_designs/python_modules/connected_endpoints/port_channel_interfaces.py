from __future__ import annotations

import re
from collections import ChainMap
from functools import cached_property

from ansible_collections.arista.avd.plugins.filter.esi_management import generate_esi, generate_lacp_id, generate_route_target
from ansible_collections.arista.avd.plugins.filter.range_expand import range_expand
from ansible_collections.arista.avd.plugins.plugin_utils.strip_empties import strip_null_from_data
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get

from .utils import UtilsMixin


class PortChannelInterfacesMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def port_channel_interfaces(self) -> dict | None:
        """
        Return structured config for ethernet_interfaces
        """
        port_channel_interfaces = {}
        for connected_endpoint in self._filtered_connected_endpoints:
            for adapter in connected_endpoint["adapters"]:
                if get(adapter, "port_channel.mode") is None:
                    continue

                default_channel_group_id = int("".join(re.findall(r"\d", adapter["switch_ports"][0])))
                channel_group_id = get(adapter, "port_channel.channel_id", default=default_channel_group_id)

                port_channel_interface_name = f"Port-Channel{channel_group_id}"
                port_channel_interfaces[port_channel_interface_name] = self._get_port_channel_interface_cfg(adapter, channel_group_id, connected_endpoint)
                if (subinterfaces := get(adapter, "port_channel.subinterfaces")) is None:
                    continue

                for subinterface in subinterfaces:
                    if "number" not in subinterface:
                        continue

                    port_channel_subinterface_name = f"Port-Channel{channel_group_id}.{subinterface['number']}"
                    port_channel_interfaces[port_channel_subinterface_name] = self._get_port_channel_subinterface_cfg(subinterface, adapter, channel_group_id)

        for network_port in self._filtered_network_ports:
            if get(network_port, "port_channel.mode") is None:
                continue

            connected_endpoint = {
                "name": network_port.get("description"),
                "type": "network_port",
            }
            for ethernet_interface_name in range_expand(network_port["switch_ports"]):
                # Override switches and switch_ports to only render for a single interface
                # The blank extra switch is only inserted to work around port_channel validations
                # This also means that port-channels defined with network_ports data model will be single-port per switch.
                # Caveat: "short_esi: auto" and "designated_forwarder_algorithm: auto" will not work correctly.
                tmp_network_port = ChainMap(
                    {
                        "switch_ports": [ethernet_interface_name, ""],
                        "switches": [self._hostname, ""],
                    },
                    network_port,
                )

                default_channel_group_id = int("".join(re.findall(r"\d", ethernet_interface_name)))
                channel_group_id = get(tmp_network_port, "port_channel.channel_id", default=default_channel_group_id)

                port_channel_interface_name = f"Port-Channel{channel_group_id}"
                port_channel_interfaces[port_channel_interface_name] = self._get_port_channel_interface_cfg(
                    tmp_network_port, channel_group_id, connected_endpoint
                )

        if port_channel_interfaces:
            return port_channel_interfaces

        return None

    def _get_port_channel_interface_cfg(self, adapter: dict, channel_group_id: int, connected_endpoint: dict) -> dict:
        """
        Return structured_config for one port_channel_interface
        """
        peer = connected_endpoint["name"]
        adapter_port_channel_description = get(adapter, "port_channel.description")
        port_channel_type = "routed" if get(adapter, "port_channel.subinterfaces") else "switched"
        port_channel_mode = get(adapter, "port_channel.mode")
        node_index = adapter["switches"].index(self._hostname)

        # Common port_channel_interface settings
        port_channel_interface = {
            "description": self._avd_interface_descriptions.connected_endpoints_port_channel_interfaces(peer, adapter_port_channel_description),
            "type": port_channel_type,
            "shutdown": not get(adapter, "port_channel.enabled", default=True),
            "mtu": adapter.get("mtu"),
            "service_profile": adapter.get("qos_profile"),
            "link_tracking_groups": self._get_adapter_link_tracking_groups(adapter),
            "eos_cli": get(adapter, "port_channel.raw_eos_cli"),
            "struct_cfg": get(adapter, "port_channel.structured_config"),
        }

        # Only switches interfaces
        if port_channel_type == "switched":
            port_channel_interface.update(
                {
                    "mode": adapter.get("mode"),
                    "l2_mtu": adapter.get("l2_mtu"),
                    "vlans": adapter.get("vlans"),
                    "trunk_groups": self._get_adapter_trunk_groups(adapter, connected_endpoint),
                    "native_vlan_tag": adapter.get("native_vlan_tag"),
                    "native_vlan": adapter.get("native_vlan"),
                    "spanning_tree_portfast": adapter.get("spanning_tree_portfast"),
                    "spanning_tree_bpdufilter": adapter.get("spanning_tree_bpdufilter"),
                    "spanning_tree_bpduguard": adapter.get("spanning_tree_bpduguard"),
                    "storm_control": self._get_adapter_storm_control(adapter),
                }
            )

        # EVPN A/A
        if (short_esi := self._get_short_esi(adapter, channel_group_id)) is not None:
            port_channel_interface["evpn_ethernet_segment"] = self._get_adapter_evpn_ethernet_segment_cfg(adapter, short_esi, node_index, connected_endpoint)
            if port_channel_mode == "active":
                port_channel_interface["lacp_id"] = generate_lacp_id(short_esi)

        # Set MLAG ID on port-channel if connection is multi-homed and this switch is running MLAG
        elif self._mlag and len(set(adapter["switches"])) > 1:
            port_channel_interface["mlag"] = channel_group_id

        # LACP Fallback
        if port_channel_mode in ["active", "passive"] and (lacp_fallback_mode := get(adapter, "port_channel.lacp_fallback.mode")) == "static":
            port_channel_interface.update(
                {
                    "lacp_fallback_mode": lacp_fallback_mode,
                    "lacp_fallback_timeout": get(adapter, "port_channel.lacp_fallback.timeout", default=90),
                }
            )

        return strip_null_from_data(port_channel_interface)

    def _get_port_channel_subinterface_cfg(self, subinterface: dict, adapter: dict, channel_group_id: int) -> dict:
        """
        Return structured_config for one port_channel_interface (subinterface)
        """
        # Common port_channel_interface settings
        port_channel_interface = {
            "type": "l2dot1q",
            "vlan_id": subinterface.get("vlan_id", subinterface["number"]),
            "encapsulation_vlan": {
                "client": {
                    "dot1q": {
                        "vlan": get(subinterface, "encapsulation_vlan.client_dot1q", default=subinterface["number"]),
                    }
                },
                "network": {
                    "client": True,
                },
            },
        }

        # EVPN A/A
        if (
            short_esi := self._get_short_esi(adapter, channel_group_id, short_esi=subinterface.get("short_esi"), hash_extra_value=str(subinterface["number"]))
        ) is not None:
            port_channel_interface["evpn_ethernet_segment"] = {
                "identifier": generate_esi(short_esi, self._evpn_short_esi_prefix),
                "route_target": generate_route_target(short_esi),
            }

        return strip_null_from_data(port_channel_interface)
