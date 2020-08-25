<h1 align="center">neo3-boa</h1>
<p align="center">
  Write smart contracts for Neo3 in Python by COZ
</p>

<p align="center"> · <a href="https://github.com/neo-project/neo"><strong>Neo</strong></a> · <a href="https://github.com/CityOfZion/neo3-boa"><strong>neo3-boa</strong></a> · <a href="https://github.com/CityOfZion/neo3-python"><strong>neo3-mamba</strong></a> · </p>

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
- [Installation](#installation)
  - [Pip](#pip)
  - [Manual](#manual)
- [Quickstart](#quickstart)
- [Docs](#docs)
- [Supported Features](#supported-features)
- [Related Projects](#related-projects)
- [Project Structure](#project-structure)
- [Opening a New Issue](#opening-a-new-issue)
- [License](#license)

<br/>
<br/>

## Overview

The `neo3-boa` compiler is a tool for compiling Python files to the `.nef` and `.manisfest.json` formats for usage in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm/) which is used to execute contracts on the [Neo Blockchain](https://github.com/neo-project/neo/).

- Compiles a subset of the Python language to the `.nef` and `.manisfest.json` format for use in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm)

- Works for Python 3.6+

- Logs compiler errors and warnings
 
- Logs when the main method is analysed
 
- Logs method inclusions in `.abi` file to work with Neo Debuggers.
  
<br/>
<br/>

## Installation

Installation requires a Python 3.6 or later environment.

#### Pip

```
pip install neo3-boa
```

#### Manual

Clone the repository and navigate into the project directory. Make a Python 3 virtual environment and activate it via:

```
python3 -m venv venv
source venv/bin/activate
```

or, to install Python 3.6 specifically:

```
virtualenv -p /usr/local/bin/python3.6 venv
source venv/bin/activate
```

Then, install the requirements:

```
pip install -r requirements.txt
```

<br/>

> Note: If you have problems with the requirements installation make sure you have installed MSVC v142 - Build tools VS 2019 C++ x64/x86 (v14.24).

<br/>
<br/>

## Quickstart

The compiler may be used as follows:

```
from boa3.boa3 import Boa3

Boa3.compile_and_save('path/to/your/file.py')
```

Or you can use the cli version:

```
> neo3-boa path/to/your/file.py
```

You can find a smart contract example [here](boa3_test/examples/HelloWorld.py).

<br/>
<br/>

## Docs

You can [read the docs here](https://docs.coz.io/neo3/boa/index.html).

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
|🔜 | <p>Bytes Slicing</p> | <p>`x = b'\x01\x02\x03\x04'[2:]`, `x = b'\x01\x02\x03\x04'[:]`, `x = b'\x01\x02\x03\x04'[::2]`</p> |
|✅ | <p>Assert</p>                                             | <p>`assert x % 2 == 0`<br/>`assert x % 3 != 2, 'error message'`</p> |
|🔜 | <p>`continue`</p>                                            |  |
|🔜 | <p>`break`</p>                                               |  |
|🔜 | <p>`pass`</p>                                                |  |
|✅ | <p>Import</p>                                                | <p>`from boa3.builtin import public`<br/>`from typing import *`</p> |
|🔜 | <p>Import</p>                                                | <p>`import os`<br/>`from path.to.your.package import *`</p> |

<br/>
<br/>

## Related Projects

- [neo](https://github.com/neo-project/neo): Neo core library, contains base classes, including ledger, p2p and IO modules.</br>
- [neo3-boa](https://github.com/CityOfZion/neo3-boa): Python smart contracts compiler.</br>
- [neo3-mamba](https://github.com/CityOfZion/neo-mamba): Python SDK for interacting with neo.</br>

<br/>
<br/>

## Project Structure

<br/>
<br/>

## Opening a New Issue

- Open a new [issue](https://github.com/CityOfZion/neo3-boa/issues/new) if you encounter a problem.
- Pull requests are welcome. New features, writing tests and documentation are all needed.

<br/>
<br/>

## License

- Open-source [Apache](https://github.com/CityOfZion/neo3-boa/blob/master/LICENSE).
