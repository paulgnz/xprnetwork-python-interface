import os
import argparse
from dotenv import load_dotenv
import xprpy

# Load environment variables from .env file
load_dotenv()

# Fetch the private key from the environment
key = os.getenv("XPRNETWORK_PRIVATE_KEY")

if not key:
    raise ValueError("XPRNETWORK_PRIVATE_KEY is not set in the environment")

# Set up argparse to accept command-line arguments
parser = argparse.ArgumentParser(description="Transfer XPR between accounts")
parser.add_argument("sender", type=str, help="The account name of the sender")
parser.add_argument("receiver", type=str, help="The account name of the receiver")
parser.add_argument("amount", type=str, help="The amount of XPR to send (e.g., '55.00000000 XPR')")
parser.add_argument("--memo", type=str, default="", help="Optional memo for the transfer")
parser.add_argument("--testnet", action="store_true", help="Use XPRTestnet instead of XPRMainnet")

args = parser.parse_args()

# Prepare the transfer data
data = [
    xprpy.Data(name="from", value=xprpy.types.Name(args.sender)),
    xprpy.Data(name="to", value=xprpy.types.Name(args.receiver)),
    xprpy.Data(
        name="quantity",  # Selects the 'quantity' field in this action
        value=xprpy.types.Asset(args.amount),  # Specify amount and currency
    ),
    xprpy.Data(
        name="memo",
        value=xprpy.types.String(args.memo),  # Optional memo message
    ),
]

# Authorization for the sender's account
auth = xprpy.Authorization(actor=args.sender, permission="active")

# Create the transfer action
action = xprpy.Action(
    account="eosio.token",
    name="transfer",
    data=data,
    authorization=[auth],
)

# Determine the network to use (testnet or mainnet)
if args.testnet:
    net = xprpy.XPRTestnet()
else:
    net = xprpy.XPRMainnet()  # Assuming you have an XPRMainnet object similar to XPRTestnet

# Create and sign the transaction
raw_transaction = xprpy.Transaction(actions=[action])
linked_transaction = raw_transaction.link(net=net)
signed_transaction = linked_transaction.sign(key=key)

# Send the transaction
resp = signed_transaction.send()

# Output the response from the blockchain
print(f"Transaction response: {resp}")
