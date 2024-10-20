"""transaction tests."""

import datetime as dt
import json

import pydantic
import pytest

import xprpy

from .contracts.valid import eosio_token as eosio_token_contract
from .contracts.valid import hello as valid_contract


def test_create_authorization_using_dict():
    auth = xprpy.Authorization.parse_obj(
        {"actor": "aaa", "permission": "active"}
    )
    assert isinstance(auth, xprpy.Authorization)


def test_create_authorization_using_keywords():
    auth = xprpy.Authorization(actor="aaa", permission="active")
    assert isinstance(auth, xprpy.Authorization)


def test_create_authorization_requires_actor_len_lt_13():
    with pytest.raises(pydantic.ValidationError):
        xprpy.Authorization(actor="a" * 14, permission="active")


def test_authorization_is_immutable(auth):
    with pytest.raises(TypeError):
        auth.actor = "bbb"


def test_data_dict_serialization():
    data = xprpy.Data(name="int_value", value=xprpy.types.Int8(10))
    data_json = data.dict()
    assert data_json == {"name": "int_value", "type": "Int8", "value": 10}


def test_data_json_serialization():
    data = xprpy.Data(name="int_value", value=xprpy.types.Int8(10))
    data_json = data.json()
    assert data_json == '{"name": "int_value", "type": "Int8", "value": 10}'


def test_create_data_from_dict_with_len_3():
    data_from_dict = xprpy.Data.parse_obj(
        {"name": "int_value", "type": "Int8", "value": 10}
    )
    data_from_init = xprpy.Data(
        name="int_value", value=xprpy.types.Int8(10)
    )
    assert data_from_dict == data_from_init


def test_when_create_data_from_dict_with_len_1_then_raises_value_error():
    d = {"name": "int_value"}
    with pytest.raises(ValueError):
        xprpy.Data.parse_obj(d)


def test_when_create_data_from_dict_with_len_4_then_raises_value_error():
    d = {"name": "int_value", "type": "Int8", "value": 10, "a": "a"}
    with pytest.raises(ValueError):
        xprpy.Data.parse_obj(d)


def test_backend_serialization_matches_server_serialization(net):
    data = [
        xprpy.Data(name="from", value=xprpy.types.Name("user2")),
        xprpy.Data(
            name="message",
            value=xprpy.types.String("hello"),
        ),
    ]
    backend_data_bytes = b""
    for d in data:
        backend_data_bytes += bytes(d)

    server_resp = net.abi_json_to_bin(
        account_name="user2",
        action="sendmsg",
        json={
            "from": "user2",
            "message": "hello",
        },
    )

    server_data_bytes = server_resp

    assert backend_data_bytes == server_data_bytes


def test_backend_transfer_transaction_serialization(net):
    data = [
        xprpy.Data(name="from", value=xprpy.types.Name("user2")),
        xprpy.Data(name="to", value=xprpy.types.Name("user2")),
        xprpy.Data(
            name="quantity",
            value=xprpy.types.Asset(str(2**61) + " XPR"),
        ),
        xprpy.Data(
            name="memo",
            value=xprpy.types.String("Trying xprpy"),
        ),
    ]
    backend_data_bytes = b""
    for d in data:
        backend_data_bytes += bytes(d)

    server_resp = net.abi_json_to_bin(
        account_name="eosio.token",
        action="transfer",
        json={
            "from": "user2",
            "to": "user2",
            "quantity": str(2**61) + " XPR",
            "memo": "Trying xprpy",
        },
    )

    server_data_bytes = server_resp

    assert backend_data_bytes == server_data_bytes


def test_backend_json_to_hex_abi_serialization(net):
    abi_obj = xprpy.types.Abi.from_file(eosio_token_contract.path_abi)

    server_resp = net.get_raw_code_and_abi(account_name="eosio.token")
    server_abi = server_resp["abi"]
    server_abi_hex = xprpy.types.compostes._bin_to_hex(server_abi)

    assert server_abi_hex == abi_obj.to_hex()


def test_backend_set_wasm_code_transaction_serialization(net):
    wasm_obj = xprpy.types.Wasm.from_file(valid_contract.path_zip)

    data = [
        xprpy.Data(name="account", value=xprpy.types.Name("user2")),
        xprpy.Data(name="vmtype", value=xprpy.types.Uint8(0)),
        xprpy.Data(name="vmversion", value=xprpy.types.Uint8(0)),
        xprpy.Data(name="code", value=wasm_obj),
    ]
    backend_data_bytes = b""
    for d in data:
        backend_data_bytes += bytes(d)

    server_resp = net.abi_json_to_bin(
        account_name="eosio",
        action="setcode",
        json={
            "account": "user2",
            "vmtype": 0,
            "vmversion": 0,
            "code": wasm_obj.to_hex(),
        },
    )

    server_data_bytes = server_resp

    assert backend_data_bytes == server_data_bytes


def test_backend_set_abi_transaction_serialization(net):
    abi_obj = xprpy.types.Abi.from_file(valid_contract.path_abi)

    data = [
        xprpy.Data(name="account", value=xprpy.types.Name("user2")),
        xprpy.Data(name="abi", value=abi_obj),
    ]
    pyntelope_serialized_data = b""
    for d in data:
        pyntelope_serialized_data += bytes(d)

    leap_serialized_data = net.abi_json_to_bin(
        account_name="eosio",
        action="setabi",
        json={"account": "user2", "abi": abi_obj.to_hex()},
    )

    assert leap_serialized_data == pyntelope_serialized_data


def test_data_bytes_hex_return_expected_value():
    data = [
        xprpy.Data(
            name="from", value=xprpy.types.Name("youraccount1")
        ),
        xprpy.Data(name="to", value=xprpy.types.Name("argentinaeos")),
        xprpy.Data(
            name="memo",
            value=xprpy.types.String(" This tx was sent using PYNTELOPE"),
        ),
    ]
    data_bytes = [bytes(d) for d in data]
    data = xprpy.types.Array.from_dict(
        data_bytes, type_=xprpy.types.Bytes
    )
    bytes_ = bytes(data)
    action_hex = bytes_.hex()
    expected = "0310f2d414217335f580a932d3e5a9d835212054686973207478207761732073656e74207573696e672050594e54454c4f5045"  # NOQA: E501
    assert action_hex == expected


def test_create_action():
    auth = [xprpy.Authorization(actor="user2", permission="active")]
    data = []

    action = xprpy.Action(
        account="user2",
        name="clear",
        data=data,
        authorization=auth,
    )

    assert isinstance(action, xprpy.Action)


def test_action_requirest_at_least_one_auth():
    with pytest.raises(pydantic.ValidationError):
        xprpy.Action(
            account="user2",
            name="clear",
            data=[],
            authorization=[],
        )


def test_when_action_link_returns_linked_action(net):
    action = xprpy.Action(
        account="user2",
        name="sendmsg",
        data=[
            xprpy.Data(name="from", value=xprpy.types.Name("user1")),
            xprpy.Data(
                name="message",
                value=xprpy.types.String("msg sent using xprpy"),
            ),
        ],
        authorization=[
            xprpy.Authorization(actor="user1", permission="active"),
        ],
    )
    linked_action = action.link(net=net)
    assert isinstance(linked_action, xprpy.LinkedAction)


@pytest.fixture
def action_clear():
    auth = [xprpy.Authorization(actor="user2", permission="active")]
    data = []
    action = xprpy.Action(
        account="user2",
        name="clear",
        data=data,
        authorization=auth,
    )
    yield action


def test_action_fields_are_immutable(action_clear):
    immutables = (str, int, bool, float, tuple)
    for field_name in action_clear.__fields__:
        field = getattr(action_clear, field_name)
        assert isinstance(field, immutables)


def test_create_transaction(action_clear):
    trans = xprpy.Transaction(actions=[action_clear])
    assert isinstance(trans, xprpy.Transaction)


def test_when_link_raw_transaction_then_returns_linked_transaction(
    action_clear, net
):
    raw_trans = xprpy.Transaction(actions=[action_clear])
    linked_trans = raw_trans.link(net=net)
    assert isinstance(linked_trans, xprpy.LinkedTransaction)


def test_when_sign_linked_transaction_then_return_signed_transaction(
    action_clear, net
):
    raw_trans = xprpy.Transaction(actions=[action_clear])
    linked_trans = raw_trans.link(net=net)
    signed_trans = linked_trans.sign(
        key="5HsVgxhxdL9gvgcAAyCZSWNgtLxAhGfEX2YU98w6QSkePoVvPNK"
    )
    assert isinstance(signed_trans, xprpy.SignedTransaction)


# transaction serialization, id and signature


@pytest.fixture
def example_transaction(net):
    action = xprpy.LinkedAction(
        net=net,
        account="user2",
        name="sendmsg",
        data=[
            xprpy.Data(name="from", value=xprpy.types.Name("user2")),
            xprpy.Data(
                name="message",
                value=xprpy.types.String("hello"),
            ),
        ],
        authorization=[
            xprpy.Authorization(actor="user2", permission="active"),
        ],
    )
    linked_trans = xprpy.LinkedTransaction(
        actions=[action.link(net)],
        net=net,
        expiration_delay_sec=0,
        delay_sec=0,
        max_cpu_usage_ms=0,
        max_net_usage_words=0,
        chain_id=(
            "8a34ec7df1b8cd06ff4a8abbaa7cc50300823350cadc59ab296cb00d104d2b8f"
        ),
        ref_block_num=23631,
        ref_block_prefix=2938989125,
        expiration=dt.datetime(2021, 8, 30, 13, 3, 31),
    )
    yield linked_trans


def test_example_transaction_pack(example_transaction):
    expected = "23d72c614f5c456a2daf000000000100000000007115d6000000806199a6c20100000000007115d600000000a8ed32320e00000000007115d60568656c6c6f00"  # NOQA: E501
    print(f"expected = {expected}")
    assert bytes(example_transaction).hex() == expected


def test_example_transaction_id(example_transaction):
    expected = "1a634bb62717cb1a94f5312c7d369b95fe7ea3f1f955a8c1907a74cf0d4153d6"  # NOQA: E501
    assert example_transaction.id() == expected


def test_example_transaction_has_expected_signature(example_transaction):
    key = "5K5UHY2LjHw2QQFJKCd2PdF7hxPJnknMfQLhxbEguJJttr1DFdp"
    signed_transaction = example_transaction.sign(key=key)
    expected = "SIG_K1_HMzTApq6UiSA7Ldr6mCKqPKQkrsmUknHiZi4HZt7HMz3ktHHMv4MuRTEUx9Za8VbB6NzcUFh35EBj4Y9wtVjw9qL3t4xYX"  # NOQA: E501
    assert signed_transaction.signatures[0] == expected


@pytest.fixture
def trans_signed(action_clear, net):
    raw_trans = xprpy.Transaction(actions=[action_clear])
    linked_trans = raw_trans.link(net=net)
    trans = linked_trans.sign(
        key="5K5UHY2LjHw2QQFJKCd2PdF7hxPJnknMfQLhxbEguJJttr1DFdp",
    )
    yield trans


def test_signed_transaction_has_1_signature(trans_signed):
    assert len(trans_signed.signatures) == 1


def test_when_sign_signed_transaction_then_return_signed_transaction(
    trans_signed,
):
    trans2 = trans_signed.sign(
        key="5K5UHY2LjHw2QQFJKCd2PdF7hxPJnknMfQLhxbEguJJttr1DFdp"
    )
    assert isinstance(trans2, xprpy.SignedTransaction)


def test_double_signed_transaction_has_2_signatures(
    trans_signed,
):
    trans2 = trans_signed.sign(
        key="5K5UHY2LjHw2QQFJKCd2PdF7hxPJnknMfQLhxbEguJJttr1DFdp"
    )
    assert len(trans2.signatures) == 2


def test_when_send_example_transaction_then_returns_expired_transaction_error(
    net, example_transaction
):
    trans = example_transaction.sign(
        key="5K5UHY2LjHw2QQFJKCd2PdF7hxPJnknMfQLhxbEguJJttr1DFdp"
    )
    resp = net.push_transaction(transaction=trans)
    assert resp["error"]["what"] == "Expired Transaction"


def test_e2e_with_transaction_ok(net):
    data = [
        xprpy.Data(name="from", value=xprpy.types.Name("user2")),
        xprpy.Data(
            name="message",
            value=xprpy.types.String("I cant say hello again"),
        ),
    ]
    trans = xprpy.Transaction(
        actions=[
            xprpy.Action(
                account="user2",
                name="sendmsg",
                data=data,
                authorization=[
                    xprpy.Authorization(actor="user2", permission="active")
                ],
            )
        ],
    )
    linked_trans = trans.link(net=net)
    signed_trans = linked_trans.sign(
        key="5K5UHY2LjHw2QQFJKCd2PdF7hxPJnknMfQLhxbEguJJttr1DFdp"
    )
    resp = signed_trans.send()
    print(json.dumps(resp, indent=4))
    assert "transaction_id" in resp
    assert resp["transaction_id"] == signed_trans.id()
    assert "processed" in resp
    assert "receipt" in resp["processed"]
    assert "status" in resp["processed"]["receipt"]
    assert resp["processed"]["receipt"]["status"] == "executed"
    actions = resp["processed"]["action_traces"]
    assert len(actions) == 1


def test_e2e_with_transaction_signed_with_the_wrong_key(net):
    data = [
        xprpy.Data(name="from", value=xprpy.types.Name("user2")),
        xprpy.Data(
            name="message",
            value=xprpy.types.String("I cant say hello"),
        ),
    ]
    trans = xprpy.Transaction(
        actions=[
            xprpy.Action(
                account="user2",
                name="sendmsg",
                data=data,
                authorization=[
                    xprpy.Authorization(actor="user2", permission="active")
                ],
            )
        ],
    )
    linked_trans = trans.link(net=net)
    signed_trans = linked_trans.sign(
        key="5Je7woBXuxQBkpxit35SHZMap9SdKZLoeVBRKxntoMq2NuuN1rL"  # wrong key
    )
    resp = signed_trans.send()
    assert "code" in resp
    assert resp["code"] == 500
    assert "error" in resp
    assert "details" in resp["error"]
    assert len(resp["error"]["details"]) == 1
