"""Run a `runjob` action."""


import xprpy


data = [
    xprpy.Data(
        name="worker",
        value=xprpy.types.Name("open.facings"),
    ),
    xprpy.Data(
        name="nonce",
        value=xprpy.types.Uint64(123),
    ),
]

auth = xprpy.Authorization(actor="youraccount", permission="active")

action = xprpy.Action(
    account="open.facings",
    name="runjobs",
    data=data,
    authorization=[auth],
)

raw_transaction = xprpy.Transaction(actions=[action])

net = xprpy.WaxTestnet()
linked_transaction = raw_transaction.link(net=net)

key = "a_very_secret_key"
signed_transaction = linked_transaction.sign(key=key)

resp = signed_transaction.send()
