"""Send a message."""


import xprpy


data = [
    # Not specifying an account with the "to" field will send the message to the same account sending it in the "from" field
    xprpy.Data(name="from", value=xprpy.types.Name("me.wam")),
    xprpy.Data(
        name="message",
        value=xprpy.types.String("hello from xprpy"), # String specified for message type, type must be specificed
    ),
]

auth = xprpy.Authorization(actor="me.wam", permission="active")

action = xprpy.Action(
    account="me.wam",
    name="sendmsg",
    data=data,
    authorization=[auth],
)

raw_transaction = xprpy.Transaction(actions=[action])

net = xprpy.Local()
linked_transaction = raw_transaction.link(net=net)

key = "a_very_secret_key"
signed_transaction = linked_transaction.sign(key=key)

resp = signed_transaction.send()
