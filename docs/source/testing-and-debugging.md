# Testing and Debugging

## Configuring the Debugger
Neo3-Boa is compatible with the [Neo Debugger](https://github.com/neo-project/neo-debugger).
Debugger launch configuration example:
```
{
    //Launch configuration example for Neo3-Boa.
    //Make sure you compile your smart-contract before you try to debug it.
    "version": "0.2.0",
    "configurations": [
        {
            "name": "example.nef",
            "type": "neo-contract",
            "request": "launch",
            "program": "${workspaceFolder}\\example.nef",
            "operation": "main",
            "args": [],
            "storage": [],
            "runtime": {
                "witnesses": {
                    "check-result": true
                }
            }
        }
    ]
}
```

It's necessary to generate the nef debugger info file to use Neo Debugger.

### Using CLI

```shell
$ neo3-boa compile path/to/your/file.py -d|--debug
```

### Using Python Script

```python
from boa3.boa3 import Boa3

Boa3.compile_and_save('path/to/your/file.py', debug=True)
```

## boa test constructor

### Downloading

Install [boa-test-constructor](https://pypi.org/project/boa-test-constructor/) with pip by running:
```shell
$ pip install neo3-boa[test]
```
This will ensure that the boa-test-constructor version that will be installed is compatible with the latest version of 
neo3-boa.

We use this extension to run an isolated test environment for smart contracts with a neo-go node. When installing 
boa-test-constructor, [neo-mamba](https://dojo.coz.io/neo3/mamba/index.html) will be installed too.

### Testing

Create a Python Script, import the `SmartContractTestCase` class, and create a test class that inherits it. To set up
the test environment, you'll need to override the `setUpClass` method from `SmartContractTestCase`. This method is 
synchronous, so if you need to set up asynchronous tasks, like tasks that need to interact with the local blockchain,
then you can create another async method and use it int the `asyncio.run` method from `asyncio`. Common operations would
be: creating accounts, deploying the smart contract, selecting your "main" smart contract, and transferring GAS to the 
new accounts.

```python
import asyncio
from boaconstructor import SmartContractTestCase
from neo3.core import types
from neo3.wallet.account import Account
from neo3.contracts.contract import CONTRACT_HASHES

GAS = CONTRACT_HASHES.GAS_TOKEN

# the smart contract that will be tested is hello_world_with_deploy.py from the "Neo Methods" https://dojo.coz.io/neo3/boa/getting-started.html#neo-methods 
class HelloWorldWithDeployTest(SmartContractTestCase):
    genesis: Account
    user1: Account
    
    # if this variable is set, then this contract hash will be used whenever you don't specify which smart contract you'll want to invoke
    contract_hash: types.UInt160

    @classmethod
    def setUpClass(cls) -> None:
        # whenever a new test is run, the local blockchain will be reset, that's why we need to set up the environment again
        super().setUpClass()
        # you can name the account whatever you want, but the password needs to be "123"
        # this is a boa-test-constructor deliberate decision to make the tests run faster
        cls.user1 = cls.node.wallet.account_new(label="alice", password="123")
        cls.genesis = cls.node.wallet.account_get_by_label("committee")

        asyncio.run(cls.asyncSetupClass())

    @classmethod
    async def asyncSetupClass(cls) -> None:
        # this `transfer` method already uses the correct amount of decimals for the token
        await cls.transfer(GAS, cls.genesis.script_hash, cls.user1.script_hash, 100)
         
        cls.contract_hash = await cls.deploy("./hello_world_with_deploy.nef", cls.genesis)
```

Then, create functions to test the expected behavior of your smart contract. To invoke your smart contract, use the 
`call` method from `SmartContractTestCase`. The two positional parameters are the name of the method you want to invoke 
and a list of its arguments. The keyword parameters are the return type, a list of signing accounts, a list of signers, 
and the smart contract you want to invoke. Method name, and return type are obligatory, but you'll most likely also need
to pass the args too. If you get an error when calling a smart contract, then an error will be raised.

```python
    # inside the HelloWorldWithDeployTest class
    async def test_message(self):
        expected = "Hello World"
        result, _ = await self.call("get_message", return_type=str)
        self.assertEqual(expected, result)
```

To persist an invocation, use the `signing_accounts` parameter to pass a list of signing accounts when calling the 
smart contract. If you don't pass it, then it will always be a test invoke, meaning it won't be saved on the local 
blockchain. The `signers` parameter can be used alongside the `signing_accounts` if you want to change the 
[witness scope](https://developers.neo.org/docs/n3/foundation/Transactions#signature-scope) of the invocation, or by 
itself if you want to test invoke but also define the [signers](https://developers.neo.org/docs/n3/foundation/Transactions#signers)
of the transaction.

```python
        # continuation of the 'async def test_message(self)' function
        # to set this message in the smart contract, we need to pass the signing account
        new_message = "New Message"
        # since we want this change to persist, we need to pass the signing account
        result, _ = await self.call("set_message", [new_message], return_type=None,
                                    signing_accounts=[self.user1])
        self.assertIsNone(result)

        result, _ = await self.call("get_message", return_type=str)
        self.assertEqual(new_message, result)
```

#### Accessing Events

If you want to test events, you'll get all the notifications that were emitted on the transaction from the second return
value of the `call` method. The resulting stack of every notification is a list of stack items, so it's best you unwrap
them using [neo-mamba unwrapping methods](https://dojo.coz.io/neo3/mamba/api/neo3/api/helpers/unwrap.html). In this 
example, we are testing the "Transfer" event from the GAS token smart contract, so we can create a `Nep17TransferEvent` 
class that is compliant with the event being emitted. If you plan to test other events, it's best you also create a 
class or method that will help you unwrap the stack results.

```python
    # inside the HelloWorldWithDeployTest class
    async def test_gas_transfer_event(self):
        from dataclasses import dataclass
        from neo3.api import noderpc, StackItemType

        # the dataclass decorator will automatically generate the __init__ method among other things
        @dataclass
        class Nep17TransferEvent:
            # the Transfer event has 3 parameters: from, to, and amount
            from_script_hash: types.UInt160 | None
            to_script_hash: types.UInt160 | None
            amount: int

            @classmethod
            def from_notification(cls, n: noderpc.Notification):
                stack = n.state.as_list()
                from_script_hash = stack[0].as_uint160() if not stack[0].type == StackItemType.ANY else None
                to_script_hash = stack[1].as_uint160() if not stack[1].type == StackItemType.ANY else None
                amount = stack[2].as_int()
                return cls(from_script_hash, to_script_hash, amount)

        # the amount of GAS tokens to transfer, since we will be invoking the transfer method, it's necessary to multiply by the decimals
        amount_gas = 1 * 10 ** 8
        # calling the transfer method to emit a 'Transfer' event
        result, notifications = await self.call(
            "transfer", [self.user1.script_hash, self.genesis.script_hash, amount_gas, None],
            return_type=bool, target_contract=GAS, signing_accounts=[self.user1]
        )
        self.assertEqual(True, result)
        self.assertEqual(1, len(notifications))
        self.assertEqual("Transfer", notifications[0].event_name)

        # we can use the Nep17TransferEvent class to unwrap the stack items
        transfer_event = Nep17TransferEvent.from_notification(notifications[0])
        self.assertEqual(self.user1.script_hash, transfer_event.from_script_hash)
        self.assertEqual(self.genesis.script_hash, transfer_event.to_script_hash)
        self.assertEqual(amount_gas, transfer_event.amount)
```

#### Accessing the Storage

To get the key-value pairs stored in the smart contract's storage, you can use the `get_storage` method from 
`SmartContractTestCase`. Use it with the prefix of the keys you want to access, or without a prefix to get all key-value
pairs, and it will return a `dict[bytes, bytes]`. If you want to remove the prefix from the result you can use the 
`remove_prefix` parameter. 

If you want to convert those bytes values into another type, you can also pass a [`PostProcessor`](https://github.com/CityOfZion/boa-test-constructor/blob/20a45755767b3d919bf7a594cfff6bff78cb72ac/boaconstructor/storage.py#L13-L15)
as argument to process the keys and/or values before adding it to the dictionary. This `PostProcessor` needs to be an
object that when called will receive at least a `bytes` argument, in this case the key or value from the storage, and 
return this argument processed into another value. It can also receive other arguments that will help this process, but
this is optional, and currently it's not being used internally. For simpler cases, you can use the methods from
`boaconstructor.storage` that will process the most common types in Neo.

```python
    # inside the HelloWorldWithDeployTest class
    async def test_smart_contract_storage(self):
        from typing import cast

        # this function is implementing the PostProcessor pattern, and it's used to convert bytes to a string
        def bytes_to_str(data: bytes, *args) -> str:
            return data.decode("utf-8")

        # the return from the get_storage method is a `dict[bytes, bytes]`, but we are passing the bytes_to_str function
        # to convert the values to strings, so we should cast the return to `dict[bytes, str]` to avoid type warnings
        smart_contract_storage = cast(
            dict[bytes, str],
            await self.get_storage(
                # since we are not passing the prefix, it will get all key-value pairs from the smart contract storage
                values_post_processor=bytes_to_str
            )
        )

        # only the "Hello World" message is in this smart contract storage
        self.assertEqual(1, len(smart_contract_storage))
        self.assertIn(b"second script", smart_contract_storage)
        self.assertEqual("Hello World", smart_contract_storage[b"second script"])
```
