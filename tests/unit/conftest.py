import pytest

import xprpy


@pytest.fixture(scope="module")
def net():
    net = xprpy.Net(host="http://127.0.0.1:8888")
    yield net


@pytest.fixture
def auth():
    auth = xprpy.Authorization(actor="user2", permission="active")
    yield auth
