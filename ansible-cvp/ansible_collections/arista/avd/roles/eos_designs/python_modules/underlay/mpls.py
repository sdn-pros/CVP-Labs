from __future__ import annotations

from functools import cached_property

from .utils import UtilsMixin


class MplsMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def mpls(self) -> dict | None:
        """
        Return structured config for mpls
        """
        if self._underlay_mpls is not True:
            return None

        if self._underlay_ldp is True:
            return {
                "ip": True,
                "ldp": {
                    "interface_disabled_default": True,
                    "router_id": self._router_id,
                    "shutdown": False,
                    "transport_address_interface": "Loopback0",
                },
            }

        return {"ip": True}
