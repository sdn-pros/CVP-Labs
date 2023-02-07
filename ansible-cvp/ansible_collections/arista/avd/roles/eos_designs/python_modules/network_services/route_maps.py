from __future__ import annotations

from functools import cached_property

from .utils import UtilsMixin


class RouteMapsMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def route_maps(self) -> dict | None:
        """
        Return structured config for route_maps

        Contains two parts.
        - Route-maps for tenant bgp peers set_ipv4_next_hop parameter
        - Route-maps for EVPN services in VRF "default" (using _route_maps_default_vrf)
        """
        if not self._network_services_l3:
            return None

        route_maps = {}

        for tenant in self._filtered_tenants:
            for vrf in tenant["vrfs"]:
                # BGP Peers are already filtered in _filtered_tenants
                #  so we only have entries with our hostname in them.
                for bgp_peer in vrf["bgp_peers"]:
                    ipv4_next_hop = bgp_peer.get("set_ipv4_next_hop")
                    ipv6_next_hop = bgp_peer.get("set_ipv6_next_hop")
                    if ipv4_next_hop is None and ipv6_next_hop is None:
                        continue

                    route_map_name = f"RM-{vrf['name']}-{bgp_peer['ip_address']}-SET-NEXT-HOP-OUT"
                    if ipv4_next_hop is not None:
                        set_action = f"ip next-hop {ipv4_next_hop}"
                    else:
                        set_action = f"ipv6 next-hop {ipv6_next_hop}"

                    route_maps[route_map_name] = {
                        "sequence_numbers": {
                            10: {
                                "type": "permit",
                                "set": [set_action],
                            },
                        },
                    }

        if (route_maps_vrf_default := self._route_maps_vrf_default) is not None:
            route_maps.update(route_maps_vrf_default)

        if self._configure_bgp_mlag_peer_group and self._mlag_ibgp_origin_incomplete:
            route_maps.update(self._bgp_mlag_peer_group_route_map())

        if route_maps:
            return route_maps

        return None

    @cached_property
    def _route_maps_vrf_default(self) -> dict | None:
        """
        Route-maps for EVPN services in VRF "default"

        Called from main route_maps function
        """
        if not (self._overlay_vtep and self._overlay_evpn):
            return None

        subnets = self._vrf_default_ipv4_subnets
        static_routes = self._vrf_default_ipv4_static_routes["static_routes"]
        if not subnets and not static_routes:
            return None

        route_maps = {
            "RM-EVPN-EXPORT-VRF-DEFAULT": {
                "sequence_numbers": {},
            },
            "RM-BGP-UNDERLAY-PEERS-OUT": {
                "sequence_numbers": {
                    20: {
                        "type": "permit",
                    }
                }
            },
            "RM-CONN-2-BGP": {
                "sequence_numbers": {
                    # Add subnets to redistribution in default VRF
                    # sequence 10 is set in underlay and sequence 20 in inband management, so avoid setting those here
                    30: {
                        "type": "permit",
                        "match": ["ip address prefix-list PL-SVI-VRF-DEFAULT"],
                    },
                },
            },
        }

        if subnets:
            route_maps["RM-EVPN-EXPORT-VRF-DEFAULT"]["sequence_numbers"][10] = {
                "type": "permit",
                "match": ["ip address prefix-list PL-SVI-VRF-DEFAULT"],
            }
            route_maps["RM-BGP-UNDERLAY-PEERS-OUT"]["sequence_numbers"][10] = {
                "type": "deny",
                "match": ["ip address prefix-list PL-SVI-VRF-DEFAULT"],
            }

        if static_routes:
            route_maps["RM-EVPN-EXPORT-VRF-DEFAULT"]["sequence_numbers"][20] = {
                "type": "permit",
                "match": ["ip address prefix-list PL-STATIC-VRF-DEFAULT"],
            }
            route_maps["RM-BGP-UNDERLAY-PEERS-OUT"]["sequence_numbers"][15] = {
                "type": "deny",
                "match": ["ip address prefix-list PL-STATIC-VRF-DEFAULT"],
            }

        return route_maps

    def _bgp_mlag_peer_group_route_map(self):
        """
        Return dict with one route-map
        Origin Incomplete for MLAG iBGP learned routes

        TODO: Partially duplicated from mlag. Should be moved to a common class
        """
        return {
            "RM-MLAG-PEER-IN": {
                "sequence_numbers": {
                    10: {
                        "type": "permit",
                        "set": ["origin incomplete"],
                        "description": "Make routes learned over MLAG Peer-link less preferred on spines to ensure optimal routing",
                    }
                }
            }
        }
