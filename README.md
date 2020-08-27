<p align="center">
  <img
    src="/.github/resources/image/boa-rgb1.png"
    width="200px;">
</p>

<p align="center">
  Write smart contracts for Neo3 in Python by COZ
</p>

<p align="center"> · <a href="https://github.com/CityOfZion/neo3-boa"><strong>neo3-boa</strong></a> · <a href="https://github.com/CityOfZion/neo3-python"><strong>neo3-mamba</strong></a> · </p>

</p>
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
- [Supported Features](#supported-features)
- [Neo Python Suite Projects](#neo-python-suite-projects)
- [Opening a New Issue](#opening-a-new-issue)
- [License](#license)

<br/>
<br/>

## Overview

Neo3-Boa is a tool for creating Neo Smart Contracts using Python. It compiles `.py` files to `.nef` and `.manisfest.json` formats for usage in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm/) which is used to execute contracts on the [Neo Blockchain](https://github.com/neo-project/neo/).

Neo-boa is part of the Neo Python Framework, aimed to allow the full development of dApps using Python alone.

#### Product Strategy

##### Pure Python
We want Python developers to feel comfortable when trying neo3- boa for
the first time. It should look and behave like regular Python. For this reason,
we decided to avoid adding new keywords, but use decorators and helpers
functions instead.

##### Neo Python Framework
In real world, only coding a smart contract is not enough. Developers need
to debug, deploy and invoke it. It is important then, that this tool is be part of
a bigger Python framework.
Help the developer
To avoid a bad user experience, we need to use logs and inform errors with
details.

##### Testing against Neo VM
We need to ensure that the code works as expected, and the only way to do
that is to run our tests against the official Neo 3 VM.
Neo repository already contains a class called TestEngine that is capable of
running tests using C# smart- contracts. It will be adjusted to support
com piled smart- contracts.

##### Maintenance
Create a product that is easy to main and upgrade. Use Unit tests, typed
and documented code to ensure its maintainability.

#### Project Structure

The diagram bellow shows the basic buiding blocks of the Neo3-Boa project.
<p>
  <img
    src="/.github/resources/image/Simpli_neo3-boa_activity_diagram0.2.png"
    width="500px;">
</p>

<br/>
<br/>

## Quickstart

Installation requires a Python 3.8 or later environment.

### Installation 

1. Make a Python 3 virtual environment and activate it via:

```
python3 -m venv venv
source venv/bin/activate
```

1.1. For Windows:

```
python3 -m venv venv
venv/Scripts/activate.bat
```

2. Install Neo3-Boa using Pip

```
pip install neo3-boa
```

2.1. Build from Source

You can also compile Neo3-Boa on your local machine.

2.1.1. Clone the repository and navigate into the project directory.

2.1.2. 
```
pip install -e .
```

<br/>

> Note: If you have problems with the requirements installation make sure you have installed MSVC v142 - Build tools VS 2019 C++ x64/x86 (v14.24).


### Compiling your Smart Contract

#### Using CLI

```
> neo3-boa path/to/your/file.py
```

#### Using Python Script

```
from boa3.boa3 import Boa3

Boa3.compile_and_save('path/to/your/file.py')
```

### Configuring the Debugger

<br/>
<br/>

## Docs

You can [read the docs here](https://docs.coz.io/neo3/boa/index.html).

<br/>
<br/>

## Reference Examples

For an extensive collection of examples:
- [Smart Contract Examples](/boa3_test/examples)
- [Implemented Features Test Examples](/boa3_test/test_sc)

<br/>
<br/>

## Supported Features

| Status | Converts | Example Code |
| :--:|:---|:---|
|✅ | <p>Local Variable Declarations and Assignments</p>       | <p>`def func():`<br/>&emsp;`foo: int = 42`<br/> &emsp;`bar = foo`</p> |
|✅ | <p>Global Variable Declarations and Assignments</p>       | <p>`foo: int = 42`<br/>`bar = foo`</p> |
|✅ | <p>Arithmetic Operations</p>                      | <p>`+`, `-`, `*`, `//`, `%`</p> |
|🔜 | <p>Arithmetic Operations</p>                      | <p>`/`, `**`</p> |
|✅ | <p>Arithmetic Augmented assignment Operators</p> | <p>`+=`, `-=`, `*=`, `//=`, `%=`</p> |
|🔜 | <p>Arithmetic Augmented assignment Operators</p> | <p>`/=`</p> |
|✅ | <p>Relational Operations</p>                             | <p>`==`, `!=`, `<`, `<=`, `>`, `>=`<br/>`is None`, `is not None`</p> |
|🔜 | <p>Relational Operations</p>                          | <p>`is`, `is not`</p> |
|✅ | <p>Bitwise Operations</p>                             | <p>`&`, `\|`, `~`, `^`, `<<`, `>>`</p> |
|🔜 | <p>Bitwise Augmented assignment Operators</p> | <p>`&=`, `\|=`, `~=`, `^=`, `<<=`, `>>=`</p> |
|✅ | <p>Boolean Logic Operations</p>      | <p>`and`, `or`, `not`<p/> |
|✅ | <p>Tuple type</p>                                            | <p>`a = ('1', '2', '3')`</p> |
|✅ | <p>List type</p>                                             | <p>`a = ['1', '2', '3']`</p> |
|✅ | <p>Dict type</p>                                             | <p>`a = {1:'1', 2:'2', 3:'3'}`</p> |
|🔜 | <p>Set type</p>                                              | <p>`a = {'1', '2', '3'}`</p> |
|✅ | <p>Bytes type</p>                                            | <p>`a = b'\x01\x02\x03\x04'`</p> |
|✅ | <p>Bytearray type</p>                                        | <p>`a = bytearray(b'\x01\x02\x03\x04')`</p> |
|✅ | <p>While Statement</p>                                       | <p>`foo = 0`<br/>`while condition:`<br/>&emsp;`foo = foo + 2`</p> |
|✅ | <p>If, elif, else Statements</p>                             | <p>`if condition1:`<br/>&emsp;`foo = 0`<br/>`elif condition2:`<br/>&emsp;`foo = 1`<br/>`else:`<br/>&emsp;`bar = 2`</p>     |
|✅ | <p>For Statement</p>                                         | <p>`for x in (1, 2, 3):`<br/>&emsp;`...`</p> |
|✅ | <p>Function Call</p>                                         | <p>`def Main(num: int):`<br/>&emsp;`a = foo(num)`<br/>&emsp;`...`<br/><br/>`def foo(num: int) -> int:`<br/>&emsp;`...`</p> |
|✅ | <p>Built in function</p>               | <p>`a = len('hello')`</p> |
|🔜 | <p>Built in function</p>               | <p>`a = abs(-5)`<br/>`b = max(7, 0, 12, 8)`<br/>`c = min(1, 6, 2)`<br/>`d = pow(2, 2)`<br/>`f = sum(list_of_num, 0)`<br/>`g = range(1,5,2)`<br/>`h = reversed([1, 2, 3, 4])`</p> |
|✅ | <p>Multiple Expressions in the same line<p/>                 | <p>`i = i + h; a = 1; b = 3 + a; count = 0`</p> |
|🔜 | <p>Chained assignment<p/>                 | <p>`x = y = foo()`</p> |
|✅ | <p>Sequence Slicing<p/>                                        | <p>`x = 'example'[2:4]`, `x = [1, 2, 3][:2]`, `x = 'example'[4:]`, `x = (1, 2, 3)[:]`, `x = 'example'[-4:-2]`, `x = 'example'[:-4]`</p> |
|🔜 | <p>Sequence Slicing</p> | <p>`x = 'example'[2:4:2]`, `x = 'example'[::2]`</p> |
|✅ | <p>Assert</p>                                             | <p>`assert x % 2 == 0`<br/>`assert x % 3 != 2, 'error message'`</p> |
|✅ | <p>Try catch</p>                                             | <p>`try:`<br/>&emsp;`a = foo(b)`<br/>`except Exception as e:`<br/>&emsp;`a = foo(b)`</p> |
|🔜 | <p>`continue`</p>                                            |  |
|🔜 | <p>`break`</p>                                               |  |
|🔜 | <p>`pass`</p>                                                |  |
|✅ | <p>Import</p>                                                | <p>Only `boa3.builtin` packages are supported right now.</p> |

<br/>
<br/>

## Neo Python Suite Projects

- [neo3-boa](https://github.com/CityOfZion/neo3-boa): Python smart contracts compiler.</br>
- [neo3-mamba](https://github.com/CityOfZion/neo-mamba): Python SDK for interacting with neo.</br>

<br/>
<br/>

## Opening a New Issue

- Open a new [issue](https://github.com/CityOfZion/neo3-boa/issues/new) if you encounter a problem.
- Pull requests are welcome. New features, writing tests and documentation are all needed.

<br/>
<br/>

## License

- Open-source [Apache 2.0](https://github.com/CityOfZion/neo3-boa/blob/master/LICENSE).
