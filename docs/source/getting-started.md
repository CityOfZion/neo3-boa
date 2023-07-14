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

### Overview of Neo3-Boa features

| Packages                                                                                                        | Contains:                                                                                                                                 | Important features                                                                                                                                                                                                                                                                                                                                                                               |
|-----------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [boa3.builtin](auto-package/boa3/builtin/boa3-builtins)                                                         | all packages below, it also contains an env variable that lets you change the value of a variable when compiling the smart contract.      | {data}`env <boa3.builtin.env>`                                                                                                                                                                                                                                                                                                                                                                   |
| [boa3.builtin.compile_time](auto-package/boa3/builtin/compile-time/boa3-builtin-compile-time)                   | methods and classes that are needed when you are compiling your smart contract, as opposed to when it's being executed on the blockchain. | {func}`public <boa3.builtin.compile_time.public>`, {func}`metadata <boa3.builtin.compile_time.metadata>`, {func}`contract <boa3.builtin.compile_time.contract>`, {func}`CreateNewEvent <boa3.builtin.compile_time.CreateNewEvent>`, {class}`NeoMetadata <boa3.builtin.compile_time.NeoMetadata>`                                                                                                 |
| [boa3.builtin.contract](auto-package/boa3/builtin/contract/boa3-builtin-contract)                               | events and methods that might help when writing something specific about Neo blockchain                                                   | {func}`abort <boa3.builtin.contract.abort>`, {data}`Nep17TransferEvent <boa3.builtin.contract.Nep17TransferEvent>`, {data}`Nep11TransferEvent <boa3.builtin.contract.Nep11TransferEvent>`                                                                                                                                                                                                        |
| [boa3.builtin.interop](auto-package/boa3/builtin/interop/boa3-builtin-interop)                                  | other packages that have a lot of helpful interoperable services. Has some overlap with the native contracts.                             | {mod}`storage <boa3.builtin.interop.storage>`, {mod}`runtime <boa3.builtin.interop.runtime>`, {mod}`contract <boa3.builtin.interop.contract>`, {mod}`blockchain <boa3.builtin.interop.blockchain>`                                                                                                                                                                                               |
| [boa3.builtin.interop.blockchain](auto-package/boa3/builtin/interop/blockchain/boa3-builtin-interop-blockchain) | features to get information on the Neo blockchain.                                                                                        | {data}`current_hash <boa3.builtin.interop.blockchain.current_hash>`, {func}`get_contract <boa3.builtin.interop.blockchain.get_contract>`, {class}`Transaction <boa3.builtin.interop.blockchain.transaction.Transaction>`                                                                                                                                                                         |
| [boa3.builtin.interop.contract](auto-package/boa3/builtin/interop/contract/boa3-builtin-interop-contract)       | features related to smart contracts.                                                                                                      | {func}`call_contract <boa3.builtin.interop.contract.call_contract>`, {func}`update_contract <boa3.builtin.interop.contract.update_contract>`, {class}`Contract <boa3.builtin.interop.contract.contract.Contract>`                                                                                                                                                                                |
| [boa3.builtin.interop.crypto](auto-package/boa3/builtin/interop/crypto/boa3-builtin-interop-crypto)             | features related to cryptography.                                                                                                         | {func}`sha256 <boa3.builtin.interop.crypto.sha256>`, {func}`hash160 <boa3.builtin.interop.crypto.hash160>`, {func}`hash256 <boa3.builtin.interop.crypto.hash256>`, {func}`check_sig <boa3.builtin.interop.crypto.check_sig>`                                                                                                                                                                     |
| [boa3.builtin.interop.iterator](auto-package/boa3/builtin/interop/iterator/boa3-builtin-interop-iterator)       | the iterator class.                                                                                                                       | {class}`Iterator <boa3.builtin.interop.iterator.Iterator>`                                                                                                                                                                                                                                                                                                                                       |
| [boa3.builtin.interop.json](auto-package/boa3/builtin/interop/json/boa3-builtin-interop-json)                   | methods to serialize and deserialize JSON.                                                                                                | {func}`json_serialize <boa3.builtin.interop.json.json_serialize>`, {func}`json_deserialize <boa3.builtin.interop.json.json_deserialize>`                                                                                                                                                                                                                                                         |
| [boa3.builtin.interop.oracle](auto-package/boa3/builtin/interop/oracle/boa3-builtin-interop-oracle)             | features related with Neo Oracle, it is used to get information from outside the blockchain.                                              | {class}`Oracle <boa3.builtin.nativecontract.oracle.Oracle>`                                                                                                                                                                                                                                                                                                                                      |
| [boa3.builtin.interop.policy](auto-package/boa3/builtin/interop/policy/boa3-builtin-interop-policy)             | features related to policies that affect the entire Neo blockchain.                                                                       | {func}`get_exec_fee_factor <boa3.builtin.interop.policy.get_exec_fee_factor>`, {func}`get_storage_price <boa3.builtin.interop.policy.get_storage_price>`                                                                                                                                                                                                                                         |
| [boa3.builtin.interop.role](auto-package/boa3/builtin/interop/role/boa3-builtin-interop-role)                   | methods to get information about the nodes on the blockchain.                                                                             | {func}`get_designated_by_role <boa3.builtin.interop.role.get_designated_by_role>`                                                                                                                                                                                                                                                                                                                |
| [boa3.builtin.interop.runtime](auto-package/boa3/builtin/interop/runtime/boa3-builtin-interop-runtime)          | features to get information that can only be acquired when running the smart contract.                                                    | {func}`check_witness <boa3.builtin.interop.runtime.check_witness>`, {func}`calling_script_hash <boa3.builtin.interop.runtime.calling_script_hash>`, {func}`executing_script_hash <boa3.builtin.interop.runtime.executing_script_hash>`, {func}`script_container <boa3.builtin.interop.runtime.script_container>`, {class}`Notification <boa3.builtin.interop.runtime.notification.Notification>` |
| [boa3.builtin.interop.stdlib](auto-package/boa3/builtin/interop/stdlib/boa3-builtin-interop-stdlib)             | methods that convert one data to another or methods that can check and compare memory.                                                    | {func}`serialize <boa3.builtin.interop.stdlib.serialize>`, {func}`deserialize <boa3.builtin.interop.stdlib.deserialize>`                                                                                                                                                                                                                                                                         |
| [boa3.builtin.interop.storage](auto-package/boa3/builtin/interop/storage/boa3-builtin-interop-storage)          | features to store, get, or change values inside the blockchain.                                                                           | {func}`get <boa3.builtin.interop.storage.get>`, {func}`put <boa3.builtin.interop.storage.put>`, {func}`find <boa3.builtin.interop.storage.find>`, {class}`FindOptions <boa3.builtin.interop.storage.findoptions.FindOptions>`                                                                                                                                                                    |
| [boa3.builtin.nativecontract](auto-package/boa3/builtin/nativecontract/boa3-builtin-nativecontract)             | classes that interface Neo's native contracts.                                                                                            | {class}`ContractManagement <boa3.builtin.nativecontract.contractmanagement.ContractManagement>`, {class}`GAS <boa3.builtin.nativecontract.gas.GAS>`, {class}`NEO <boa3.builtin.nativecontract.neo.NEO>`, {class}`StdLib <boa3.builtin.nativecontract.stdlib.StdLib>`                                                                                                                             |
| [boa3.builtin.type](auto-package/boa3/builtin/type/boa3-builtin-type)                                           | Neo types.                                                                                                                                | {class}`UInt160 <boa3.builtin.type.UInt160>`, {class}`UInt256 <boa3.builtin.type.UInt256>`, {class}`Event <boa3.builtin.type.Event>`, {class}`ECPoint <boa3.builtin.type.ECPoint>`                                                                                                                                                                                                               |
| [boa3.builtin.vm](auto-package/boa3/builtin/vm/boa3-builtin-vm)                                                 | Opcodes used internally by the Neo VM, used to create scripts dynamically.                                                                | {class}`Opcode <boa3.builtin.vm.Opcode>`                                                                                                                                                                                                                                                                                                                                                         |
| [boa3.builtin.math](auto-package/boa3/builtin/boa3-builtin-math)                                                | a small sample of functions similar to Python's math.                                                                                     | {func}`sqrt <boa3.builtin.math.sqrt>`, {func}`floor <boa3.builtin.math.floor>`, {func}`ceil <boa3.builtin.math.ceil>`                                                                                                                                                                                                                                                                            |


### Hello World
Let's write a quick Hello World script that has a method that will save `"Hello World"` on the blockchain 
and another method that will return the string.

Those 2 functions will need to be callable and will also need to change the values inside the storage, 
so let's import both the `public` decorator and the `storage` package.

```python
# hello_world.py
from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage


@public     # the public decorator will make this method callable
def save_hello_world():             # an empty return type indicates that the return is None
    storage.put(b"first script", "Hello World")      # the put method will store the "Hello World" value with the "first script" key


@public     # the public decorator will make this method callable too
def get_hello_world() -> str:       # this method will return a string, so it needs to specify it
    return str(storage.get(b"first script"))              # the get method will return the value associated with "first script" key
```

### Neo Methods
Neo currently has 2 special methods: `_deploy` and `verify`:

```python
from typing import Any
from boa3.builtin.compile_time import public

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

from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage


@public
def _deploy(data: Any, update: bool):               # the _deploy function needs to have this signature
    storage.put(b"second script", "Hello World")      # "Hello World" will be stored when this smart contract is deployed


@public
def get_message() -> str:                       # this method will still try to get the value saved on the blockchain
    return str(storage.get(b"second script"))            


@public
def set_message(new_message: str):              # now this method will overwrite a new string on the blockchain
    storage.put(b"second script", new_message)
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
- [Smart contract examples](https://github.com/CityOfZion/neo3-boa/blob/development/boa3_test/examples)
- [Features tests](https://github.com/CityOfZion/neo3-boa/blob/development/boa3_test/test_sc)


## What's next
- [Testing and debugging your smart contract](./testing-and-debugging.md)
- [How to call other smart contracts on the blockchain](./calling-smart-contracts.md)
- [Invoking smart contracts with NeoNova](./invoking-with-neonova.md)
