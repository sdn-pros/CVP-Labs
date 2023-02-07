from __future__ import absolute_import, division, print_function

__metaclass__ = type

from contextlib import nullcontext as does_not_raise

import pytest
from ansible.errors import AnsibleFilterError

from ansible_collections.arista.avd.plugins.filter.snmp_hash import PRIV_KEY_LENGTH, FilterModule, get_hash_object, key_from_passphrase, localize_passphrase

f = FilterModule()


class TestSNMPHashFilter:
    @pytest.mark.parametrize(
        "auth_type, result, expectation",
        [
            ("md5", "md5", does_not_raise()),
            ("sha", "sha1", does_not_raise()),
            ("sha256", "sha256", does_not_raise()),
            ("sha384", "sha384", does_not_raise()),
            ("sha512", "sha512", does_not_raise()),
            ("toto", None, pytest.raises(AnsibleFilterError)),
        ],
    )
    def test_get_hash_object(self, auth_type, result, expectation):
        with expectation:
            assert get_hash_object(auth_type).name == result

    @pytest.mark.parametrize(
        "passphrase, auth_type, result, expectation",
        [
            ("testauth", "md5", "7a3d6867d36341fcc49c7d6dd0182078", does_not_raise()),
            (
                "testauth",
                "sha",
                "d6997cbe7ffa9efa756721303e367478d0a9a61b",
                does_not_raise(),
            ),
            (
                "testauth",
                "sha224",
                "b4cdc03923d5fa37bb20ca665bf2e971b9d7521c3cc311a7d29bfed2",
                does_not_raise(),
            ),
            (
                "testauth",
                "sha256",
                "bd7b6e2a86527e0b93b65ad3d67d1fc870a420c49d53b4d652364d81e954f704",
                does_not_raise(),
            ),
            (
                "testauth",
                "sha384",
                "bf8300efa68bb5d99945fef87fafb9b564ebaccd9c371bb8184fdba1df95eaa5d05b5f0fcaacfb0a3906b6e37693c6dd",
                does_not_raise(),
            ),
            (
                "testauth",
                "sha512",
                "c005b901a9a29e140e2749bb5d51789bba97f614c3c8060a1c080d775f12494ba6d968dc22526bb06532e96e2e4d3bd0e746f2696439a4a034d040e1c7de0aaa",
                does_not_raise(),
            ),
            ("testauth", "toto", None, pytest.raises(AnsibleFilterError)),
        ],
    )
    def test_key_from_passphrase(self, passphrase, auth_type, result, expectation):
        with expectation:
            assert key_from_passphrase(passphrase, auth_type) == result

    @pytest.mark.parametrize(
        "passphrase, auth_type, engine_id, priv_type, result, expectation",
        [
            (
                "testauth",
                "md5",
                "424242424242424242",
                None,
                "a487532d40f65644034ba50bec29bd90",
                does_not_raise(),
            ),
            (
                "testauth",
                "sha",
                "424242424242424242",
                None,
                "14c3e7d55a9d67b7341e0dafba817bd33d3eb2e4",
                does_not_raise(),
            ),
            (
                "testauth",
                "sha224",
                "424242424242424242",
                None,
                "b74ddba450a2b8a2b7f1823df22b4a1efa984071c5afcefadd72cc3f",
                does_not_raise(),
            ),
            (
                "testauth",
                "sha256",
                "424242424242424242",
                None,
                "ca08c9b519c910b678faf598bc33e118272f37fd9a1522d5b4b764fea26fd9ca",
                does_not_raise(),
            ),
            (
                "testauth",
                "sha384",
                "424242424242424242",
                None,
                "84e53e90d79c258426a67a229759cfe46058339d2d9db41e12ba29fe671ecf8085c4d45049b419ea23ae2e1fa0773bff",
                does_not_raise(),
            ),
            (
                "testauth",
                "sha512",
                "424242424242424242",
                None,
                "bccbd436115c60540422ad8e98b8373dee507fd9e77730372f03dcf8e8a074a43d9f04bd6b7be64eb806bdbaeff43ccd1ca93c4606ab46eb797720e4c59abcc7",
                does_not_raise(),
            ),
            (
                "testauth",
                "toto",
                "424242424242424242",
                None,
                None,
                pytest.raises(AnsibleFilterError),
            ),
            # only testing priv with one auth algorithm, the longest, to verify key length
            (
                "testpriv",
                "sha512",
                "424242424242424242",
                "des",
                "ca5e54b5c49e7addba0046c591f8f541",
                does_not_raise(),
            ),
            (
                "testpriv",
                "sha512",
                "424242424242424242",
                "aes",
                "ca5e54b5c49e7addba0046c591f8f541",
                does_not_raise(),
            ),
            (
                "testpriv",
                "sha512",
                "424242424242424242",
                "aes192",
                "ca5e54b5c49e7addba0046c591f8f5417338cdc1043068ab",
                does_not_raise(),
            ),
            (
                "testpriv",
                "sha512",
                "424242424242424242",
                "aes256",
                "ca5e54b5c49e7addba0046c591f8f5417338cdc1043068abf8c2a7ab751f13dc",
                does_not_raise(),
            ),
            (
                "testpriv",
                "sha512",
                "424242424242424242",
                "toto",
                None,
                pytest.raises(AnsibleFilterError),
            ),
            # non hex engine_id
            (
                "testpriv",
                "sha512",
                "zzzzzzzzzzzz",
                "toto",
                None,
                pytest.raises(AnsibleFilterError),
            ),
        ],
    )
    def test_localize_passphrase(self, passphrase, auth_type, engine_id, priv_type, result, expectation):
        with expectation:
            localized_passphrase = localize_passphrase(passphrase, auth_type, engine_id, priv_type=priv_type)
            assert localized_passphrase == result
            if priv_type:
                assert len(localized_passphrase) * 4 == PRIV_KEY_LENGTH[priv_type]

    def test_snmp_hash_filter(self):
        resp = f.filters()
        assert isinstance(resp, dict)
        assert "hash_passphrase" in resp.keys()
