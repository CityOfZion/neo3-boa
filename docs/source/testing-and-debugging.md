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
example, we are testing the "Transfer" event, so we can use the `Nep17TransferEvent` class from `boaconstructor`. If you
plan to test other events, it's best you also create a class or method that will help you unwrap the stack results. 
Check out [`Nep17TransferEvent`](https://github.com/CityOfZion/boa-test-constructor/blob/20a45755767b3d919bf7a594cfff6bff78cb72ac/boaconstructor/__init__.py#L302-L314)
implementation for reference.

```python
    # inside the HelloWorldWithDeployTest class
    async def test_gas_transfer_event(self):
        # the amount of GAS tokens to transfer, since we will be invoking the transfer method, it's necessary to multiply by the decimals 
        amount = 1 * 10**8
        # calling the transfer method to emit a 'Transfer' event
        result, notifications = await self.call(
            "transfer", [self.user1.script_hash, self.genesis.script_hash, amount, None],
            return_type=bool, target_contract=GAS, signing_accounts=[self.user1]
        )
        self.assertEqual(True, result)
        self.assertEqual(1, len(notifications))
        self.assertEqual("Transfer", notifications[0].event_name)

        from boaconstructor import Nep17TransferEvent
        # we can use the Nep17TransferEvent class to unwrap the stack items
        transfer_event = Nep17TransferEvent.from_notification(notifications[0])
        self.assertEqual(self.user1.script_hash, transfer_event.source)
        self.assertEqual(self.genesis.script_hash, transfer_event.destination)
        self.assertEqual(amount, transfer_event.amount)
```
