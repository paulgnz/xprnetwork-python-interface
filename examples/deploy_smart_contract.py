"""Deploy a smart contract."""

import xprpy

setcode_data = [
    # data to set wasm file to account me.wam
    xprpy.Data(
        name="account",
        value=xprpy.types.Name("me.wam"),
    ),
    xprpy.Data(
        name="vmtype",
        value=xprpy.types.Uint8(0),  # almost always set to 0, has to be set
    ),
    xprpy.Data(
        name="vmversion",
        value=xprpy.types.Uint8(0),  # almost always set to 0, has to be set
    ),
    xprpy.Data(
        name="code",  # select "code" field to set a wasm file
        value=xprpy.types.Wasm.from_file(
            "test_contract/test_contract.zip"
        ),  # path from current directory to wasm file
    ),
]

setabi_data = [
    xprpy.Data(
        name="account",
        value=xprpy.types.Name("me.wam"),
    ),
    xprpy.Data(
        name="abi",  # select "abi" field to set a abi file
        value=xprpy.types.Abi.from_file(
            "test_contract/test_contract.abi"
        ),  # path from current directory to abi file
    ),
]

auth = xprpy.Authorization(actor="me.wam", permission="active")

setcode_action = xprpy.Action(
    account="eosio",
    name="setcode",
    data=setcode_data,
    authorization=[auth],
)

setabi_action = xprpy.Action(
    account="eosio",
    name="setabi",
    data=setabi_data,
    authorization=[auth],
)

raw_transaction = xprpy.Transaction(
    actions=[setabi_action, setcode_action]
)

net = xprpy.XPRTestnet()
linked_transaction = raw_transaction.link(net=net)

key = "a_very_secret_key"
signed_transaction = linked_transaction.sign(key=key)

resp = signed_transaction.send()
