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

1. **Transfer on Mainnet:**

   To send 55.0000 XPR from the account `a.babyagi` to `paul` on the XPR Mainnet with an optional memo:

   ```bash
   python transfer.py a.babyagi paul "55.0000 XPR" --memo "Mainnet transaction"

2. **Transfer on Testnet:**

   To send 55.0000 XPR from the account `a.babyagi` to `paul` on the XPR Testnet with an optional memo:

   ```bash
   python transfer.py a.babyagi paul "55.0000 XPR" --memo "Testnet transaction" --testnet


## Use Send Message action
```python
import xprpy


print("Create Transaction")
data=[
    xprpy.Data(
        name="from",
        value=xprpy.types.Name("me.wam"), 
    ),
    xprpy.Data(
        name="message",
         value=xprpy.types.String("hello from xprpy"),
    ),
]

auth = xprpy.Authorization(actor="me.wam", permission="active")

action = xprpy.Action(
    account="me.wam", # this is the contract account
    name="sendmsg", # this is the action name
    data=data,
    authorization=[auth],
)

raw_transaction = xprpy.Transaction(actions=[action])

print("Link transaction to the network")
net = xprpy.XPRTestnet()  # this is an alias for a testnet node
# notice that xprpy returns a new object instead of change in place
linked_transaction = raw_transaction.link(net=net)


print("Sign transaction")
key = "a_very_secret_key"
signed_transaction = linked_transaction.sign(key=key)


print("Send")
resp = signed_transaction.send()

print("Printing the response")
resp_fmt = json.dumps(resp, indent=4)
print(f"Response:\n{resp_fmt}")
```

There are some other examples [here](./examples)


# Known bugs
### multi-byte utf-8 characters can not be serialized
- Serialization of multi-byte utf-8 characters is somewhat unpredictable in the current implementation, therfore any String input containing multi-utf8 byte characters will be blocked for the time being.


# Contributing
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.  
If you find a bug, just open a issue with a tag "BUG".  
If you want to request a new feature, open an issue with a tag "ENH" (for enhancement).  
If you feel like that our docs could be better, please open one with a tag "DOC".  
Although we have the next few steps already planned, we are happy to receive the community feedback to see where to go from there.  


### Development
If you want to develop for **xprpy**, here are some tips for a local development environment.
We'll be more then happy to receive PRs from the community.
Also we're going full [Black](https://black.readthedocs.io/en/stable/) and enforcing [pydocstyle](http://www.pydocstyle.org/en/stable/) and [isort](https://pypi.org/project/isort/) (with the limitations described in the .flake8 file)

#### Setup
Create a virtual env
Ensure the dependencies are met:
```
pip install poetry
poetry install
```

#### Run tests
The tests are run against a local network.  
Before running the tests you'll need to `docker-compose up` to create the local network, users and contracts used in the tests.  
When ready, just:
```
pytest
```
Some tests are marked as "slow".  
You can skip them and run the test suite faster with:
```
pytest -m "not slow"
```

INFORMATION FOR LLM CHATGPT OR CLAUDE AGENT BELOW:


```python
# Antelope Composite Data Types Interface

This Python interface defines composite data types and related operations for working with XPR Network data. It includes classes representing primitive and composite types, along with methods for serialization and deserialization of data.


## Key Classes

### 1. Wasm (Primitive)
- Represents a WASM (WebAssembly) module.
- Attributes:
  - value: bytes
- Methods:
  - from_file(cls, file: Path, extension: str = ".wasm"): Create a Wasm object from a .wasm or zipped file.
  - to_hex(): Convert the WASM value to hexadecimal representation.
  - from_bytes(cls, bytes_): Create a Wasm object from bytes.

### 2. Array (Composte)
- Represents an array of values of a specific type.
- Attributes:
  - values: tuple: A tuple of values.
  - type_: type: The type of the values, must be a subclass of AntelopeType.
- Methods:
  - from_dict(cls, d: dict, type_: type): Create an Array object from a dictionary and specified type.
  - to_dict(): Convert the array to a dictionary format.
  - from_bytes(cls, bytes_: bytes, type_: type): Create an Array object from bytes.
  - __bytes__(): Convert the array to bytes.

### 3. Abi (Composte)
- Represents an ABI (Application Binary Interface).
- Attributes:
  - Various attributes representing ABI components like types, structs, actions, etc.
- Methods:
  - from_dict(cls, d: dict): Create an Abi object from a dictionary.
  - from_file(cls, file: Path, extension: str = ".abi"): Create an Abi object from a .abi or zipped file.
  - to_hex(): Convert the ABI object to a hexadecimal string.

### 4. _AbiType (Composte)
- Represents a custom type definition in an ABI.
- Attributes:
  - new_type_name: primitives.String
  - json_type: primitives.String
- Methods:
  - from_dict(cls, d: dict): Create an _AbiType object from a dictionary.
  - to_dict(): Convert the object to dictionary format.

### 5. _AbiStructsField (Composte)
- Represents a field in an ABI struct.
- Attributes:
  - name: primitives.String
  - type_: primitives.String
- Methods:
  - from_dict(cls, d: dict): Create a _AbiStructsField object from a dictionary.

### 6. _AbiStruct (Composte)
- Represents a struct in an ABI.
- Attributes:
  - name: primitives.String
  - base: primitives.String
  - fields: Array (an array of `_AbiStructsField`)
- Methods:
  - from_dict(cls, d: dict): Create an _AbiStruct object from a dictionary.

### 7. _AbiAction (Composte)
- Represents an action in an ABI.
- Attributes:
  - name: primitives.Name
  - type_: primitives.String
  - ricardian_contract: primitives.String
- Methods:
  - from_dict(cls, d: dict): Create an _AbiAction object from a dictionary.

### 8. _AbiTable (Composte)
- Represents a table in an ABI.
- Attributes:
  - name: primitives.Name
  - index_type: primitives.String
  - key_names: Array
  - key_types: Array
  - type_: primitives.String
- Methods:
  - from_dict(cls, d: dict): Create an _AbiTable object from a dictionary.

## Helper Functions

- _load_bin_from_file(file: Path, extension: str)
  - Load binary content from a given file or a zipped file.

- _bin_to_hex(bin: bytes) -> str
  - Convert binary data to hexadecimal.

- _hex_to_uint8_array(hex_string: str) -> Array
  - Convert a hexadecimal string to an array of uint8 values.

- _uint8_list_to_hex(uint8_list: list) -> str
  - Convert a list of uint8 values to a hexadecimal string.

- _hex_to_bin(hexcode: str) -> bytes
  - Convert a hexadecimal string back to binary.

`


# Transaction, Authorization, and Action Classes Interface

This Python interface defines the classes used to manage transactions, authorizations, and actions for the Antelope blockchain. These classes allow for the creation, manipulation, and linking of blockchain actions and transactions, as well as signing and sending transactions.



## Key Classes

### 1. Authorization
- Represents an authorization to be used in an action.
- **Attributes**:
  - `actor: str`: Actor's account name, must be between 1 and 13 characters.
  - `permission: str`: Permission level, must be between 1 and 13 characters.
- **Methods**:
  - `__bytes__()`: Convert the authorization to bytes representation.

### 2. Data
- Represents data to be used in actions.
- **Attributes**:
  - `name: str`: The data field name.
  - `value: types.AntelopeType`: The typed value of the data.
- **Methods**:
  - `parse_obj(obj)`: Parse an object into `Data` format.
  - `dict()`: Convert the `Data` object to a dictionary.
  - `json()`: Convert the `Data` object to a JSON string.
  - `__bytes__()`: Convert the `Data` object to bytes representation.

### 3. Action
- Represents an action to be used in a transaction.
- **Attributes**:
  - `account: str`: Account name associated with the action, max length of 13.
  - `name: str`: Action name.
  - `authorization: List[Authorization]`: List of authorizations, between 1 and 10.
  - `data: List[Data]`: List of data fields.
- **Methods**:
  - `link(net: Net)`: Return a `LinkedAction` with current values and a specified network.
  - `__bytes__()`: Raises `TypeError` when trying to convert an `Action` to bytes.

### 4. LinkedAction
- Represents an action linked to a specific network.
- **Attributes**:
  - Inherits all attributes from `Action`.
  - `net: Net`: The network to which the action is linked.
- **Methods**:
  - `__bytes__()`: Convert the `LinkedAction` to bytes representation.

### 5. Transaction
- Represents a raw transaction, which cannot be sent to the blockchain until linked to a network.
- **Attributes**:
  - `actions: List[Action]`: List of actions, between 1 and 10.
  - `expiration_delay_sec: int`: Expiration delay in seconds, default is 600.
  - `delay_sec: int`: Delay in seconds.
  - `max_cpu_usage_ms: int`: Maximum CPU usage in milliseconds.
  - `max_net_usage_words: int`: Maximum network usage in words.
- **Methods**:
  - `link(net: Net)`: Link the transaction to a specified network, creating a `LinkedTransaction`.

### 6. LinkedTransaction
- Represents a transaction linked to a network.
- **Attributes**:
  - Inherits all attributes from `Transaction`.
  - `net: Net`: The network to which the transaction is linked.
  - `chain_id: str`: The blockchain chain ID.
  - `ref_block_num: str`: Reference block number.
  - `ref_block_prefix: str`: Reference block prefix.
  - `expiration: dt.datetime`: Expiration time of the transaction.
- **Methods**:
  - `__bytes__()`: Convert the `LinkedTransaction` to bytes representation.
  - `id()`: Generate a unique ID for the transaction.
  - `sign(key: str)`: Sign the transaction with a given key, returning a `SignedTransaction`.

### 7. SignedTransaction
- Represents a signed transaction that can be sent to the blockchain.
- **Attributes**:
  - Inherits all attributes from `LinkedTransaction`.
  - `signatures: List[str]`: List of transaction signatures, between 1 and 10.
- **Methods**:
  - `pack()`: Pack the transaction into a hexadecimal string.
  - `send()`: Send the transaction to the blockchain network.

## Helper Functions

- **_endian_reverse_u32(i: int) -> int**
  - Reverse the endianness of a 32-bit integer.

- **_get_tapos_info(block_id: str) -> Tuple[int]**
  - Retrieve TAPOS (Transaction as Proof-of-Stake) information from the block ID.
