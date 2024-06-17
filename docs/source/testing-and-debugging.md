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

Install [boa-test-constructor](https://pypi.org/project/boa-test-constructor/) with pip. We use this extension to run an isolated
test environment for smart contracts with a neo-go node. When installing boa-test-constructor, [neo-mamba](https://dojo.coz.io/neo3/mamba/index.html)
will be installed too.

### Testing

Create a Python Script, import the `SmartContractTestCase` class, and create a test class that inherits it. To set up
the test environment, you'll need to override the `setUpClass` method from `SmartContractTestCase`. This method is 
synchronous, so if you need to set up asynchronous tasks, you can create another async method and use it int the 
`asyncio.run` method from `asyncio`. Common operations would be: creating accounts, deploying the smart contract, 
selecting your "main" smart contract, and transferring GAS to the new accounts.

Then, create functions to test the expected behavior of your smart contract. To invoke or test invoke your smart 
contract, use the `call` method from `SmartContractTestCase`. The two positional parameters are the name of the method 
you want to invoke and a list of its arguments. The keyword parameters are the return type, a list of signing accounts,
a list of signers, and the smart contract you want to invoke. If you get an error when calling a smart contract, then an
error will be raised.

To persist an invocation, use the `signing_accounts` parameter to pass a list of signing accounts when calling the 
smart contract. If you don't pass it, then it will always be a test invoke. The `signers` parameter can be used 
alongside the `signing_accounts` if you want to change the witness scope of the invocation, or by itself if you want to
test invoke but also define the signers of the transaction.

Your Python Script should look something like this:

```python
import asyncio
from boaconstructor import SmartContractTestCase
from neo3.core import types
from neo3.wallet.account import Account
from neo3.contracts.contract import CONTRACT_HASHES

GAS = CONTRACT_HASHES.GAS_TOKEN

class SmartContractTest(SmartContractTestCase):
    genesis: Account
    user1: Account
    
    # if this variable is set, then this contract hash will be called whenever you don't use the `target_contract` parameter on the `call` method
    contract_hash: types.UInt160

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # you can name the account whatever you want, but the password needs to be "123"
        cls.user1 = cls.node.wallet.account_new("123", "alice")
        cls.genesis = cls.node.wallet.account_get_by_label("committee")

        asyncio.run(cls.asyncSetupClass())

    @classmethod
    async def asyncSetupClass(cls) -> None:
        # this `transfer` method already uses the correct amount of decimals for the token
        await cls.transfer(GAS, cls.genesis.script_hash, cls.user1.script_hash, 100)
        
        # the smart contract I'm deploying is hello_world_with_deploy.py from the "Neo Methods" https://dojo.coz.io/neo3/boa/getting-started.html#neo-methods 
        cls.contract_hash = await cls.deploy("./smart_contract.nef", cls.genesis)

    async def test_message(self):
        expected = "Hello World"
        result, _ = await self.call("get_message", return_type=str)
        self.assertEqual(expected, result)

        new_message = "New Message"
        # since we want this change to persist, we need to pass the signing account
        result, _ = await self.call("set_message", [new_message], return_type=None,
                                    signing_accounts=[self.user1])
        self.assertIsNone(result)

        result, _ = await self.call("get_message", return_type=str)
        self.assertEqual(new_message, result)
```
