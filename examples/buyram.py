"""Buy some ram to some account."""


import xprpy

data = [
    # in this case the account me.wam is buying ram for itself
    xprpy.Data(name="payer", value=xprpy.types.Name("me.wam")),
    xprpy.Data(name="receiver", value=xprpy.types.Name("me.wam")),
    xprpy.Data(
        name="quant", # Selects the 'quant' field in this action, must be a valid field in the action
        value=xprpy.types.Asset("5.00000000 XPR"), # Asset type must be specified as quant requires the amount and currency type, which Asset includes
    ),
]

auth = xprpy.Authorization(actor="me.wam", permission="active")

action = xprpy.Action(
    account="eosio",
    name="buyram",
    data=data,
    authorization=[auth],
)

raw_transaction = xprpy.Transaction(actions=[action])

net = xprpy.XPRTestnet()
linked_transaction = raw_transaction.link(net=net)

key = "a_very_secret_key"
signed_transaction = linked_transaction.sign(key=key)

resp = signed_transaction.send()
