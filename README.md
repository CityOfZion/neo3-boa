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
If Pip is not available, you can run Neo3-Boa from source.

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
      <a href="/boa3_test/test_sc/variable_test/ArgumentAssignment.py">ArgumentAssignment.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/AssignLocalWithArgument.py">AssignLocalWithArgument.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/AssignLocalWithArgumentShadowingGlobal.py">AssignLocalWithArgumentShadowingGlobal.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/AssignmentWithoutType.py">AssignmentWithoutType.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/AssignmentWithType.py">AssignmentWithType.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/DeclarationWithType.py">DeclarationWithType.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/ManyAssignments.py">ManyAssignments.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/ReturnArgument.py">ReturnArgument.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/ReturnLocalVariable.py">ReturnLocalVariable.py</a>
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
      <a href="/boa3_test/test_sc/variable_test/GetGlobalValueWrittenAfter.py">GetGlobalValueWrittenAfter.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/GlobalAssignmentBetweenFunctions.py">GlobalAssignmentBetweenFunctions.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/GlobalAssignmentInFunctionWithArgument.py">GlobalAssignmentInFunctionWithArgument.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/GlobalAssignmentInFunctionWithArgument.py">GlobalAssignmentInFunctionWithArgument.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/GlobalAssignmentWithType.py">GlobalAssignmentWithType.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/GlobalDeclarationWithArgumentWrittenAfter.py">GlobalDeclarationWithArgumentWrittenAfter.py</a>, 
      <a href="/boa3_test/test_sc/variable_test/ManyGlobalAssignments.py">ManyGlobalAssignments.py</a>
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
      <a href="/boa3_test/test_sc/variable_test/GlobalAssignmentInFunctionWithArgument.py">GlobalAssignmentInFunctionWithArgument.py</a>
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
      <a href="/boa3_test/test_sc/arithmetic_test/Addition.py">Addition.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/AdditionThreeElements.py">AdditionThreeElements.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/Concatenation.py">Concatenation.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/IntegerDivision.py">IntegerDivision.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/MixedOperations.py">MixedOperations.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/Modulo.py">Modulo.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/Multiplication.py">Multiplication.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/Negative.py">Negative.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/Positive.py">Positive.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/StringMultiplication.py">StringMultiplication.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/Subtraction.py">Subtraction.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/WithParentheses.py">WithParentheses.py</a>
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
      <a href="/boa3_test/test_sc/arithmetic_test/AdditionAugmentedAssignment.py">AdditionAugmentedAssignment.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/ConcatenationAugmentedAssignment.py">ConcatenationAugmentedAssignment.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/IntegerDivisionAugmentedAssignment.py">IntegerDivisionAugmentedAssignment.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/ModuloAugmentedAssignment.py">ModuloAugmentedAssignment.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/MultiplicationAugmentedAssignment.py">MultiplicationAugmentedAssignment.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/StringMultiplicationAugmentedAssignment.py">StringMultiplicationAugmentedAssignment.py</a>, 
      <a href="/boa3_test/test_sc/arithmetic_test/SubtractionAugmentedAssignment.py">SubtractionAugmentedAssignment.py</a>
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
      <a href="/boa3_test/test_sc/relational_test/BoolEquality.py">BoolEquality.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/BoolInequality.py">BoolInequality.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/MixedEquality.py">MixedEquality.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/MixedInequality.py">MixedInequality.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine.py</a>, 
      <a href="/boa3_test/test_sc/none_test/NoneEquality.py">NoneEquality.py</a>, 
      <a href="/boa3_test/test_sc/none_test/NoneIdentity.py">NoneIdentity.py</a>, 
      <a href="/boa3_test/test_sc/none_test/NoneNotIdentity.py">NoneNotIdentity.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/NumEquality.py">NumEquality.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/NumGreaterOrEqual.py">NumGreaterOrEqual.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/NumGreaterThan.py">NumGreaterThan.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/NumInequality.py">NumInequality.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/NumLessOrEqual.py">NumLessOrEqual.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/NumLessThan.py">NumLessThan.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/NumRange.py">NumRange.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/StrEquality.py">StrEquality.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/StrGreaterOrEqual.py">StrGreaterOrEqual.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/StrGreaterThan.py">StrGreaterThan.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/StrInequality.py">StrInequality.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/StrLessOrEqual.py">StrLessOrEqual.py</a>, 
      <a href="/boa3_test/test_sc/relational_test/StrLessThan.py">StrLessThan.py</a>
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
      <a href="/boa3_test/test_sc/logical_test/LogicAndBool.py">LogicAndBool.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/LogicAndInt.py">LogicAndInt.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/LogicLeftShift.py">LogicLeftShift.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/LogicNotBool.py">LogicNotBool.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/LogicNotInt.py">LogicNotInt.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/LogicOrBool.py">LogicOrBool.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/LogicOrInt.py">LogicOrInt.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/LogicRightShift.py">LogicRightShift.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/LogicXorBool.py">LogicXorBool.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/LogicXorInt.py">LogicXorInt.py</a>
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
      <a href="/boa3_test/test_sc/logical_test/BoolAnd.py">BoolAnd.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/BoolNot.py">BoolNot.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/BoolOr.py">BoolOr.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/BoolOrThreeElements.py">BoolOrThreeElements.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/MixedOperations.py">MixedOperations.py</a>, 
      <a href="/boa3_test/test_sc/logical_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine.py</a>
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
      <a href="/boa3_test/test_sc/none_test/NoneTuple.py">NoneTuple.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/BoolTuple.py">BoolTuple.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/EmptyTupleAssignment.py">EmptyTupleAssignment.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/GetValue.py">GetValue.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/IntTuple.py">IntTuple.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/Nep5Main.py">Nep5Main.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/StrTuple.py">StrTuple.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleOfTuple.py">TupleOfTuple.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingEndOmitted.py">TupleSlicingEndOmitted.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingLiteralValues.py">TupleSlicingLiteralValues.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingNegativeEnd.py">TupleSlicingNegativeEnd.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingNegativeStart.py">TupleSlicingNegativeStart.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingOmitted.py">TupleSlicingOmitted.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingStartOmitted.py">TupleSlicingStartOmitted.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingVariableValues.py">TupleSlicingVariableValues.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/VariableTuple.py">VariableTuple.py</a>
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
      <a href="/boa3_test/test_sc/list_test/AppendAnyValue.py">AppendAnyValue.py</a>, 
      <a href="/boa3_test/test_sc/list_test/AppendIntValue.py">AppendIntValue.py</a>, 
      <a href="/boa3_test/test_sc/list_test/AppendIntWithBuiltin.py">AppendIntWithBuiltin.py</a>, 
      <a href="/boa3_test/test_sc/list_test/BoolList.py">BoolList.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ClearList.py">ClearList.py</a>, 
      <a href="/boa3_test/test_sc/list_test/EmptyListAssignment.py">EmptyListAssignment.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ExtendAnyValue.py">ExtendAnyValue.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ExtendTupleValue.py">ExtendTupleValue.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ExtendWithBuiltin.py">ExtendWithBuiltin.py</a>, 
      <a href="/boa3_test/test_sc/list_test/GetValue.py">GetValue.py</a>, 
      <a href="/boa3_test/test_sc/list_test/GetValueNegativeIndex.py">GetValueNegativeIndex.py</a>, 
      <a href="/boa3_test/test_sc/list_test/IntList.py">IntList.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ListOfList.py">ListOfList.py</a>, 
      <a href="/boa3_test/test_sc/list_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine.py</a>, 
      <a href="/boa3_test/test_sc/list_test/Nep5Main.py">Nep5Main.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ReverseList.py">ReverseList.py</a>, 
      <a href="/boa3_test/test_sc/list_test/SetValue.py">SetValue.py</a>, 
      <a href="/boa3_test/test_sc/list_test/SetValueNegativeIndex.py">SetValueNegativeIndex.py</a>, 
      <a href="/boa3_test/test_sc/list_test/StrList.py">StrList.py</a>, 
      <a href="/boa3_test/test_sc/list_test/TypeHintAssignment.py">TypeHintAssignment.py</a>, 
      <a href="/boa3_test/test_sc/list_test/VariableList.py">VariableList.py</a>
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
      <a href="/boa3_test/test_sc/list_test/PopList.py">PopList.py</a>, 
      <a href="/boa3_test/test_sc/list_test/PopListLiteralArgument.py">PopListLiteralArgument.py</a>, 
      <a href="/boa3_test/test_sc/list_test/PopListLiteralNegativeArgument.py">PopListLiteralNegativeArgument.py</a>, 
      <a href="/boa3_test/test_sc/list_test/PopListVariableArgument.py">PopListVariableArgument.py</a>, 
      <a href="/boa3_test/test_sc/list_test/PopListWithoutAssignment.py">PopListWithoutAssignment.py</a>
    </td>
  </tbody>
  <tbody>
    <td>🔜</td>
    <td>next release</td>
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
      <a href="/boa3_test/test_sc/dict_test/AnyValueDict.py">AnyValueDict.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/DictOfDict.py">DictOfDict.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/EmptyDictAssignment.py">EmptyDictAssignment.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/GetValue.py">GetValue.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/IntKeyDict.py">IntKeyDict.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/KeysDict.py">KeysDict.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/SetValue.py">SetValue.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/StrKeyDict.py">StrKeyDict.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/TypeHintAssignment.py">TypeHintAssignment.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/ValuesDict.py">ValuesDict.py</a>, 
      <a href="/boa3_test/test_sc/dict_test/VariableDict.py">VariableDict.py</a>
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
      <a href="/boa3_test/test_sc/bytes_test/BytearrayToIntWithBytesBuiltin.py">BytearrayToIntWithBytesBuiltin.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytesFromBytearray.py">BytesFromBytearray.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytesGetValue.py">BytesGetValue.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytesGetValueNegativeIndex.py">BytesGetValueNegativeIndex.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytesLiteral.py">BytesLiteral.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytesToInt.py">BytesToInt.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytesToIntWithBuiltin.py">BytesToIntWithBuiltin.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytesToStr.py">BytesToStr.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytesToStrWithBuiltin.py">BytesToStrWithBuiltin.py</a>
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
      <a href="/boa3_test/test_sc/bytes_test/BytearrayAppend.py">BytearrayAppend.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayAppendWithBuiltin.py">BytearrayAppendWithBuiltin.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayAppendWithMutableSequence.py">BytearrayAppendWithMutableSequence.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayClear.py">BytearrayClear.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayFromLiteralBytes.py">BytearrayFromLiteralBytes.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayFromVariableBytes.py">BytearrayFromVariableBytes.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayGetValuet.py">BytearrayGetValue.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayGetValueNegativeIndex.py">BytearrayGetValueNegativeIndex.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayReverse.py">BytearrayReverse.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearraySetValue.py">BytearraySetValue.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearraySetValueNegativeIndex.py">BytearraySetValueNegativeIndex.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayToInt.py">BytearrayToInt.py</a>, 
      <a href="/boa3_test/test_sc/bytes_test/BytearrayToIntWithBuiltin.py">BytearrayToIntWithBuiltin.py</a>
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
      <a href="/boa3_test/test_sc/while_test/ConstantCondition.py">ConstantCondition.py</a>, 
      <a href="/boa3_test/test_sc/while_test/MultipleRelationalCondition.py">MultipleRelationalCondition.py</a>, 
      <a href="/boa3_test/test_sc/while_test/NestedWhile.py">NestedWhile.py</a>, 
      <a href="/boa3_test/test_sc/while_test/RelationalCondition.py">RelationalCondition.py</a>, 
      <a href="/boa3_test/test_sc/while_test/VariableCondition.py">VariableCondition.py</a>, 
      <a href="/boa3_test/test_sc/while_test/WhileBoa2Test.py">WhileBoa2Test.py</a>, 
      <a href="/boa3_test/test_sc/while_test/WhileBoa2Test1.py">WhileBoa2Test1.py</a>, 
      <a href="/boa3_test/test_sc/while_test/WhileBoa2Test2.py">WhileBoa2Test2.py</a>, 
      <a href="/boa3_test/test_sc/while_test/WhileBreak.py">WhileBreak.py</a>, 
      <a href="/boa3_test/test_sc/while_test/WhileBreakElse.py">WhileBreakElse.py</a>, 
      <a href="/boa3_test/test_sc/while_test/WhileContinue.py">WhileContinue.py</a>, 
      <a href="/boa3_test/test_sc/while_test/WhileElse.py">WhileElse.py</a>
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
      <a href="/boa3_test/test_sc/if_test/ConstantCondition.py">ConstantCondition.py</a>, 
      <a href="/boa3_test/test_sc/if_test/IfElif.py">IfElif.py</a>, 
      <a href="/boa3_test/test_sc/if_test/IfElse.py">IfElse.py</a>, 
      <a href="/boa3_test/test_sc/if_test/IfExpVariableCondition.py">IfExpVariableCondition.py</a>, 
      <a href="/boa3_test/test_sc/if_test/MultipleBranches.py">MultipleBranches.py</a>, 
      <a href="/boa3_test/test_sc/if_test/NestedIf.py">NestedIf.py</a>, 
      <a href="/boa3_test/test_sc/if_test/RelationalCondition.py">RelationalCondition.py</a>, 
      <a href="/boa3_test/test_sc/if_test/VariableCondition.py">VariableCondition.py</a>
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
      <a href="/boa3_test/test_sc/for_test/ForBreak.py">ForBreak.py</a>, 
      <a href="/boa3_test/test_sc/for_test/ForBreakElse.py">ForBreakElse.py</a>, 
      <a href="/boa3_test/test_sc/for_test/ForContinue.py">ForContinue.py</a>, 
      <a href="/boa3_test/test_sc/for_test/ForElse.py">ForElse.py</a>, 
      <a href="/boa3_test/test_sc/for_test/NestedFor.py">NestedFor.py</a>, 
      <a href="/boa3_test/test_sc/for_test/StringCondition.py">StringCondition.py</a>, 
      <a href="/boa3_test/test_sc/for_test/TupleCondition.py">TupleCondition.py</a>
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
      <a href="/boa3_test/test_sc/function_test/CallFunctionWithoutVariables.py">CallFunctionWithoutVariables.py</a>, 
      <a href="/boa3_test/test_sc/function_test/CallFunctionWrittenBefore.py">CallFunctionWrittenBefore.py</a>, 
      <a href="/boa3_test/test_sc/function_test/CallReturnFunctionOnReturn.py">CallReturnFunctionOnReturn.py</a>, 
      <a href="/boa3_test/test_sc/function_test/CallReturnFunctionWithLiteralArgs.py">CallReturnFunctionWithLiteralArgs.py</a>, 
      <a href="/boa3_test/test_sc/function_test/CallReturnFunctionWithoutArgs.py">CallReturnFunctionWithoutArgs.py</a>, 
      <a href="/boa3_test/test_sc/function_test/CallReturnFunctionWithVariableArgs.py">CallReturnFunctionWithVariableArgs.py</a>, 
      <a href="/boa3_test/test_sc/function_test/CallVoidFunctionWithLiteralArgs.py">CallVoidFunctionWithLiteralArgs.py</a>, 
      <a href="/boa3_test/test_sc/function_test/CallVoidFunctionWithoutArgs.py">CallVoidFunctionWithoutArgs.py</a>, 
      <a href="/boa3_test/test_sc/function_test/CallVoidFunctionWithVariableArgs.py">CallVoidFunctionWithVariableArgs.py</a>
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
      <a href="/boa3_test/test_sc/built_in_methods_test">Folder with the Examples.</a>
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
      <a href="/boa3_test/test_sc/range_test">Range examples folder</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceBoolLiteral.py">IsInstanceBoolLiteral.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceBoolVariable.py">IsInstanceBoolVariable.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceIntLiteral.py">IsInstanceIntLiteral.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceIntVariable.py">IsInstanceIntVariable.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceListLiteral.py">IsInstanceListLiteral.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceManyTypes.py">IsInstanceManyTypes.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceStrLiteral.py">IsInstanceStrLiteral.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceStrVariable.py">IsInstanceStrVariable.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceTupleLiteral.py">IsInstanceTupleLiteral.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceTupleVariable.py">IsInstanceTupleVariable.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/IsInstanceVariableType.py">IsInstanceVariableType.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/PrintInt.py">PrintInt.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/PrintIntMissingFunctionReturn.py">PrintIntMissingFunctionReturn.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/PrintList.py">PrintList.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/PrintManyValues.py">PrintManyValues.py</a>, 
      <a href="/boa3_test/test_sc/built_in_methods_test/PrintStr.py">PrintStr.py</a>
    </td>
  </tbody>
  <tbody>
    <td>🔜</td>
    <td>next release</td>
    <td>Built in function</td>
    <td>
      <pre>
        <code>
  a = reversed([1, 2, 3, 4])
        </code>
      </pre>
    </td>
    <td>
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
      <a href="/boa3_test/test_sc/arithmetic_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine (Arithmetic)</a>, 
      <a href="/boa3_test/test_sc/logical_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine (Logical)</a>, 
      <a href="/boa3_test/test_sc/list_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine (List)</a>, 
      <a href="/boa3_test/test_sc/tuple_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine (Tuple)</a>, 
      <a href="/boa3_test/test_sc/relational_test/MultipleExpressionsInLine.py">MultipleExpressionsInLine (Relational)</a>
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
      <a href="/boa3_test/test_sc/list_test/ListSlicingEndOmitted.py">ListSlicingEndOmitted.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ListSlicingLiteralValues.py">ListSlicingLiteralValues.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ListSlicingNegativeEnd.py">ListSlicingNegativeEnd.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ListSlicingNegativeStart.py">ListSlicingNegativeStart.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ListSlicingOmitted.py">ListSlicingOmitted.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ListSlicingStartOmitted.py">ListSlicingStartOmitted.py</a>, 
      <a href="/boa3_test/test_sc/list_test/ListSlicingVariableValues.py">ListSlicingVariableValues.py</a>, 
      <a href="/boa3_test/test_sc/string_test/StringSlicingEndOmitted.py">StringSlicingEndOmitted.py</a>, 
      <a href="/boa3_test/test_sc/string_test/StringSlicingLiteralValues.py">StringSlicingLiteralValues.py</a>, 
      <a href="/boa3_test/test_sc/string_test/StringSlicingNegativeEnd.py">StringSlicingNegativeEnd.py</a>, 
      <a href="/boa3_test/test_sc/string_test/StringSlicingNegativeStart.py">StringSlicingNegativeStart.py</a>, 
      <a href="/boa3_test/test_sc/string_test/StringSlicingOmitted.py">StringSlicingOmitted.py</a>, 
      <a href="/boa3_test/test_sc/string_test/StringSlicingStartOmitted.py">StringSlicingStartOmitted.py</a>, 
      <a href="/boa3_test/test_sc/string_test/StringSlicingVariableValues.py">StringSlicingVariableValues.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingEndOmitted.py">TupleSlicingEndOmitted.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingLiteralValues.py">TupleSlicingLiteralValues.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingNegativeEnd.py">TupleSlicingNegativeEnd.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingNegativeStart.py">TupleSlicingNegativeStart.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingOmitted.py">TupleSlicingOmitted.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingStartOmitted.py">TupleSlicingStartOmitted.py</a>, 
      <a href="/boa3_test/test_sc/tuple_test/TupleSlicingVariableValues.py">TupleSlicingVariableValues.py</a>
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
      <a href="/boa3_test/test_sc/assert_test/AssertAny.py">AssertAny.py</a>, 
      <a href="/boa3_test/test_sc/assert_test/AssertBinaryOperation.py">AssertBinaryOperation.py</a>, 
      <a href="/boa3_test/test_sc/assert_test/AssertBytes.py">AssertBytes.py</a>, 
      <a href="/boa3_test/test_sc/assert_test/AssertDict.py">AssertDict.py</a>, 
      <a href="/boa3_test/test_sc/assert_test/AssertInt.py">AssertInt.py</a>, 
      <a href="/boa3_test/test_sc/assert_test/AssertList.py">AssertList.py</a>, 
      <a href="/boa3_test/test_sc/assert_test/AssertStr.py">AssertStr.py</a>, 
      <a href="/boa3_test/test_sc/assert_test/AssertUnaryOperation.py">AssertUnaryOperation.py</a>, 
      <a href="/boa3_test/test_sc/assert_test/AssertWithMessage.py">AssertWithMessage.py</a>
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
      <a href="/boa3_test/test_sc/exception_test/TryExceptBaseException.py">TryExceptBaseException.py</a>, 
      <a href="/boa3_test/test_sc/exception_test/TryExceptSpecificException.py">TryExceptSpecificException.py</a>, 
      <a href="/boa3_test/test_sc/exception_test/TryExceptWithoutException.py">TryExceptWithoutException.py</a>
    </td>
  </tbody>
  <tbody>
    <td>🔜</td>
    <td>next release</td>
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
      <a href="/boa3_test/test_sc/import_test/FromImportTyping.py">FromImportTyping.py</a>, 
      <a href="/boa3_test/test_sc/import_test/FromImportTypingWithAlias.py">FromImportTypingWithAlias.py</a>, 
      <a href="/boa3_test/test_sc/import_test/FromImportUserModule.py">FromImportUserModule.py</a>, 
      <a href="/boa3_test/test_sc/import_test/FromImportUserModuleWithAlias.py">FromImportUserModuleWithAlias.py</a>, 
      <a href="/boa3_test/test_sc/import_test/FromImportVariable.py">FromImportVariable.py</a>, 
      <a href="/boa3_test/test_sc/import_test/FromImportWithGlobalVariables.py">FromImportWithGlobalVariables.py</a>, 
      <a href="/boa3_test/test_sc/import_test/ImportTyping.py">ImportTyping.py</a>, 
      <a href="/boa3_test/test_sc/import_test/ImportTypingWithAlias.py">ImportTypingWithAlias.py</a>, 
      <a href="/boa3_test/test_sc/import_test/ImportUserModule.py">ImportUserModule.py</a>, 
      <a href="/boa3_test/test_sc/import_test/ImportUserModuleWithAlias.py">ImportUserModuleWithAlias.py</a>
    </td>
  </tbody>
</table>

## Neo Python Suite Projects

- <b>[neo3-boa](https://github.com/CityOfZion/neo3-boa)</b>: Python smart contracts compiler.</br>
- [neo3-mamba](https://github.com/CityOfZion/neo-mamba): Python SDK for interacting with neo.</br>

## Opening a New Issue

- Open a new [issue](https://github.com/CityOfZion/neo3-boa/issues/new) if you encounter a problem.
- Pull requests are welcome. New features, writing tests and documentation are all needed.


## License

- Open-source [Apache 2.0](https://github.com/CityOfZion/neo3-boa/blob/master/LICENSE).
