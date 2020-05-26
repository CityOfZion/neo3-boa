<h1 align="center">neo3-boa</h1>
<p align="center">
  Write smart contracts for Neo3 in Python by COZ
</p>



- [Overview](#overview)

## Overview

The `neo3-boa` compiler is a tool for compiling Python files to the `.nef` and `.manisfest.json` formats for usage in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm/) which is used to execute contracts on the [Neo Blockchain](https://github.com/neo-project/neo/).


#### What does it currently do

- Compiles a subset of the Python language to the `.nef` and `.manisfest.json` format for use in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm)

- Works for Python 3.6+

- Convert Functions

- Convert Local Variable Declarations and Assignments 
    
    ```
    foo: int = 42
    bar = foo
    ```
- Convert Number Arithmetic Operations (`+`, `-`, `*`, `/`, `//`, `%`, `**`)

- Convert Number Relational Operations (`==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `is not`)

- Convert Boolean Logic Operations and chained comparisons (`and`, `or`, `not`)

- Convert Tuple type (`get` and `set` operations)

- While Statement

 ```python
foo = 0

    while condition:
        foo = foo + 2

    return foo
 ```

- If, elif, else Statements

```python
if x:
    foo = 0
elif y:
    foo = 1
else:
    bar = 2
```

- `len()` for `str` and `tuple`

#### What will it do

- Log compiler errors and warnings, when main method is analysed, methods inclusions in `.abi` file to work with Neo Debuggers.

- `continue`, `break` and `pass`

- Numeric Arithmetic Augmented assignment Operators (`+=`, `-=`, `*=`, `/=`, `//=`, `%=`)

- Convert List type

- Convert Function Call

```python
def Main(num: int)
    a = foo(num)
    ...

def foo(num: int) -> int
    ...
```

- String Slicing (`x = 'example'[2:4]`)

- For Statement

```python
for x in (1, 2, 3):
    ...
```

- Multiple Expressions in same line (`i = i + h; a = 1; b = 3 + a; count = 0`)
