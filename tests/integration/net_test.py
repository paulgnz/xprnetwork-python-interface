import re

import pytest

import xprpy

aliases = [
    xprpy.EosMainnet,
    xprpy.KylinTestnet,
    xprpy.Jungle3Testnet,
    xprpy.TelosMainnet,
    xprpy.TelosTestnet,
    xprpy.ProtonMainnet,
    xprpy.ProtonTestnet,
    xprpy.UosMainnet,
    xprpy.FioMainnet,
    xprpy.XPRTestnet,
    xprpy.WaxMainnet,
]


@pytest.mark.flaky(reruns=5)
@pytest.mark.parametrize("alias", aliases)
def test_get_info_from_alias(alias):
    net = alias()
    info = net.get_info()
    assert isinstance(info, dict)
    assert "chain_id" in info
    patt = r"[a-f0-9]{64}"
    assert re.fullmatch(patt, info["chain_id"])
