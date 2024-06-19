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

Here's a [simple example](https://github.com/CityOfZion/neo3-boa/blob/development/boa3_test/examples/simple_nep17.py) of a Token contract following the NEP-17 standard.
>Note: The NEP-17 standard also has requirements on how each method must be implemented. Be sure to check the [full documentation](https://docs.neo.org/docs/en-us/develop/write/nep17.html) on the NEP-17 standard to ensure the implementation is correct.

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
- [Smart contract examples](https://github.com/CityOfZion/neo3-boa/blob/development/boa3_test/examples)
- [Features tests](https://github.com/CityOfZion/neo3-boa/blob/development/boa3_test/test_sc)

For reference of boa3 smart contract package utilities, take a look at [Package Reference](https://dojo.coz.io/neo3/boa/auto-package/package-reference.html) from boa3 documentation


## What's next
- [Testing and debugging your smart contract](./testing-and-debugging.md)
- [How to call other smart contracts on the blockchain](./calling-smart-contracts.md)
- [Invoking smart contracts with NeoNova](./invoking-with-neonova.md)
