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
- [Supported Features](#supported-features)
- [Neo Python Suite Projects](#neo-python-suite-projects)
- [Opening a New Issue](#opening-a-new-issue)
- [License](#license)

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
running tests using C# smart-contracts. It will be adjusted to support
compiled smart- contracts.

##### Maintenance
Create a product that is easy to main and upgrade. Use Unit tests, typed
and documented code to ensure its maintainability.

#### Project Structure

The diagram bellow shows the basic buiding blocks of the Neo3-Boa project.
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

## Supported Features

| Status | Converts | Example Code | Contract Example Test |
| :--:|:---|:---|:---|
|✅ | <p>Local variable declarations and assignments</p>   | <p>`def func():`<br/>&emsp;`foo: int = 42`<br/> &emsp;`bar = foo`</p> | [ArgumentAssignment.py](/boa3_test/test_sc/variable_test/ArgumentAssignment.py), [AssignLocalWithArgument.py](/boa3_test/test_sc/variable_test/AssignLocalWithArgument.py), [AssignLocalWithArgumentShadowingGlobal.py](/boa3_test/test_sc/variable_test/AssignLocalWithArgumentShadowingGlobal.py), [AssignmentWithoutType.py](/boa3_test/test_sc/variable_test/AssignmentWithoutType.py), [AssignmentWithType.py](/boa3_test/test_sc/variable_test/AssignmentWithType.py), [AssignmentWithoutType.py](/boa3_test/test_sc/variable_test/AssignmentWithoutType.py), [DeclarationWithType.py](/boa3_test/test_sc/variable_test/DeclarationWithType.py), [ManyAssignments.py](/boa3_test/test_sc/variable_test/ManyAssignments.py), [ReturnArgument.py](/boa3_test/test_sc/variable_test/ReturnArgument.py), [ReturnLocalVariable.py](/boa3_test/test_sc/variable_test/ReturnLocalVariable.py) |
|✅ | <p>Global variable declarations and assignments</p>  | <p>`foo: int = 42`<br/>`bar = foo`</p> | [GetGlobalValueWrittenAfter.py](/boa3_test/test_sc/variable_test/GetGlobalValueWrittenAfter.py), [GlobalAssignmentBetweenFunctions.py](/boa3_test/test_sc/variable_test/GlobalAssignmentBetweenFunctions.py), [GlobalAssignmentInFunctionWithArgument.py](/boa3_test/test_sc/variable_test/GlobalAssignmentInFunctionWithArgument.py), [GlobalAssignmentInFunctionWithArgument.py](/boa3_test/test_sc/variable_test/GlobalAssignmentInFunctionWithArgument.py), [GlobalAssignmentWithType.py](/boa3_test/test_sc/variable_test/GlobalAssignmentWithType.py), [GlobalDeclarationWithArgumentWrittenAfter.py](/boa3_test/test_sc/variable_test/GlobalDeclarationWithArgumentWrittenAfter.py), [ManyGlobalAssignments.py](/boa3_test/test_sc/variable_test/ManyGlobalAssignments.py) |
|✅ | <p>Arithmetic operations</p>                         | <p>`+`, `-`, `*`, `//`, `%`</p> | [Addition.py](/boa3_test/test_sc/arithmetic_test/Addition.py), [AdditionThreeElements.py](/boa3_test/test_sc/arithmetic_test/AdditionThreeElements.py), [Concatenation.py](/boa3_test/test_sc/arithmetic_test/Concatenation.py), [IntegerDivision.py](/boa3_test/test_sc/arithmetic_test/IntegerDivision.py), [MixedOperations.py](/boa3_test/test_sc/arithmetic_test/MixedOperations.py), [Modulo.py](/boa3_test/test_sc/arithmetic_test/Modulo.py), [MultipleExpressionsInLine.py](/boa3_test/test_sc/arithmetic_test/MultipleExpressionsInLine.py), [Multiplication.py](/boa3_test/test_sc/arithmetic_test/Multiplication.py), [Negative.py](/boa3_test/test_sc/arithmetic_test/Negative.py), [Positive.py](/boa3_test/test_sc/arithmetic_test/Positive.py), [StringMultiplication.py](/boa3_test/test_sc/arithmetic_test/StringMultiplication.py), [Subtraction.py](/boa3_test/test_sc/arithmetic_test/Subtraction.py), [WithParentheses.py](/boa3_test/test_sc/arithmetic_test/WithParentheses.py) |
|🔜 | <p>Arithmetic operations</p>                         | <p>`/`, `**`</p> |  |
|✅ | <p>Arithmetic augmented assignment operators</p>     | <p>`+=`, `-=`, `*=`, `//=`, `%=`</p> | [AdditionAugmentedAssignment.py](/boa3_test/test_sc/arithmetic_test/AdditionAugmentedAssignment.py), [ConcatenationAugmentedAssignment.py](/boa3_test/test_sc/arithmetic_test/ConcatenationAugmentedAssignment.py), [IntegerDivisionAugmentedAssignment.py](/boa3_test/test_sc/arithmetic_test/IntegerDivisionAugmentedAssignment.py), [ModuloAugmentedAssignment.py](/boa3_test/test_sc/arithmetic_test/ModuloAugmentedAssignment.py), [MultiplicationAugmentedAssignment.py](/boa3_test/test_sc/arithmetic_test/MultiplicationAugmentedAssignment.py), [StringMultiplicationAugmentedAssignment.py](/boa3_test/test_sc/arithmetic_test/StringMultiplicationAugmentedAssignment.py), [SubtractionAugmentedAssignment.py](/boa3_test/test_sc/arithmetic_test/SubtractionAugmentedAssignment.py) |
|🔜 | <p>Arithmetic augmented assignment operators</p>     | <p>`/=`</p> |  |
|✅ | <p>Relational operations</p>                         | <p>`==`, `!=`, `<`, `<=`, `>`, `>=`<br/>`is None`, `is not None`</p> | [BoolEquality.py](/boa3_test/test_sc/relational_test/BoolEquality.py), [BoolInequality.py](/boa3_test/test_sc/relational_test/BoolInequality.py), [MixedEquality.py](/boa3_test/test_sc/relational_test/MixedEquality.py), [MixedInequality.py](/boa3_test/test_sc/relational_test/MixedInequality.py), [MultipleExpressionsInLine.py](/boa3_test/test_sc/relational_test/MultipleExpressionsInLine.py), [NoneEquality.py](/boa3_test/test_sc/none_test/NoneEquality.py), [NoneIdentity.py](/boa3_test/test_sc/none_test/NoneIdentity.py), [NoneNotIdentity.py](/boa3_test/test_sc/none_test/NoneNotIdentity.py), [NumEquality.py](/boa3_test/test_sc/relational_test/NumEquality.py), [NumGreaterOrEqual.py](/boa3_test/test_sc/relational_test/NumGreaterOrEqualpy), [NumGreaterThan.py](/boa3_test/test_sc/relational_test/NumGreaterThan.py), [NumInequality.py](/boa3_test/test_sc/relational_test/NumInequality.py), [NumLessOrEqual.py](/boa3_test/test_sc/relational_test/NumLessOrEqual.py), [NumLessThan.py](/boa3_test/test_sc/relational_test/NumLessThan.py), [NumRange.py](/boa3_test/test_sc/relational_test/NumRange.py), [StrEquality.py](/boa3_test/test_sc/relational_test/StrEquality.py), [StrGreaterOrEqual.py](/boa3_test/test_sc/relational_test/StrGreaterOrEqual.py), [StrGreaterThan.py](/boa3_test/test_sc/relational_test/StrGreaterThan.py), [StrInequality.py](/boa3_test/test_sc/relational_test/StrInequality.py), [StrLessOrEqual.py](/boa3_test/test_sc/relational_test/StrLessOrEqual.py), [StrLessThan.py](/boa3_test/test_sc/relational_test/StrLessThan.py) |
|🔜 | <p>Relational operations</p>                         | <p>`is`, `is not`</p> |  |
|✅ | <p>Bitwise operations</p>                            | <p>`&`, `\|`, `~`, `^`, `<<`, `>>`</p> | [LogicAndBool.py](/boa3_test/test_sc/logical_test/LogicAndBool.py), [LogicAndInt.py](/boa3_test/test_sc/logical_test/LogicAndInt.py), [LogicLeftShift.py](/boa3_test/test_sc/logical_test/LogicLeftShift.py), [LogicNotBool.py](/boa3_test/test_sc/logical_test/LogicNotBool.py), [LogicNotInt.py](/boa3_test/test_sc/logical_test/LogicNotInt.py), [LogicOrBool.py](/boa3_test/test_sc/logical_test/LogicOrBool.py), [LogicOrInt.py](/boa3_test/test_sc/logical_test/LogicOrInt.py), [LogicRightShift.py](/boa3_test/test_sc/logical_test/LogicRightShift.py), [LogicXorBool.py](/boa3_test/test_sc/logical_test/LogicXorBool.py), [LogicXorInt.py](/boa3_test/test_sc/logical_test/LogicXorInt.py) |
|🔜 | <p>Bitwise augmented assignment operators</p>        | <p>`&=`, `\|=`, `~=`, `^=`, `<<=`, `>>=`</p> |  |
|✅ | <p>Boolean logic operations</p>                      | <p>`and`, `or`, `not`<p/> | [BoolAnd.py](/boa3_test/test_sc/logical_test/BoolAnd.py), [BoolNot.py](/boa3_test/test_sc/logical_test/BoolNot.py), [BoolOr.py](/boa3_test/test_sc/logical_test/BoolOr.py), [BoolOrThreeElements.py](/boa3_test/test_sc/logical_test/BoolOrThreeElements.py), [MixedOperations.py](/boa3_test/test_sc/logical_test/MixedOperations.py), [MultipleExpressionsInLine.py](/boa3_test/test_sc/logical_test/MultipleExpressionsInLine.py) |
|✅ | <p>Tuple type</p>                                    | <p>`a = ('1', '2', '3')`</p> | [NoneTuple.py](/boa3_test/test_sc/none_test/NoneTuple.py), [BoolTuple.py](/boa3_test/test_sc/tuple_test/BoolTuple.py), [EmptyTupleAssignment.py](/boa3_test/test_sc/tuple_test/EmptyTupleAssignment.py), [GetValue.py](/boa3_test/test_sc/tuple_test/GetValue.py), [IntTuple.py](/boa3_test/test_sc/tuple_test/IntTuple.py), [MultipleExpressionsInLine.py](/boa3_test/test_sc/tuple_test/MultipleExpressionsInLine.py), [Nep5Main.py](/boa3_test/test_sc/tuple_test/Nep5Main.py), [StrTuple.py](/boa3_test/test_sc/tuple_test/StrTuple.py), [TupleOfTuple.py](/boa3_test/test_sc/tuple_test/TupleOfTuple.py), [TupleSlicingEndOmitted.py](/boa3_test/test_sc/tuple_test/TupleSlicingEndOmitted.py), [TupleSlicingLiteralValues.py](/boa3_test/test_sc/tuple_test/TupleSlicingLiteralValues.py), [TupleSlicingNegativeEnd.py](/boa3_test/test_sc/tuple_test/TupleSlicingNegativeEnd.py), [TupleSlicingNegativeStart.py](/boa3_test/test_sc/tuple_test/TupleSlicingNegativeStart.py), [TupleSlicingOmitted.py](/boa3_test/test_sc/tuple_test/TupleSlicingOmitted.py), [TupleSlicingStartOmitted.py](/boa3_test/test_sc/tuple_test/TupleSlicingStartOmitted.py), [TupleSlicingVariableValues.py](/boa3_test/test_sc/tuple_test/TupleSlicingVariableValues.py), [VariableTuple.py](/boa3_test/test_sc/tuple_test/VariableTuple.py) |
|✅ | <p>List type</p>                                     | <p>`a = ['1', '2', '3']`</p> | [AppendAnyValue.py](/boa3_test/test_sc/list_test/AppendAnyValue.py), [AppendIntValue.py](/boa3_test/test_sc/list_test/AppendIntValue.py), [AppendIntWithBuiltin.py](/boa3_test/test_sc/list_test/AppendIntWithBuiltin.py), [BoolList.py](/boa3_test/test_sc/list_test/BoolList.py), [ClearList.py](/boa3_test/test_sc/list_test/ClearList.py), [EmptyListAssignment.py](/boa3_test/test_sc/list_test/EmptyListAssignment.py), [ExtendAnyValue.py](/boa3_test/test_sc/list_test/ExtendAnyValue.py), [ExtendTupleValue.py](/boa3_test/test_sc/list_test/ExtendTupleValue.py), [ExtendWithBuiltin.py](/boa3_test/test_sc/list_test/ExtendWithBuiltin.py), [GetValue.py](/boa3_test/test_sc/list_test/GetValue.py), [GetValueNegativeIndex.py](/boa3_test/test_sc/list_test/GetValueNegativeIndex.py), [IntList.py](/boa3_test/test_sc/list_test/IntList.py), [ListOfList.py](/boa3_test/test_sc/list_test/ListOfList.py), [MultipleExpressionsInLine.py](/boa3_test/test_sc/list_test/MultipleExpressionsInLine.py), [Nep5Main.py](/boa3_test/test_sc/list_test/Nep5Main.py), [PopList.py](/boa3_test/test_sc/list_test/PopList.py), [PopListLiteralArgument.py](/boa3_test/test_sc/list_test/PopListLiteralArgument.py), [PopListLiteralNegativeArgument.py](/boa3_test/test_sc/list_test/PopListLiteralNegativeArgument.py), [PopListVariableArgument.py](/boa3_test/test_sc/list_test/PopListVariableArgument.py), [PopListWithoutAssignment.py](/boa3_test/test_sc/list_test/PopListWithoutAssignment.py), [ReverseList.py](/boa3_test/test_sc/list_test/ReverseList.py), [SetValue.py](/boa3_test/test_sc/list_test/SetValue.py), [SetValueNegativeIndex.py](/boa3_test/test_sc/list_test/SetValueNegativeIndex.py), [StrList.py](/boa3_test/test_sc/list_test/StrList.py), [TypeHintAssignment.py](/boa3_test/test_sc/list_test/TypeHintAssignment.py), [VariableList.py](/boa3_test/test_sc/list_test/VariableList.py) |
|✅ | <p>Dict type</p>                                     | <p>`a = {1:'1', 2:'2', 3:'3'}`</p> | [AnyValueDict.py](/boa3_test/test_sc/dict_test/AnyValueDict.py), [DictOfDict.py](/boa3_test/test_sc/dict_test/DictOfDict.py), [EmptyDictAssignment.py](/boa3_test/test_sc/dict_test/EmptyDictAssignment.py), [GetValue.py](/boa3_test/test_sc/dict_test/GetValue.py), [IntKeyDict.py](/boa3_test/test_sc/dict_test/IntKeyDict.py), [KeysDict.py](/boa3_test/test_sc/dict_test/KeysDict.py), [SetValue.py](/boa3_test/test_sc/dict_test/SetValue.py), [StrKeyDict.py](/boa3_test/test_sc/dict_test/StrKeyDict.py), [TypeHintAssignment.py](/boa3_test/test_sc/dict_test/TypeHintAssignment.py), [ValuesDict.py](/boa3_test/test_sc/dict_test/ValuesDict.py), [VariableDict.py](/boa3_test/test_sc/dict_test/VariableDict.py) |
|🔜 | <p>Set type</p>                                      | <p>`a = {'1', '2', '3'}`</p> |  |
|✅ | <p>Bytes type</p>                                    | <p>`a = b'\x01\x02\x03\x04'`</p> | [BytearrayToIntWithBytesBuiltin.py](/boa3_test/test_sc/bytes_test/BytearrayToIntWithBytesBuiltin.py), [BytesFromBytearray.py](/boa3_test/test_sc/bytes_test/BytesFromBytearray.py), [BytesGetValue.py](/boa3_test/test_sc/bytes_test/BytesGetValue.py), [BytesGetValueNegativeIndex.py](/boa3_test/test_sc/bytes_test/BytesGetValueNegativeIndex.py), [BytesLiteral.py](/boa3_test/test_sc/bytes_test/BytesLiteral.py), [BytesToInt.py](/boa3_test/test_sc/bytes_test/BytesToInt.py), [BytesToIntWithBuiltin.py](/boa3_test/test_sc/bytes_test/BytesToIntWithBuiltin.py), [BytesToStr.py](/boa3_test/test_sc/bytes_test/BytesToStr.py), [BytesToStrWithBuiltin.py](/boa3_test/test_sc/bytes_test/BytesToStrWithBuiltin.py) |
|✅ | <p>Bytearray type</p>                                | <p>`a = bytearray(b'\x01\x02\x03\x04')`</p> | [BytearrayAppend.py](/boa3_test/test_sc/bytes_test/BytearrayAppend.py), [BytearrayAppendWithBuiltin.py](/boa3_test/test_sc/bytes_test/BytearrayAppendWithBuiltin.py), [BytearrayAppendWithMutableSequence.py](/boa3_test/test_sc/bytes_test/BytearrayAppendWithMutableSequence.py), [BytearrayClear.py](/boa3_test/test_sc/bytes_test/BytearrayClear.py), [BytearrayFromLiteralBytes.py](/boa3_test/test_sc/bytes_test/BytearrayFromLiteralBytes.py), [BytearrayFromVariableBytes.py](/boa3_test/test_sc/bytes_test/BytearrayFromVariableBytes.py), [BytearrayGetValue.py](/boa3_test/test_sc/bytes_test/BytearrayGetValuet.py), [BytearrayGetValueNegativeIndex.py](/boa3_test/test_sc/bytes_test/BytearrayGetValueNegativeIndex.py), [BytearrayReverse.py](/boa3_test/test_sc/bytes_test/BytearrayReverse.py), [BytearraySetValue.py](/boa3_test/test_sc/bytes_test/BytearraySetValue.py), [BytearraySetValueNegativeIndex.py](/boa3_test/test_sc/bytes_test/BytearraySetValueNegativeIndex.py), [BytearrayToInt.py](/boa3_test/test_sc/bytes_test/BytearrayToInt.py), [BytearrayToIntWithBuiltin.py](/boa3_test/test_sc/bytes_test/BytearrayToIntWithBuiltin.py) |
|✅ | <p>While statement</p>                               | <p>`foo = 0`<br/>`while condition:`<br/>&emsp;`foo = foo + 2`</p> | [ConstantCondition.py](/boa3_test/test_sc/while_test/ConstantCondition.py), [MultipleRelationalCondition.py](/boa3_test/test_sc/while_test/MultipleRelationalCondition.py), [NestedWhile.py](/boa3_test/test_sc/while_test/NestedWhile.py), [RelationalCondition.py](/boa3_test/test_sc/while_test/RelationalCondition.py), [VariableCondition.py](/boa3_test/test_sc/while_test/VariableCondition.py), [WhileBoa2Test.py](/boa3_test/test_sc/while_test/WhileBoa2Test.py), [WhileBoa2Test1.py](/boa3_test/test_sc/while_test/WhileBoa2Test1.py), [WhileBoa2Test2.py](/boa3_test/test_sc/while_test/WhileBoa2Test2.py), [WhileBreak.py](/boa3_test/test_sc/while_test/WhileBreak.py), [WhileBreakElse.py](/boa3_test/test_sc/while_test/WhileBreakElse.py), [WhileContinue.py](/boa3_test/test_sc/while_test/WhileContinue.py), [WhileElse.py](/boa3_test/test_sc/while_test/WhileElse.py) |
|✅ | <p>If, elif, else statements</p>                     | <p>`if condition1:`<br/>&emsp;`foo = 0`<br/>`elif condition2:`<br/>&emsp;`foo = 1`<br/>`else:`<br/>&emsp;`bar = 2`</p>     | [ConstantCondition.py](/boa3_test/test_sc/if_test/ConstantCondition.py), [IfElif.py](/boa3_test/test_sc/if_test/IfElif.py), [IfElse.py](/boa3_test/test_sc/if_test/IfElse.py), [IfExpVariableCondition.py](/boa3_test/test_sc/if_test/IfExpVariableCondition.py), [MultipleBranches.py](/boa3_test/test_sc/if_test/MultipleBranches.py), [NestedIf.py](/boa3_test/test_sc/if_test/NestedIf.py), [RelationalCondition.py](/boa3_test/test_sc/if_test/RelationalCondition.py), [VariableCondition.py](/boa3_test/test_sc/if_test/VariableCondition.py) |
|✅ | <p>For statement</p>                                 | <p>`for x in (1, 2, 3):`<br/>&emsp;`...`</p> | [ForBreak.py](/boa3_test/test_sc/for_test/ForBreak.py), [ForBreakElse.py](/boa3_test/test_sc/for_test/ForBreakElse.py), [ForContinue.py](/boa3_test/test_sc/for_test/ForContinue.py), [ForElse.py](/boa3_test/test_sc/for_test/ForElse.py), [NestedFor.py](/boa3_test/test_sc/for_test/NestedFor.py), [StringCondition.py](/boa3_test/test_sc/for_test/StringCondition.py), [TupleCondition.py](/boa3_test/test_sc/for_test/TupleCondition.py), [VariableCondition.py](/boa3_test/test_sc/for_test/VariableCondition.py) |
|✅ | <p>Function call</p>                                 | <p>`def Main(num: int):`<br/>&emsp;`a = foo(num)`<br/>&emsp;`...`<br/><br/>`def foo(num: int) -> int:`<br/>&emsp;`...`</p> | [CallFunctionWithoutVariables.py](/boa3_test/test_sc/function_test/CallFunctionWithoutVariables.py), [CallFunctionWrittenBefore.py](/boa3_test/test_sc/function_test/CallFunctionWrittenBefore.py), [CallReturnFunctionOnReturn.py](/boa3_test/test_sc/function_test/CallReturnFunctionOnReturn.py), [CallReturnFunctionWithLiteralArgs.py](/boa3_test/test_sc/function_test/CallReturnFunctionWithLiteralArgs.py), [CallReturnFunctionWithoutArgs.py](/boa3_test/test_sc/function_test/CallReturnFunctionWithoutArgs.py), [CallReturnFunctionWithVariableArgs.py](/boa3_test/test_sc/function_test/CallReturnFunctionWithVariableArgs.py), [CallVoidFunctionWithLiteralArgs.py](/boa3_test/test_sc/function_test/CallVoidFunctionWithLiteralArgs.py), [CallVoidFunctionWithoutArgs.py](/boa3_test/test_sc/function_test/CallVoidFunctionWithoutArgs.py), [CallVoidFunctionWithVariableArgs.py](/boa3_test/test_sc/function_test/CallVoidFunctionWithVariableArgs.py) |
|✅ | <p>Built in function</p>                             | <p>`a = len('hello')`</p> | [Folder](/boa3_test/test_sc/built_in_methods_test) with the Examples. |
|🔜 | <p>Built in function</p>                             | <p>`a = abs(-5)`<br/>`b = max(7, 0, 12, 8)`<br/>`c = min(1, 6, 2)`<br/>`d = pow(2, 2)`<br/>`f = sum(list_of_num, 0)`<br/>`g = range(1,5,2)`<br/>`h = reversed([1, 2, 3, 4])`</p> |  |
|✅ | <p>Multiple expressions in the same line<p/>         | <p>`i = i + h; a = 1; b = 3 + a; count = 0`</p> | [MultipleExpressionsInLine (Arithmetic)](/boa3_test/test_sc/arithmetic_test/MultipleExpressionsInLine.py), [MultipleExpressionsInLine (Logical)](/boa3_test/test_sc/logical_test/MultipleExpressionsInLine.py), [MultipleExpressionsInLine (List)](/boa3_test/test_sc/list_test/MultipleExpressionsInLine.py), [MultipleExpressionsInLine (Tuple)](/boa3_test/test_sc/tuple_test/MultipleExpressionsInLine.py), [MultipleExpressionsInLine (Relational)](/boa3_test/test_sc/relational_test/MultipleExpressionsInLine.py) |
|🔜 | <p>Chained assignment<p/>                            | <p>`x = y = foo()`</p> |  |
|✅ | <p>Sequence slicing<p/>                              | <p>`x = 'example'[2:4]`, `x = [1, 2, 3][:2]`, `x = 'example'[4:]`, `x = (1, 2, 3)[:]`, `x = 'example'[-4:-2]`, `x = 'example'[:-4]`</p> | [ListSlicingEndOmitted.py](/boa3_test/test_sc/list_test/ListSlicingEndOmitted.py), [ListSlicingLiteralValues.py](/boa3_test/test_sc/list_test/ListSlicingLiteralValues.py), [ListSlicingNegativeEnd.py](/boa3_test/test_sc/list_test/ListSlicingNegativeEnd.py), [ListSlicingNegativeStart.py](/boa3_test/test_sc/list_test/ListSlicingNegativeStart.py), [ListSlicingOmitted.py](/boa3_test/test_sc/list_test/ListSlicingOmitted.py), [ListSlicingStartOmitted.py](/boa3_test/test_sc/list_test/ListSlicingStartOmitted.py), [ListSlicingVariableValues.py](/boa3_test/test_sc/list_test/ListSlicingVariableValues.py), [StringSlicingEndOmitted.py](/boa3_test/test_sc/string_test/StringSlicingEndOmitted.py), [StringSlicingLiteralValues.py](/boa3_test/test_sc/string_test/StringSlicingLiteralValues.py), [StringSlicingNegativeEnd.py](/boa3_test/test_sc/string_test/StringSlicingNegativeEnd.py), [StringSlicingNegativeStart.py](/boa3_test/test_sc/string_test/StringSlicingNegativeStart.py), [StringSlicingOmitted.py](/boa3_test/test_sc/string_test/StringSlicingOmitted.py), [StringSlicingStartOmitted.py](/boa3_test/test_sc/string_test/StringSlicingStartOmitted.py), [StringSlicingVariableValues.py](/boa3_test/test_sc/string_test/StringSlicingVariableValues.py), [TupleSlicingEndOmitted.py](/boa3_test/test_sc/tuple_test/TupleSlicingEndOmitted.py), [TupleSlicingLiteralValues.py](/boa3_test/test_sc/tuple_test/TupleSlicingLiteralValues.py), [TupleSlicingNegativeEnd.py](/boa3_test/test_sc/tuple_test/TupleSlicingNegativeEnd.py), [TupleSlicingNegativeStart.py](/boa3_test/test_sc/tuple_test/TupleSlicingNegativeStart.py), [TupleSlicingOmitted.py](/boa3_test/test_sc/tuple_test/TupleSlicingOmitted.py), [TupleSlicingStartOmitted.py](/boa3_test/test_sc/tuple_test/TupleSlicingStartOmitted.py), [TupleSlicingVariableValues.py](/boa3_test/test_sc/tuple_test/TupleSlicingVariableValues.py) |
|🔜 | <p>Sequence slicing</p>                              | <p>`x = 'example'[2:4:2]`, `x = 'example'[::2]`</p> |  |
|✅ | <p>Assert</p>                                        | <p>`assert x % 2 == 0`<br/>`assert x % 3 != 2, 'error message'`</p> | [AssertAny.py](/boa3_test/test_sc/assert_test/AssertAny.py), [AssertBinaryOperation.py](/boa3_test/test_sc/assert_test/AssertBinaryOperation.py), [AssertBytes.py](/boa3_test/test_sc/assert_test/AssertBytes.py), [AssertDict.py](/boa3_test/test_sc/assert_test/AssertDict.py), [AssertInt.py](/boa3_test/test_sc/assert_test/AssertInt.py), [AssertList.py](/boa3_test/test_sc/assert_test/AssertList.py), [AssertStr.py](/boa3_test/test_sc/assert_test/AssertStr.py), [AssertUnaryOperation.py](/boa3_test/test_sc/assert_test/AssertUnaryOperation.py), [AssertWithMessage.py](/boa3_test/test_sc/assert_test/AssertWithMessage.py) |
|✅ | <p>Try catch</p>                                     | <p>`try:`<br/>&emsp;`a = foo(b)`<br/>`except Exception as e:`<br/>&emsp;`a = foo(b)`</p> | [TryExceptBaseException.py](/boa3_test/test_sc/exception_test/TryExceptBaseException.py), [TryExceptSpecificException.py](/boa3_test/test_sc/exception_test/TryExceptSpecificException.py), [TryExceptWithoutException.py](/boa3_test/test_sc/exception_test/TryExceptWithoutException.py) |
|🔜 | <p>Continue, break and pass</p>                      |  |  |
|✅ | <p>Import</p>                                        | <p>Only `boa3.builtin` packages are supported right now.</p> | [FromImportTyping.py](/boa3_test/test_sc/import_test/FromImportTyping.py), [FromImportTypingWithAlias.py](/boa3_test/test_sc/import_test/FromImportTypingWithAlias.py), [FromImportUserModule.py](/boa3_test/test_sc/import_test/FromImportUserModule.py), [FromImportUserModuleWithAlias.py](/boa3_test/test_sc/import_test/FromImportUserModuleWithAlias.py), [FromImportVariable.py](/boa3_test/test_sc/import_test/FromImportVariable.py), [FromImportWithGlobalVariables.py](/boa3_test/test_sc/import_test/FromImportWithGlobalVariables.py), [ImportTyping.py](/boa3_test/test_sc/import_test/ImportTyping.py), [ImportTypingWithAlias.py](/boa3_test/test_sc/import_test/ImportTypingWithAlias.py), [ImportUserModule.py](/boa3_test/test_sc/import_test/ImportUserModule.py), [ImportUserModuleWithAlias.py](/boa3_test/test_sc/import_test/ImportUserModuleWithAlias.py) |

## Neo Python Suite Projects

- <b>[neo3-boa](https://github.com/CityOfZion/neo3-boa)</b>: Python smart contracts compiler.</br>
- [neo3-mamba](https://github.com/CityOfZion/neo-mamba): Python SDK for interacting with neo.</br>

## Opening a New Issue

- Open a new [issue](https://github.com/CityOfZion/neo3-boa/issues/new) if you encounter a problem.
- Pull requests are welcome. New features, writing tests and documentation are all needed.


## License

- Open-source [Apache 2.0](https://github.com/CityOfZion/neo3-boa/blob/master/LICENSE).
