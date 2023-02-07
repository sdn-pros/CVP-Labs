from __future__ import annotations

from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.utils import default, get

from .utils import UtilsMixin


class IpIgmpSnoopingMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def ip_igmp_snooping(self) -> dict | None:
        """
        Return structured config for ip_igmp_snooping
        """

        if not self._network_services_l2:
            return None

        ip_igmp_snooping = {}
        igmp_snooping_enabled = get(self._hostvars, "switch.igmp_snooping_enabled", required=True)
        ip_igmp_snooping["globally_enabled"] = igmp_snooping_enabled
        if not (igmp_snooping_enabled is True):
            return ip_igmp_snooping

        vlans = {}
        for tenant in self._filtered_tenants:
            for vrf in tenant["vrfs"]:
                for svi in vrf["svis"]:
                    if vlan := self._ip_igmp_snooping_vlan(svi, tenant):
                        vlan_id = int(svi["id"])
                        vlans[vlan_id] = vlan
            for l2vlan in tenant["l2vlans"]:
                if vlan := self._ip_igmp_snooping_vlan(l2vlan, tenant):
                    vlan_id = int(l2vlan["id"])
                    vlans[vlan_id] = vlan

        if vlans:
            ip_igmp_snooping["vlans"] = vlans

        return ip_igmp_snooping

    def _ip_igmp_snooping_vlan(self, vlan, tenant) -> dict:
        """
        ip_igmp_snooping logic for one vlan

        Can be used for both svis and l2vlans
        """
        tenant_igmp_snooping_querier = tenant.get("igmp_snooping_querier", {})
        igmp_snooping_querier = vlan.get("igmp_snooping_querier", {})
        igmp_snooping_enabled = None
        igmp_snooping_querier_enabled = None
        evpn_l2_multicast_enabled = default(
            get(vlan, "evpn_l2_multicast.enabled"),
            get(tenant, "evpn_l2_multicast.enabled"),
        )
        if self._overlay_vtep and evpn_l2_multicast_enabled is True:
            # Leaving igmp_snooping_enabled unset, to avoid extra line of config as we already check
            # that global igmp snooping is enabled and igmp snooping is required for evpn_l2_multicast.

            # Forcing querier to True since evpn_l2_multicast requires
            # querier on all vteps
            igmp_snooping_querier_enabled = True

        else:
            igmp_snooping_enabled = vlan.get("igmp_snooping_enabled")
            if self._network_services_l3 and self._uplink_type == "p2p":
                igmp_snooping_querier_enabled = default(
                    igmp_snooping_querier.get("enabled"),
                    tenant_igmp_snooping_querier.get("enabled"),
                )

        ip_igmp_snooping_vlan = {}
        if igmp_snooping_enabled is not None:
            ip_igmp_snooping_vlan["enabled"] = igmp_snooping_enabled

        if igmp_snooping_querier_enabled is not None:
            ip_igmp_snooping_vlan["querier"] = {"enabled": igmp_snooping_querier_enabled}
            # TODO: The if below should be uncommented when we have settled the behavioral change
            # if svi_igmp_snooping_querier_enabled is True:
            address = default(igmp_snooping_querier.get("source_address"), tenant_igmp_snooping_querier.get("source_address"), self._router_id)
            if address is not None:
                ip_igmp_snooping_vlan["querier"]["address"] = address

            version = default(
                igmp_snooping_querier.get("version"),
                tenant_igmp_snooping_querier.get("version"),
            )
            if version is not None:
                ip_igmp_snooping_vlan["querier"]["version"] = version

        return ip_igmp_snooping_vlan
