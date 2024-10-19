"""Vote to a nice blockproducer ;) ."""

import xprpy

data = [
    # Specifices the voter account
    xprpy.Data(
        name="voter",
        value=xprpy.types.Name("me.wam"),
    ),
    # Specifices the proxy (can be empty)
    xprpy.Data(
        name="proxy",
        value=xprpy.types.Name(""),
    ),
    # Specifics the producers
    xprpy.Data(
        name="producers",
        # One can vote for mutliple producers, so value is of type array
        # An Array is what is called a Composte type. It is formed of multiple
        # others xprpy types.
        # Compostes types instantiation are more verbose.
        value=xprpy.types.Array.from_dict(
            ["eosiodetroit"], type_=xprpy.types.Name
        ),
        # If you want to instantiate it directly you'd need to provide a tuple
        # of names:
        # value=xprpy.types.Array(
        #     values=(xprpy.types.Name("eosiodetroit")),
        #     type_=xprpy.types.Name,
        # ),
    ),
]

auth = xprpy.Authorization(actor="me.wam", permission="active")

action = xprpy.Action(
    account="eosio",
    name="voteproducer",
    data=data,
    authorization=[auth],
)

raw_transaction = xprpy.Transaction(actions=[action])

net = xprpy.XPRTestnet()
linked_transaction = raw_transaction.link(net=net)

key = "a_very_secret_key"
signed_transaction = linked_transaction.sign(key=key)

resp = signed_transaction.send()
