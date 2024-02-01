# Calling smart contracts
Currently, there are 2 different ways to call another smart contract on the blockchain: using a `call_contract` method 
or using an interface, but internally they work both the same way.

Let us suppose the following contract was deployed on Neo:
```python
from boa3.builtin.compile_time import public


@public
def hello_stranger(name: str) -> str:               
    return "Hello " + name
```
To call the `hello_stranger` method, first you'll need to know the smart contract's [script hash](https://developers.neo.org/docs/n3/develop/deploy/deploy#the-contract-scripthash),
Let us also assume it is `0x000102030405060708090A0B0C0D0E0F10111213`.

## with call_contract
Use the `call_contract` method from `boa3.builtin.interop.contract` on your smart contract. You'll need to use the 
script hash, followed by the name of the function you want to call, followed by the arguments of said function. You'll 
also need to type cast the return so the compiler type checker works as expected, otherwise the return type will be 
considered as `Any`.
```python
# calling_with_call_contract.py
from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.type import UInt160

@public
def calling_other_contract() -> str:
    greetings: str = call_contract(UInt160(b'\x13\x12\x11\x10\x0F\x0E\x0D\x0C\x0B\x0A\x09\x08\x07\x06\x05\x04\x03\x02\x01\x00'),     # usually, script hashes that starts with "0x" means that they are using big endian, so when using `bytes` you'll need to revert the order
                                   'hello_stranger',     # it's the function's name
                                   'John Doe'            # the parameter of 'hello_stranger'
                                  )
    return greetings
```

> Note: If you are going to call a contract only once, then it's ok to use `call_contract`, however, it might be hard to 
keep track of a lot of `call_contract`s on the same file. It's pretty much always better to use an interface when dealing with other 
smart contracts.

## with Interface
Use the `contract` decorator from `boa3.builtin.compile_time` using the script hash and create a class that have the 
same methods you want call.
```python
# calling_with_interface.py
from boa3.builtin.compile_time import contract, public
from boa3.builtin.type import UInt160

@public
def calling_other_contract() -> str:
    greetings = HelloStrangerContract.hello_stranger('John Doe')
    return greetings


@contract('0x000102030405060708090A0B0C0D0E0F10111213')
class HelloStrangerContract:
    hash: UInt160   # this class variable will reflect the value you passed to the `contract` decorator
    
    @staticmethod
    def hello_stranger(name: str) -> str:
        pass

```

### Calling native contracts
Neo3-Boa already has interfaces for all the [native contracts](https://docs.neo.org/docs/en-us/reference/scapi/framework/native.html) 
that you can import from `boa3.builtin.nativecontract`
```python
# calling_native_contract.py
from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.neo import NEO

@public
def calling_other_contract() -> str:
    neo_symbol = NEO.symbol()
    return neo_symbol
```

### Automate with CPM
Instead of manually writing the smart contract interface, you can use [CPM](https://github.com/CityOfZion/cpm/tree/master#readme) 
to generate it automatically. After installing Neo3-Boa, you can install CPM by typing `install_cpm` on CLI (without the 
`neo3-boa` prefix). Then, you'll need to create a [cpm.yaml config file](https://github.com/CityOfZion/cpm/blob/master/docs/config.md), 
put the smart contract information there, and [run cpm](https://github.com/CityOfZion/cpm#example-commands).

For example, if you use CPM to create a [dice smart contract](https://dora.coz.io/contract/neo3/mainnet/0x4380f2c1de98bb267d3ea821897ec571a04fe3e0)
interface, the following file will be generated:
```python
# cpm_out/python/dice/contract.py
from boa3.builtin.type import UInt160, UInt256, ECPoint
from boa3.builtin.compile_time import contract, display_name
from typing import cast, Any


@contract('0x4380f2c1de98bb267d3ea821897ec571a04fe3e0')
class Dice:
    hash: UInt160

    @staticmethod
    def rand_between(start: int, end: int) -> int: 
        pass

    @staticmethod
    def map_bytes_onto_range(start: int, end: int, entropy: bytes) -> int: 
        pass

    @staticmethod
    def roll_die(die: str) -> int: 
        pass

    @staticmethod
    def roll_dice_with_entropy(die: str, precision: int, entropy: bytes) -> list: 
        pass

    @staticmethod
    def update(script: bytes, manifest: bytes, data: Any) -> None: 
        pass
```

Then, all you need to do is import this class onto your smart contract.
```python
# calling_with_cpm.py
from boa3.builtin.compile_time import public
from cpm_out.python.dice.contract import Dice


@public
def calling_other_contract() -> str:
    d6_roll = Dice.rand_between(1, 6)
    return "Dice result is " + str(d6_roll)
```
