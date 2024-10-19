"""Stake cpu / delegate bandwitdh to an account."""

import xprpy

data = [
    # In this case the account me.wam is staking cpu for itself
    xprpy.Data(name="from", value=xprpy.types.Name("me.wam")),
    xprpy.Data(name="receiver", value=xprpy.types.Name("me.wam")),
    xprpy.Data(
        name="stake_cpu_quantity", # Selects the 'stake_cpu_quantity' field in this action to stake cpu, any fields must exist in the action to be selected
        value=xprpy.types.Asset("15.00000000 XPR"), # Asset type must be specified as 'stake_cpu_quantity' requires the amount and currency type, which Asset includes
    ),
    xprpy.Data(
        name="stake_net_quantity", # Selects the 'stake_net_quantity' field in this action to stake net
        value=xprpy.types.Asset("30.00000000 XPR"), # Asset type must be specified as 'stake_net_quantity' requires the amount and currency type, which Asset includes
    ),
    xprpy.Data(
        name="transfer", # Selects the 'transfer' field in this action to stake cpu
        value=xprpy.types.Bool(False), # Bool type used to indicate transfer
    ),
]

auth = xprpy.Authorization(actor="me.wam", permission="active")

action = xprpy.Action(
    account="eosio",
    name="delegatebw",
    data=data,
    authorization=[auth],
)

raw_transaction = xprpy.Transaction(actions=[action])

net = xprpy.XPRTestnet()
linked_transaction = raw_transaction.link(net=net)

key = "a_very_secret_key"
signed_transaction = linked_transaction.sign(key=key)

resp = signed_transaction.send()
