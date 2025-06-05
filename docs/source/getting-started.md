# Getting Started

Check out our [GitHub README page](https://github.com/CityOfZion/neo3-boa/tree/master#quickstart) to see how you can 
install Neo3-Boa.

## Writing a smart contract
It's pretty easy to write a Python3 script with Neo3-Boa, since it is compatible with a lot of Python features. However,
there are some key differences that you should be aware of, here's the 4 most prominent ones:
- there is no floating point arithmetic, only the `int` type is implemented;
- you need to specify a function's return type and parameter types;
- if you want to call other smart contracts, you can only call public functions;
- to interact with the Neo blockchain, you need to use a function, variable, or class inside the `boa3.builtin` package.


### Hello World
Let's write a quick Hello World script that has a method that will save `"Hello World"` on the blockchain 
and another method that will return the string.

Those 2 functions will need to be callable and will also need to change the values inside the storage, 
so let's import both the `public` decorator and the `storage` package.

```python
# hello_world.py
from boa3.sc.compiletime import public
from boa3.sc import storage


@public  # the public decorator will make this method callable
def save_hello_world():  # an empty return type indicates that the return is None
    storage.put_str(b"first script",
                    "Hello World")  # the put method will store the "Hello World" value with the "first script" key


@public  # the public decorator will make this method callable too
def get_hello_world() -> str:  # this method will return a string, so it needs to specify it
    return storage.get_str(b"first script")  # the get method will return the value associated with "first script" key
```

### Neo Methods
Neo currently has 2 special methods: `_deploy` and `verify`:

```python
from typing import Any
from boa3.sc.compiletime import public


@public
def _deploy(data: Any, update: bool):
    """
    This method will automatically be called when the smart contract is deployed or updated.
    """
    pass


@public
def verify() -> bool:
    """
    When this contract address is included in the transaction signature,
    this method will be triggered as a VerificationTrigger to verify that the signature is correct.
    For example, this method needs to be called when withdrawing token from the contract.

    :return: whether the transaction signature is correct
    """
    pass
```

So, using the example above, if you want to set the `"Hello World"` message when you deploy your smart contract and have
another method to save a given string you could do the following:

```python
# hello_world_with_deploy.py
from typing import Any

from boa3.sc.compiletime import public
from boa3.sc import storage


@public
def _deploy(data: Any, update: bool):  # the _deploy function needs to have this signature
    storage.put_str(b"second script",
                    "Hello World")  # "Hello World" will be stored when this smart contract is deployed


@public
def get_message() -> str:  # this method will still try to get the value saved on the blockchain
    return storage.get_str(b"second script")


@public
def set_message(new_message: str):  # now this method will overwrite a new string on the blockchain
    storage.put_str(b"second script", new_message)
```

### How to make a Token smart contract
For a smart contract to be a fungible token on the Neo blockchain, it needs to adhere to the [NEP-17](https://docs.neo.org/docs/en-us/develop/write/nep17.html) standard, which requires the implementation of a few specific methods:
- `symbol` - Returns the symbol of the token.
- `decimals` - Returns the number of decimals used by the token.
- `totalSupply` - Returns the total supply of the token.
- `balanceOf` - Returns the balance of the specified account.
- `transfer` - Transfers tokens from one account to another.

And must also implement and trigger a `Transfer` event whenever tokens are transferred, minted or burned. 

Here's a [simple example](../../boa3_test/examples/simple_nep17.py) of a Token contract following the NEP-17 standard.
>Note: The NEP-17 standard also has requirements on how each method must be implemented. Be sure to check the [full documentation](https://docs.neo.org/docs/en-us/develop/write/nep17.html) on the NEP-17 standard to ensure the implementation is correct.

### How to make a Non-Fungible (NFT) Token smart contract
Just like the fungible token, for a contract to be a non-fungible token (NFT) in the Neo blockchain, it needs to adhere to the [NEP-11](https://docs.neo.org/docs/en-us/develop/write/nep11.html) standard by implementing a few methods and events:
- `symbol` - Returns the symbol of the token.
- `decimals` - Returns the number of decimals used by the token.
- `totalSupply` - Returns the total supply of the token.
- `tokensOf` = Returns the IDs of all NFTs owned by the specified account.

In addition, an NFT contract may be either *non-divisible* or *divisible*. The remaining methods have the same name, but different **signatures** for each, and different returns:
- For **non-divisible** NFT contracts:
  - `balanceOf` - Returns the total amount of NFTs of the specified account.
  - `transfer` - Transfers tokens to a specified account.
  - `ownerOf` - Returns the address of the owner of a specified NFT ID.

- For **divisible** NFT contracts:
  - `balanceOf` - Returns the amount of NFTs of the specified NFT ID for the specified account.
  - `transfer` - Transfers tokens to from a specified account to another.
  - `ownerOf` - Returns the addresses of all co-owners of a specified NFT ID.

In both cases, the contract must also implement and trigger a `Transfer` event whenever tokens are transferred. 

>Note: Although many methods and events have the same name as the NEP-17 standard, their implementation and parameters may differ.

Here's a [full example](../../boa3_test/examples/nep11_non_divisible.py) of a non-divisible token contract following the NEP-11 standard.
>Note: The example above is rather complete and contains more than just the basic implementation of a NEP-11 contract. Once again, be sure to check the [full documentation](https://docs.neo.org/docs/en-us/develop/write/nep11.html) on the NEP-11 standard to ensure the implementation is correct.

### How to receive tokens
Any smart contract can receive tokens. To do so, the smart contract must implement a method to be used as callback by the token contract:
- If the token being received is a fungible token, then the token contract adheres to the NEP-17 standard
  - In this case, the method `onNEP17Payment` must be implemented
- If the token being received is a non-fungible token, then the token contract adheres to the NEP-11 standard
  - In this case, the method `onNEP11Payment` must be implemented
>Note: A contract **does not** need to adhere to the NEP-11 or NEP-17 standards to **receive** tokens, fungible or not. It needs only to implement the methods used as callbacks for each type of token it wishes to receive.

We can then modify our `Hello World` example to be able to receive fungible and non-fungible tokens:
```python
# hello_world_receiving_tokens.py
from typing import Any

from boa3.sc import runtime, storage
from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import UInt160
from boa3.sc.utils import abort

@public
def _deploy(data: Any, update: bool):
    storage.put_str(b"second script",
                    "Hello World")


@public
def get_message() -> str:
    return storage.get_str(b"second script")


@public
def set_message(new_message: str):
    storage.put_str(b"second script", new_message)


# This method MUST be in camel case, either directly or renamed with the decorator parameter `name`
# This callback is called every time a fungible token is transferred to this contract
@public(name="onNEP17Payment")
def on_nep17_payment(from_address: UInt160, amount: int, data: Any):
    if runtime.calling_script_hash == NeoToken.hash: #  Check if the token contract calling this callback is the Neo token
        storage.put_bool(b"has_received_neo", True)
    else:
        # We MUST abort the method if this contract is not accepting any other type of token
        abort()


# This method MUST be in camel case, either directly or renamed with the decorator parameter `name`
# This callback is called every time a non-fungible token is transferred to this contract
@public(name="onNEP11Payment")
def on_nep11_payment(from_address: UInt160, amount: int, token_id: bytes, data: Any):
    #  Check if the NFT contract calling this callback is "my NFT" contract hash
    if runtime.calling_script_hash == UInt160(b"my_nft_contract_hash"):
        storage.put_bool(b"has_received_nft", True)
    else:
        # We MUST abort the method if this contract is not accepting any other type of NFT    
        abort()

```

## Compiling your Smart Contract

### Using CLI

```shell
$ neo3-boa compile path/to/your/file.py
```

> Note: When resolving compilation errors it is recommended to resolve the first reported error and try to compile again. An error can have a cascading effect and throw more errors all caused by the first.

### Using Python Script

```python
from boa3.boa3 import Boa3

Boa3.compile_and_save('path/to/your/file.py')
```

## Reference Examples and Tutorials

Check out [Neo3-boa tutorials](https://developers.neo.org/tutorials/tags/neo-3-boa) on [Neo Developer](https://developers.neo.org/).

For an extensive collection of examples:
- [Smart contract examples](https://github.com/CityOfZion/neo3-boa/tree/master/boa3_test/examples)
- [Features tests](https://github.com/CityOfZion/neo3-boa/tree/master/boa3_test/test_sc)


For reference of boa3 smart contract package utilities, take a look at [Package Reference](https://dojo.coz.io/neo3/boa/auto-package/package-reference.html) from boa3 documentation


## What's next
- [Testing and debugging your smart contract](./testing-and-debugging.md)
- [How to call other smart contracts on the blockchain](./calling-smart-contracts.md)
- [Invoking smart contracts with NeoNova](./invoking-with-neonova.md)
