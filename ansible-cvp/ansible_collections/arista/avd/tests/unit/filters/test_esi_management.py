from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.arista.avd.plugins.filter.esi_management import FilterModule, generate_esi, generate_lacp_id, generate_route_target
from ansible_collections.arista.avd.tests.unit.filters.filter_utils import convert_esi_short_to_route_target_format

ESI_SHORT = "0303:0202:0101"
ESI_PREFIX = "1111:1111"
ESI_SHORT_1 = "0404:0202:0101"


f = FilterModule()


class TestEsiManagementFilter:
    def test_generate_esi_without_prefix(self):
        resp = generate_esi(ESI_SHORT)
        assert resp == "0000:0000:" + ESI_SHORT

    def test_generate_esi_with_prefix(self):
        assert ESI_PREFIX is not None and ESI_PREFIX != ""
        resp = generate_esi(ESI_SHORT, ESI_PREFIX)
        assert resp == ESI_PREFIX + ESI_SHORT

    def test_lacp_id(self):
        assert ESI_SHORT_1 is not None and ESI_SHORT_1 != ""
        resp = generate_lacp_id(ESI_SHORT_1)
        assert ":" not in resp
        assert "." in resp

    def test_generate_route_target(self):
        route_target_format_esi = convert_esi_short_to_route_target_format(ESI_SHORT)
        resp = generate_route_target(ESI_SHORT)
        assert resp == route_target_format_esi
        resp1 = generate_route_target(None)
        assert resp1 is None

    def test_esi_management_filter(self):
        resp = f.filters()
        assert isinstance(resp, dict)
        assert "generate_route_target" in resp.keys()
        assert "generate_lacp_id" in resp.keys()
        assert "generate_esi" in resp.keys()
