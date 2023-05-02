<p align="center">
  <img
    src="/.github/resources/images/logo.png"
    width="200px;">
</p>

<p align="center">
  Write smart contracts for Neo3 in Python 
  <br/> Made by <b>COZ.IO</b>
</p>

<p align="center">  <a href="https://github.com/CityOfZion/neo3-boa"><strong>Neo3-boa</strong></a> · <a href="https://github.com/CityOfZion/neo-mamba">neo-mamba</a>  </p>

<p align="center">
  <a href="https://circleci.com/gh/CityOfZion/neo3-boa/tree/master">
    <img src="https://circleci.com/gh/CityOfZion/neo3-boa.svg?style=shield" alt="CircleCI.">
  </a>
  <a href='https://coveralls.io/github/CityOfZion/neo3-boa?branch=master'>
    <img src='https://coveralls.io/repos/github/CityOfZion/neo3-boa/badge.svg?branch=master' alt='Coverage Status' />
  </a>
  <a href="https://pypi.org/project/neo3-boa/">
    <img src="https://img.shields.io/pypi/v/neo3-boa.svg" alt="PyPI.">
  </a>
  <a href="https://opensource.org/licenses/Apache-2.0">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Licence.">
  </a>
</p>

<br/>

> Note: The latest release (v0.14.0) has breaking changes with contracts written using previous versions. Please refer to our [migration guide](/docs/migration-guide-v0.14.0.md) to update your smart contracts.

## Table of Contents
- [Overview](#overview)
- [Quickstart](#quickstart)
  - [Installation](#installation)
    - [Pip (Recommended)](#pip-recommended)
    - [Build from Source (Optional)](#build-from-source-optional)
  - [Compiling your Smart Contract](#compiling-your-smart-contract)
    - [Using CLI](#using-cli)
    - [Using Python Script](#using-python-script)
  - [Configuring the Debugger](#configuring-the-debugger)
  - [Neo Test Runner](#neo-test-runner)
    - [Downloading](#downloading)
    - [Testing](#testing)
- [Docs](#docs)
- [Reference Examples](#reference-examples)
- [Python Supported Features](#python-supported-features)
- [Neo Python Suite Projects](#neo-python-suite-projects)
- [Contributing](#contributing)
- [License](#license)

## Overview

Neo3-boa is a tool for creating Neo Smart Contracts using Python. It compiles `.py` files to `.nef` and `.manifest.json` formats for usage in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm/) which is used to execute contracts on the [Neo Blockchain](https://github.com/neo-project/neo/).

Neo3-boa is part of the Neo Python Framework, aimed to allow the full development of dApps using Python alone.

## Quickstart

Installation requires Python 3.7 or later.

### Installation

##### Make a Python 3 virtual environment and activate it:

On Linux / Mac OS:
```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

On Windows:

```shell
$ python3 -m venv venv
$ venv\Scripts\activate.bat
```

##### Pip (Recommended)

###### Install Neo3-boa using Pip:

```shell
$ pip install neo3-boa
```

##### Build from Source (Optional)
If Neo3-boa is not available via pip, you can run it from source.

###### Clone Neo3-boa:
```shell
$ git clone https://github.com/CityOfZion/neo3-boa.git
```
###### Install project dependencies:
```shell
$ pip install wheel
$ pip install -e .
```

### Compiling your Smart Contract

#### Using CLI

```shell
$ neo3-boa path/to/your/file.py
```

<br/>

> Note: When resolving compilation errors it is recommended to resolve the first reported error and try to compile again. An error can have a cascading effect and throw more errors all caused by the first.

#### Using Python Script

```python
from boa3.boa3 import Boa3

Boa3.compile_and_save('path/to/your/file.py')
```

### Configuring the Debugger
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

#### Using CLI

```shell
$ neo3-boa path/to/your/file.py -d|--debug
```

#### Using Python Script

```python
from boa3.boa3 import Boa3

Boa3.compile_and_save('path/to/your/file.py', debug=True)
```


### Neo Test Runner

#### Downloading

Install [Neo-Express](https://github.com/neo-project/neo-express#neo-express-and-neo-trace) and [Neo Test Runner](https://github.com/ngdenterprise/neo-test#neo-test-runner).

```shell
$ dotnet tool install Neo.Express
$ dotnet tool install Neo.Test.Runner
```

#### Testing

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

    invoke = runner.call_contract(path, 'Main')
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

    invoke = runner.call_contract(path, 'Main')
    runner.execute()
    assert invoke.result is None
```

## Docs
You can [read the docs here](https://docs.coz.io/neo3/boa/index.html). Please check our examples for reference.

## Reference Examples

For an extensive collection of examples:
- [Smart contract examples](/boa3_test/examples)
- [Features tests](/boa3_test/test_sc)

## Tests

This project uses Neo Test Runner and Neo-Express to test its features. To run all tests run the python
script at boa3_test/tests/run_unit_tests.py

> Note: If you don't want to use the Neo-Express instance on boa3_test/tests, you can change the path of this constant
> [here](/boa3/internal/env.py). However, your Neo-Express instance will need to have the following accounts: "owner", 
> "testAccount1", "testAccount2" and "testAccount3".

## Python Supported Features

<table>
  <thead>
    <tr>
      <td><b>Status</b></td>
      <td><b>Release</b></td>
      <td><b>Converts</b></td>
      <td><b>Example Code</b></td>
      <td><b>Contract Example Test</b></td>
    </tr>
  </thead>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Local variable declarations and assignments</td>
    <td>
      <pre>
        <code>
  def func():
    foo: int = 42
    bar = foo
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#local-variable-declarations-and-assignments">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Global variable declarations and assignments</td>
    <td>
      <pre>
        <code>
  foo: int = 42
  bar = foo
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#global-variable-declarations-and-assignments">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.4</td>
    <td>Global keyword</td>
    <td>
      <pre>
        <code>
  foo: int = 42
  bar = foo
        </code>
        <code>
  def func():
    global foo
    foo = 1
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#global-keyword">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Arithmetic operations</td>
    <td>
      <pre>
        <code>
  +, -, *, //, %
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#arithmetic-operations">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.8</td>
    <td>Arithmetic operations</td>
    <td>
      <pre>
        <code>
  **
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#arithmetic-operations-1">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>🔜</td>
    <td>backlog</td>
    <td>Arithmetic operations</td>
    <td>
      <pre>
        <code>
  /
        </code>
      </pre>
    </td>
    <td>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Arithmetic augmented assignment operators</td>
    <td>
      <pre>
        <code>
  +=, -=, *=, //=, %=
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#arithmetic-augmented-assignment-operators">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.8</td>
    <td>Arithmetic augmented assignment operators</td>
    <td>
      <pre>
        <code>
  **=
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#arithmetic-augmented-assignment-operators-1">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>🔜</td>
    <td>backlog</td>
    <td>Arithmetic augmented assignment operators</td>
    <td>
      <pre>
        <code>
  /=
        </code>
      </pre>
    </td>
    <td>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Relational operations</td>
    <td>
      <pre>
        <code>
  ==, !=, <, <=, >, >=, 
  is None, is not None
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#relational-operations">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.8.3</td>
    <td>Relational operations</td>
    <td>
      <pre>
        <code>
  is, is not
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#relational-operations-1">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Bitwise operations</td>
    <td>
      <pre>
        <code>
  &, |, ~, ^, <<, >>
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#bitwise-operations">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.8.3</td>
    <td>Bitwise augmented assignment operators</td>
    <td>
      <pre>
        <code>
  &=, |=, ~=, ^=, <<=, >>=
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#bitwise-augmented-assignment-operators">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Boolean logic operations</td>
    <td>
      <pre>
        <code>
  and, or, not
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#boolean-logic-operations">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Tuple type</td>
    <td>
      <pre>
        <code>
  a = ('1', '2', '3')
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#tuple-type">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>List type</td>
    <td>
      <pre>
        <code>
  a = ['1', '2', '3']
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#list-type">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.4</td>
    <td>List type</td>
    <td>
      <pre>
        <code>
  a.pop()
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#list-type-1">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.7</td>
    <td>List type</td>
    <td>
      <pre>
        <code>
  a.remove(1)
  a.insert('example', 2)
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#list-type-2">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Dict type</td>
    <td>
      <pre>
        <code>
  a = {1:'1', 2:'2', 3:'3'}
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#dict-type">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>🔜</td>
    <td>backlog</td>
    <td>Set type</td>
    <td>
      <pre>
        <code>
  a = {'1', '2', '3'}
        </code>
      </pre>
    </td>
    <td>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Bytes type</td>
    <td>
      <pre>
        <code>
  a = b'\x01\x02\x03\x04'
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#bytes-type">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Bytearray type</td>
    <td>
      <pre>
        <code>
  a = bytearray(b'\x01\x02\x03\x04')
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#bytearray-type">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.8.2</td>
    <td>Optional type</td>
    <td>
      <pre>
        <code>
  a: Optional[int] = 5
  a = 142
  a = None
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#optional-type">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.6.1</td>
    <td>Union type</td>
    <td>
      <pre>
        <code>
  a: Union[int, str] = 5
  a = 142
  a = 'example'
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#union-type">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>While statement</td>
    <td>
      <pre>
        <code>
  foo = 0
  while condition:
    foo = foo + 2
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#while-statement">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>If, elif, else statements</td>
    <td>
      <pre>
        <code>
  if condition1:
    foo = 0
  elif condition2:
    foo = 1
  else:
    bar = 2
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#if-elif-else-statements">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>For statement</td>
    <td>
      <pre>
        <code>
  for x in (1, 2, 3):
    ...
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#for-statement">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Function call</td>
    <td>
      <pre>
        <code>
  def Main(num: int):
    a = foo(num)
    ...
        </code>
        <code>
  def foo(num: int) -> int:
    ...
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#function-call">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Built in function</td>
    <td>
      <pre>
        <code>
  a = len('hello')
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#built-in-function">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.4</td>
    <td>Built in function</td>
    <td>
      <pre>
        <code>
  a = range(1, 5, 2)
  b = isinstance(5, str)
  print(42)
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#built-in-function-1">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.7</td>
    <td>Built in function</td>
    <td>
      <pre>
        <code>
  a = max(7, 12)
  b = min(1, 6)
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#built-in-function-2">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.8</td>
    <td>Built in function</td>
    <td>
      <pre>
        <code>
  a = abs(-5)
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#built-in-function-3">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.8.1</td>
    <td>Built in function</td>
    <td>
      <pre>
        <code>
  a = sum(list_of_num, 0)
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#built-in-function-4">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.8.3</td>
    <td>Built in function</td>
    <td>
      <pre>
        <code>
  a = max(7, 0, 12, 8)
  b = min(1, 6, 2)
  c = reversed([1, 2, 3, 4])
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#built-in-function-6">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.11.0</td>
    <td>Built in function</td>
    <td>
      <pre>
        <code>
  a = pow(2, 2)
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#built-in-function-7">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Multiple expressions in the same line</td>
    <td>
      <pre>
        <code>
  i = i + h; a = 1; b = 3 + a; count = 0
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#multiple-expressions-in-the-same-line">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.4</td>
    <td>Chained assignment</td>
    <td>
      <pre>
        <code>
  x = y = foo()
        </code>
      </pre>
    </td>
    <td>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Sequence slicing</td>
    <td>
      <pre>
        <code>
  x = 'example'[2:4]
  x = [1, 2, 3][:2]
  x = 'example'[4:]
  x = (1, 2, 3)[:]
  x = 'example'[-4:-2]
  x = 'example'[:-4]
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#sequence-slicing">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.10.0</td>
    <td>Sequence slicing</td>
    <td>
      <pre>
        <code>
  x = 'example'[2:4:2]
  x = 'example'[::2]
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#sequence-slicing-1">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Assert</td>
    <td>
      <pre>
        <code>
  assert x % 2 == 0
  assert x % 3 != 2, 'error message'
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#assert">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.4</td>
    <td>Try except</td>
    <td>
      <pre>
        <code>
  try:
    a = foo(b)
  except Exception as e:
    a = foo(b)
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#try-except">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.5</td>
    <td>Try except with finally</td>
    <td>
      <pre>
        <code>
  try:
    a = foo(b)
  except Exception as e:
    a = zubs(b)
  finally:
    b = zubs(a)
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#try-except-with-finally">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.4</td>
    <td>Continue, break</td>
    <td>
    </td>
    <td>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.11.2</td>
    <td>Pass</td>
    <td>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#pass-keyword">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Import</td>
    <td>Support to <code>boa3.builtin</code> packages.</td>
    <td>
      <a href="/docs/ContractExamplesTest.md#import">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.8.3</td>
    <td>Import</td>
    <td>Support to user created modules.</td>
    <td>
      <a href="/docs/ContractExamplesTest.md#import-2">List of examples</a>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.10.0</td>
    <td>Class</td>
    <td>
      <pre>
        <code>
  class Foo:
    def __init__(self, bar: Any):
      pass
        </code>
      </pre>
    </td>
    <td>
      <a href="/docs/ContractExamplesTest.md#user-created-classes">List of examples</a>
    </td>
  </tbody>
</table>


## Neo Python Suite Projects

- **[Neo3-boa](https://github.com/CityOfZion/neo3-boa)**: Python smart contracts' compiler.
- [neo3-mamba](https://github.com/CityOfZion/neo-mamba): Python SDK for interacting with Neo.

## Contributing

Checkout our [contributing file](CONTRIBUTING.md) to see how you can contribute with our project.

## License

- Open-source [Apache 2.0](https://github.com/CityOfZion/neo3-boa/blob/master/LICENSE).
