from __future__ import annotations

import re
from functools import cached_property

from ansible_collections.arista.avd.plugins.filter.natural_sort import natural_sort
from ansible_collections.arista.avd.plugins.plugin_utils.errors import AristaAvdError
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get

from .utils import UtilsMixin


class EthernetInterfacesMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def ethernet_interfaces(self) -> dict | None:
        """
        Return structured config for ethernet_interfaces

        Only used with L3 or L1 network services
        """

        if not (self._network_services_l3 or self._network_services_l1):
            return None

        # Using temp variables to keep the order of interfaces from Jinja
        ethernet_interfaces = {}
        subif_parent_interface_names = set()

        if self._network_services_l3:
            for tenant in self._filtered_tenants:
                for vrf in tenant["vrfs"]:
                    # The l3_interfaces has already been filtered in _filtered_tenants
                    # to only contain entries with our hostname
                    for l3_interface in vrf["l3_interfaces"]:
                        nodes_length = len(l3_interface["nodes"])
                        if (
                            len(l3_interface["interfaces"]) != nodes_length
                            or len(l3_interface["ip_addresses"]) != nodes_length
                            or ("descriptions" in l3_interface and "description" not in l3_interface and len(l3_interface["descriptions"]) != nodes_length)
                        ):
                            raise AristaAvdError(
                                "Length of lists 'interfaces', 'nodes', 'ip_addresses' and 'descriptions' (if used) must match for l3_interfaces for"
                                f" {vrf['name']} in {tenant['name']}"
                            )

                        for node_index, node_name in enumerate(l3_interface["nodes"]):
                            if node_name != self._hostname:
                                continue

                            interface_name = str(l3_interface["interfaces"][node_index])
                            # if 'descriptions' is set, it is preferred
                            if (interface_descriptions := l3_interface.get("descriptions")) is not None:
                                interface_description = interface_descriptions[node_index]
                            else:
                                interface_description = l3_interface.get("description")
                            interface = {
                                "peer_type": "l3_interface",
                                "ip_address": l3_interface["ip_addresses"][node_index],
                                "mtu": l3_interface.get("mtu"),
                                "shutdown": not l3_interface.get("enabled", True),
                                "description": interface_description,
                                "eos_cli": l3_interface.get("raw_eos_cli"),
                                "struct_cfg": l3_interface.get("structured_config"),
                            }

                            if "." in interface_name:
                                # This is a subinterface so we need to ensure that the parent is created
                                parent_interface_name, subif_id = interface_name.split(".", maxsplit=1)
                                subif_parent_interface_names.add(parent_interface_name)

                                interface["type"] = "l3dot1q"
                                encapsulation_dot1q_vlans = l3_interface.get("encapsulation_dot1q_vlan", [])
                                if len(encapsulation_dot1q_vlans) > node_index:
                                    interface["encapsulation_dot1q_vlan"] = encapsulation_dot1q_vlans[node_index]
                                else:
                                    interface["encapsulation_dot1q_vlan"] = int(subif_id)

                            else:
                                interface["type"] = "routed"

                            if vrf["name"] != "default":
                                interface["vrf"] = vrf["name"]

                            if get(l3_interface, "ospf.enabled") is True and get(vrf, "ospf.enabled") is True:
                                interface["ospf_area"] = l3_interface["ospf"].get("area", 0)
                                interface["ospf_network_point_to_point"] = l3_interface["ospf"].get("point_to_point", False)
                                interface["ospf_cost"] = l3_interface["ospf"].get("cost")
                                ospf_authentication = l3_interface["ospf"].get("authentication")
                                if ospf_authentication == "simple" and (ospf_simple_auth_key := l3_interface["ospf"].get("simple_auth_key")) is not None:
                                    interface["ospf_authentication"] = ospf_authentication
                                    interface["ospf_authentication_key"] = ospf_simple_auth_key
                                elif (
                                    ospf_authentication == "message-digest"
                                    and (ospf_message_digest_keys := l3_interface["ospf"].get("message_digest_keys")) is not None
                                ):
                                    ospf_keys = {}
                                    for ospf_key in ospf_message_digest_keys:
                                        if not ("id" in ospf_key and "key" in ospf_key):
                                            continue

                                        ospf_keys[ospf_key["id"]] = {
                                            "hash_algorithm": ospf_key.get("hash_algorithm", "sha512"),
                                            "key": ospf_key["key"],
                                        }

                                    if ospf_keys:
                                        interface["ospf_authentication"] = ospf_authentication
                                        interface["ospf_message_digest_keys"] = ospf_keys

                            if get(l3_interface, "pim.enabled"):
                                if not vrf.get("_evpn_l3_multicast_enabled"):
                                    raise AristaAvdError(
                                        f"'pim: enabled' set on l3_interface {interface_name} on {self._hostname} requires evpn_l3_multicast: enabled: true"
                                        f" under VRF '{vrf.name}' or Tenant '{tenant.name}'"
                                    )

                                if not vrf.get("_pim_rp_addresses"):
                                    raise AristaAvdError(
                                        f"'pim: enabled' set on l3_interface {interface_name} on {self._hostname} requires at least one RP defined in"
                                        f" pim_rp_addresses under VRF '{vrf.name}' or Tenant '{tenant.name}'"
                                    )

                                interface["pim"] = {"ipv4": {"sparse_mode": True}}

                            # Strip None values from vlan before adding to list
                            interface = {key: value for key, value in interface.items() if value is not None}

                            ethernet_interfaces[interface_name] = interface

        if self._network_services_l1:
            for tenant in self._filtered_tenants:
                if "point_to_point_services" not in tenant:
                    continue

                for point_to_point_service in natural_sort(tenant["point_to_point_services"], "name"):
                    subifs = [subif for subif in point_to_point_service.get("subinterfaces", []) if subif.get("number") is not None]
                    for endpoint in point_to_point_service.get("endpoints", []):
                        if self._hostname not in endpoint.get("nodes", []):
                            continue

                        for node_index, interface_name in enumerate(endpoint["interfaces"]):
                            if endpoint["nodes"][node_index] != self._hostname:
                                continue

                            if (port_channel_mode := get(endpoint, "port_channel.mode")) in ["active", "on"]:
                                first_interface_index = list(endpoint["nodes"]).index(self._hostname)
                                first_interface_name = endpoint["interfaces"][first_interface_index]
                                channel_group_id = int("".join(re.findall(r"\d", first_interface_name)))
                                ethernet_interfaces[interface_name] = {
                                    "shutdown": False,
                                    "channel_group": {
                                        "id": channel_group_id,
                                        "mode": port_channel_mode,
                                    },
                                }
                                continue

                            if subifs:
                                # This is a subinterface so we need to ensure that the parent is created
                                subif_parent_interface_names.add(interface_name)
                                for subif in subifs:
                                    key = f"{interface_name}.{subif['number']}"
                                    ethernet_interfaces[key] = {
                                        "type": "l2dot1q",
                                        "encapsulation_vlan": {
                                            "client": {
                                                "dot1q": {
                                                    "vlan": subif["number"],
                                                },
                                            },
                                            "network": {
                                                "client": True,
                                            },
                                        },
                                        "peer_type": "l3_interface",
                                        "shutdown": False,
                                    }
                            else:
                                interface = {
                                    "type": "routed",
                                    "peer_type": "l3_interface",
                                    "shutdown": False,
                                }
                                if point_to_point_service.get("lldp_disable") is True:
                                    interface["lldp"] = {
                                        "transmit": False,
                                        "receive": False,
                                    }
                                ethernet_interfaces[interface_name] = interface

        subif_parent_interface_names = subif_parent_interface_names.difference(ethernet_interfaces.keys())
        if subif_parent_interface_names:
            for interface_name in natural_sort(subif_parent_interface_names):
                ethernet_interfaces[interface_name] = {
                    "type": "routed",
                    "peer_type": "l3_interface",
                    "shutdown": False,
                }

        if ethernet_interfaces:
            return ethernet_interfaces

        return None
