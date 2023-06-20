# Testing and Debugging

## Configuring the Debugger
Neo3-boa is compatible with the [Neo Debugger](https://github.com/neo-project/neo-debugger).
Debugger launch configuration example:
```
{
    //Launch configuration example for Neo3-boa.
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

Create a Python Script, import the NeoTestRunner class, and define a function to test your smart contract. In this 
function you'll need to call the method `call_contract()`. Its parameters are the path of the compiled smart contract, 
the smart contract's method, and the arguments if necessary. Then assert the result of your invoke to see if it's correct.

Your Python Script should look something like this:

```python
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner


def test_hello_world_main():
    neoxp_folder = '{path-to-neo-express-directory}'
    project_root_folder = '{path-to-project-root-folder}'
    path = f'{project_root_folder}/boa3_test/examples/hello_world.nef'
    runner = NeoTestRunner(neoxp_folder)

    invoke = runner.call_contract(path, 'main')
    runner.execute()
    assert invoke.result is None
```

Alternatively you can change the value of `boa3.env.NEO_EXPRESS_INSTANCE_DIRECTORY` to the path of your .neo-express 
data file:

```python
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner
from boa3.internal import env

env.NEO_EXPRESS_INSTANCE_DIRECTORY = '{path-to-neo-express-directory}'


def test_hello_world_main():
    root_folder = '{path-to-project-root-folder}'
    path = f'{root_folder}/boa3_test/examples/hello_world.nef'
    runner = NeoTestRunner()  # the default path to the Neo-Express is the one on env.NEO_EXPRESS_INSTANCE_DIRECTORY

    invoke = runner.call_contract(path, 'main')
    runner.execute()
    assert invoke.result is None
```

