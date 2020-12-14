<p align="center">
  <img
    src="/.github/resources/images/logo.png"
    width="200px;">
</p>

<p align="center">
  Write smart contracts for Neo3 in Python 
  <br/> Made by <b>COZ.IO</b>
</p>

<p align="center">  <a href="https://github.com/CityOfZion/neo3-boa"><strong>neo3-boa</strong></a> · <a href="https://github.com/CityOfZion/neo3-python">neo-mamba</a>  </p>

<p align="center">
  <a href="https://circleci.com/gh/CityOfZion/neo3-boa/tree/master">
    <img src="https://circleci.com/gh/CityOfZion/neo3-boa.svg?style=shield" alt="CircleCI.">
  </a>
  <a href="https://pypi.org/project/neo3-boa/">
    <img src="https://img.shields.io/pypi/v/neo3-boa.svg" alt="PyPI.">
  </a>
  <a href="https://opensource.org/licenses/Apache-2.0">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Licence.">
  </a>
</p>

<br/>

## Table of Contents
- [Overview](#overview)
  - [Product Strategy](#product-strategy)
  - [Project Structure](#project-structure)
- [Quickstart](#quickstart)
  - [Installation](#installation)
    - [Pip (Recomended)](#pip-recomended)
    - [Build from Source](#build-from-source)
  - [Compiling your Smart Contract](#compiling-your-smart-contract)
    - [Using CLI](#using-cli)
    - [Using Python Script](#using-python-script)
  - [Configuring the Debugger](#configuring-the-debugger)
- [Docs](#docs)
- [Reference Examples](#reference-examples)
- [Python Supported Features](#python-supported-features)
- [Neo Python Suite Projects](#neo-python-suite-projects)
- [Opening a New Issue](#opening-a-new-issue)
- [License](#license)

## Overview

Neo3-Boa is a tool for creating Neo Smart Contracts using Python. It compiles `.py` files to `.nef` and `.manisfest.json` formats for usage in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm/) which is used to execute contracts on the [Neo Blockchain](https://github.com/neo-project/neo/).

Neo-boa is part of the Neo Python Framework, aimed to allow the full development of dApps using Python alone.

#### Product Strategy

##### Pure Python
We want Python developers to feel comfortable when trying neo3-boa for the first time. It should look and behave like regular Python. For this reason we decided to avoid adding new keywords, but use decorators and helper functions instead.

##### Neo Python Framework
In the real world, simply coding a smart contract is not enough. Developers need to debug, deploy and invoke it. Therefore it’s important for this tool to be part of a bigger Python framework. To help the developers and avoid a bad user experience, we need to use logs and inform errors with details.

##### Testing against Neo VM
We need to ensure that the code works as expected, and the only way to do that is to run our tests against the official Neo 3 VM. Neo repository already contains a class called TestEngine that is capable of running tests using C# smart-contracts. It will be adjusted to support compiled smart-contracts.

##### Maintenance
Create a product that is easy to maintain and upgrade. Use Unit tests, typed and documented code to ensure its maintainability.

#### Project Structure

The diagram bellow shows the basic building blocks of the Neo3-Boa project.
<p>
  <img
    src="/.github/resources/images/diagram.png"
    width="500px;">
</p>

## Quickstart

Installation requires Python 3.8 or later.

### Installation 
Make sure you have installed MSVC v142 - Build tools VS 2019 C++ x64/x86 (v14.24). You can do this by installing Visual Studio 2019 and add C++ development features.

###### 1. Make a Python 3 virtual environment and activate it:

Linux / Mac OS:
```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

On Windows:

```shell
$ python3 -m venv venv
$ venv/Scripts/activate.bat
```

###### 2. Install Neo3-Boa using Pip

```shell
$ pip install neo3-boa
```

###### 2.1. (Optional) Run from source code
If neo3-boa is not available via pip, you can run it from source.

###### 2.1.1 Clone neo3-boa
```shell
$ git clone https://github.com/CityOfZion/neo3-boa.git
```
###### 2.1.2 Install project dependencies
```shell
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

### Debugger ready
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

## Docs
You can [read the docs here](https://docs.coz.io/neo3/boa/index.html). Please check our examples for reference.

## Examples

For an extensive collection of examples:
- [Smart contract examples](/boa3_test/examples)
- [Features tests](/boa3_test/test_sc)

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
    <td>🔜</td>
    <td>backlog</td>
    <td>Arithmetic operations</td>
    <td>
      <pre>
        <code>
  /, **
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
    <td>🔜</td>
    <td>backlog</td>
    <td>Relational operations</td>
    <td>
      <pre>
        <code>
  is, is not
        </code>
      </pre>
    </td>
    <td>
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
    <td>🔜</td>
    <td>backlog</td>
    <td>Bitwise augmented assignment operators</td>
    <td>
      <pre>
        <code>
  &=, |=, ~=, ^=, <<=, >>=
        </code>
      </pre>
    </td>
    <td>
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
    <td>🔜</td>
    <td>backlog</td>
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
    <td>next release</td>
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
    <td>🔜</td>
    <td>next release</td>
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
    </td>
  </tbody>
  <tbody>
    <td>🔜</td>
    <td>next release</td>
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
    <td>🔜</td>
    <td>backlog</td>
    <td>Built in function</td>
    <td>
      <pre>
        <code>
  a = abs(-5)
  b = max(7, 0, 12, 8)
  c = min(1, 6, 2)
  d = pow(2, 2)
  e = sum(list_of_num, 0)
  f = reversed([1, 2, 3, 4])
        </code>
      </pre>
    </td>
    <td>
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
    <td>🔜</td>
    <td>backlog</td>
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
    <td>🔜</td>
    <td>backlog</td>
    <td>Pass</td>
    <td>
    </td>
    <td>
    </td>
  </tbody>
  <tbody>
    <td>✅</td>
    <td>v0.3</td>
    <td>Import</td>
    <td>Only <code>boa3.builtin</code> packages are supported right now.</td>
    <td>
      <a href="/docs/ContractExamplesTest.md#import">List of examples</a>
    </td>
  </tbody>
</table>


## Neo Python Suite Projects

- **[neo3-boa](https://github.com/CityOfZion/neo3-boa)**: Python smart contracts compiler.</br>
- [neo3-mamba](https://github.com/CityOfZion/neo-mamba): Python SDK for interacting with neo.</br>

## Opening a New Issue

- Open a new [issue](https://github.com/CityOfZion/neo3-boa/issues/new) if you encounter a problem.
- Pull requests are welcome. New features, writing tests and documentation are all needed.


## License

- Open-source [Apache 2.0](https://github.com/CityOfZion/neo3-boa/blob/master/LICENSE).
