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

## Neo Test Runner

### Downloading

Install [Neo-Express](https://github.com/neo-project/neo-express#installation) and [Neo Test Runner](https://github.com/ngdenterprise/neo-test#neo-test-runner).

### Testing

Before writing your tests, make sure you have a Neo-Express network for local tests.
If you do not yet have a local network, open a terminal and run `neoxp create`.
Please refer to [Neo-Express documentation](https://github.com/neo-project/neo-express/blob/master/docs/command-reference.md#neoxp-create)
for more details of how to configure your local network. 

Create a Python Script, import the NeoTestRunner class, and define a function to test your smart contract. In this
function you'll need a NeoTestRunner object, which takes the path of your Neo-Express network configuration file as an
argument to set up the test environment.

You'll have to call the method `call_contract()` to interact with your smart contract. Its parameters are the path of
the compiled smart contract, the smart contract's method, and the arguments if necessary. 
This call doesn't return the result directly, but includes it in a queue of invocations. To execute all the invocations
set up, call the method `execute()`. Then assert the result of your invoke to see if it's correct.

Note that `invoke.result` won't be set if the execution fails, so you should also assert if `runner.vm_state` is valid 
for your test case.

Your Python Script should look something like this:

```python
from boa3.builtin.interop.blockchain.vmstate import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner


def test_hello_world_main():
    neoxp_config_file = '{path-to-neo-express-config-file}'
    project_root_folder = '{path-to-project-root-folder}'
    path = f'{project_root_folder}/boa3_test/examples/hello_world.nef'
    runner = NeoTestRunner(neoxp_config_file)

    invoke = runner.call_contract(path, 'main')
    runner.execute()
    assert runner.vm_state is VMState.HALT
    assert invoke.result is None
```

Alternatively you can change the value of `env.NEO_EXPRESS_INSTANCE_DIRECTORY` to the path of your .neo-express 
data file:

```python
from boa3.builtin.interop.blockchain.vmstate import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner
from boa3.internal import env

env.NEO_EXPRESS_INSTANCE_DIRECTORY = '{path-to-neo-express-config-file}'


def test_hello_world_main():
    root_folder = '{path-to-project-root-folder}'
    path = f'{root_folder}/boa3_test/examples/hello_world.nef'
    runner = NeoTestRunner()  # the default path to the Neo-Express is the one on env.NEO_EXPRESS_INSTANCE_DIRECTORY

    invoke = runner.call_contract(path, 'main')
    runner.execute()
    assert runner.vm_state is VMState.HALT
    assert invoke.result is None
```

