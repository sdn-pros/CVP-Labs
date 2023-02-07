from __future__ import annotations

from functools import cached_property

from .utils import UtilsMixin


class RouterOspfMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def router_ospf(self) -> dict | None:
        """
        Return structured config for router_ospf
        """

        if not self._underlay_ospf:
            return None

        no_passive_interfaces = [
            p2p_link["data"]["interface"] for p2p_link in self._filtered_p2p_links if p2p_link.get("include_in_underlay_protocol", True) is True
        ]
        if no_passive_interfaces:
            return {
                "process_ids": {
                    self._underlay_ospf_process_id: {
                        "no_passive_interfaces": no_passive_interfaces,
                    }
                }
            }

        return None
