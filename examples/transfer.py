"""Transfer some WAX to a receiver account."""

import xprpy

data = [
    # In this case the account me.wam is transferring to account 'reciever'
    xprpy.Data(name="from", value=xprpy.types.Name("me.wam")),
    xprpy.Data(name="to", value=xprpy.types.Name("receiver")),
    xprpy.Data(
        name="quantity", # Selects the 'quantity' field in this action, must be a valid field in the action
        value=xprpy.types.Asset("55.00000000 WAX"), # Asset type must be specified as 'quantity' requires the amount and currency type, which Asset includes
    ),
    xprpy.Data(
        name="memo", # Selects the 'memo' field in this action, just an extra message with the transfer
        value=xprpy.types.String("Trying xprpy"), # String type is used for memo
    ),
]

auth = xprpy.Authorization(actor="me.wam", permission="active")

action = xprpy.Action(
    account="eosio.token",
    name="transfer",
    data=data,
    authorization=[auth],
)

raw_transaction = xprpy.Transaction(actions=[action])

net = xprpy.WaxTestnet()
linked_transaction = raw_transaction.link(net=net)

key = "a_very_secret_key"
signed_transaction = linked_transaction.sign(key=key)

resp = signed_transaction.send()
