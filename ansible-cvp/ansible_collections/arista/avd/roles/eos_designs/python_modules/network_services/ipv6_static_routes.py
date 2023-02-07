from __future__ import annotations

from functools import cached_property

from .utils import UtilsMixin


class Ipv6StaticRoutesMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def ipv6_static_routes(self) -> list[dict] | None:
        """
        Returns structured config for ipv6_static_routes

        Consist of
        - ipv6 static_routes defined under the vrfs
        - static routes added automatically for VARPv6 with prefixes
        """

        if not self._network_services_l3:
            return None

        ipv6_static_routes = []
        for tenant in self._filtered_tenants:
            for vrf in tenant["vrfs"]:
                for static_route in vrf["ipv6_static_routes"]:
                    static_route["vrf"] = vrf["name"]
                    static_route.pop("nodes", None)
                    ipv6_static_routes.append(static_route)

        if ipv6_static_routes:
            return ipv6_static_routes

        return None
