<div align="center">
    
*Minimalist python library to interact with "XPR Network" blockchain also known as "XPR" or "XPRNetwork"*


</div>

# What is it?
**xprpy** is a python library to interact with XPR Network, an XPR Network.  
Its main focus are server side applications.  
This library is heavily influenced by µEOSIO and forked from FACINGS pyntelope. Many thanks to them for the astonishing job!  


# Main features
- Send transactions
Its main usage today is to send transactions to the blockchain
- Statically typed
This library enforces and verifies types and values.
- Serialization
**xprpy** serializes the transaction before sending to the blockchain. 
- Paralellization
Although python has the [GIL](https://realpython.com/python-gil/) we try to make as easier as possible to paralellize the jobs.  
All data is as immutable and all functions are as pure as we can make them.  


# Stability
This work is in alpha version. That means that we make constant breaking changes to its api.


# Using
## How to Use the `transfer.py` Function

The `transfer.py` script allows you to transfer XPR tokens between accounts via the command line.

### Command-Line Arguments

- `sender`: The account sending the XPR tokens.
- `receiver`: The account receiving the XPR tokens.
- `amount`: The amount of XPR to send (e.g., "55.0000 XPR").
- `--memo`: (Optional) A memo to include with the transaction.
- `--testnet`: (Optional) Use this flag to run the transaction on the XPR Testnet. If not provided, the transaction will be sent to the XPR Mainnet.

### Example Usage

See the examples folder for transfer.py
Use environment variables:
XPRNETWORK_ACCOUNT=your_account
XPRNETWORK_PRIVATE_KEY=your_private_key

1. **Transfer on Mainnet:**

   To send 55.0000 XPR from the account `a.babyagi` to `paul` on the XPR Mainnet with an optional memo:

   ```bash
   python transfer.py a.babyagi paul "55.0000 XPR" --memo "Mainnet transaction"

2. **Transfer on Testnet:**

   To send 55.0000 XPR from the account `a.babyagi` to `paul` on the XPR Testnet with an optional memo:

   ```bash
   python transfer.py a.babyagi paul "55.0000 XPR" --memo "Testnet transaction" --testnet


