4. Code Reference
#################

4.1 Examples
============

For an extensive collection of examples:

- `Smart Contract Examples <https://github.com/CityOfZion/neo3-boa/blob/development/boa3_test/examples>`_
- `Feature Tests <https://github.com/CityOfZion/neo3-boa/blob/development/boa3_test/test_sc>`_

4.2 Supported & Planned Python Features
=======================================

Variable Declarations
---------------------

.. list-table::
   :widths: 3 47 47
   :header-rows: 1
   :align: center

   * - Status
     - Feature
     - Sample
   * - ✅
     - Local variable declarations and assignments
     - ::

         def func():
            foo: int = 42
            bar = foo
   * - ✅
     - Global variable declarations and assignments
     - ::

          foo: int = 42
          bar = foo
   * - ✅
     - Global keyword
     - ::

          foo: int = 42
          bar = foo


          def func():
            global foo
            foo = 1

Operations
----------

.. list-table::
   :widths: 3 47 47
   :header-rows: 1
   :align: center

   * - Status
     - Feature
     - Sample
   * - ✅
     - Arithmetic operations
     - ::

         +, -, *, //, %, **
   * - 🔜
     - Arithmetic operations
     - ::

         /
   * - ✅
     - Arithmetic augmented assignment operators
     - ::

         +=, -=, *=, //=, %=, **=
   * - 🔜
     - Arithmetic augmented assignment operators
     - ::

         /=
   * - ✅
     - Relational operations
     - ::

         ==, !=, <, <=, >, >=, 
         is None, is not None,
         is, is not
   * - ✅
     - Bitwise operations
     - ::

         &, |, ~, ^, <<, >>
   * - ✅
     - Bitwise augmented assignment operators
     - ::

         &=, |=, ~=, ^=, <<=, >>=
   * - ✅
     - Boolean logic operations
     - ::

         and, or, not

Types
-----

.. list-table::
   :widths: 3 47 47
   :header-rows: 1
   :align: center

   * - Status
     - Feature
     - Sample
   * - ✅
     - Tuple type
     - ::

         a = ('1', '2', '3')
   * - ✅
     - List type
     - ::

         a = ['1', '2', '3']
         a.pop()
         a.remove(1)
         a.insert('example', 2)
   * - ✅
     - Dict type
     - ::

         a = {1:'1', 2:'2', 3:'3'}
   * - 🔜
     - Set type
     - ::

         a = {'1', '2', '3'}
   * - ✅
     - Bytes type
     - ::

         a = b'\x01\x02\x03\x04'
   * - ✅
     - Bytearray type
     - ::

         a = bytearray(b'\x01\x02\x03\x04')
   * - ✅
     - Optional type
     - ::

         a: Optional[int] = 5
         a = 142
         a = None
   * - ✅
     - Union type
     - ::

         a: Union[int, str] = 5
         a = 142
         a = 'example'

Control Flow Statements
-----------------------

.. list-table::
   :widths: 3 47 47
   :header-rows: 1
   :align: center

   * - Status
     - Feature
     - Sample
   * - ✅
     - While statement
     - ::

         foo = 0
         while condition:
          foo = foo + 2
   * - ✅
     - If, elif, else statements
     - ::

         if condition1:
          foo = 0
         elif condition2:
          foo = 1
         else:
          bar = 2
   * - ✅
     - For statement
     - ::

         for x in (1, 2, 3):
          ...
   * - ✅
     - Try except
     - ::

         try:
          a = foo(b)
         except Exception as e:
          a = foo(b)
   * - ✅
     - Try except with finally
     - ::

         try:
          a = foo(b)
         except Exception as e:
          a = zubs(b)
         finally:
          b = zubs(a)

Functions
---------

.. list-table::
   :widths: 3 47 47
   :header-rows: 1
   :align: center

   * - Status
     - Feature
     - Sample
   * - ✅
     - Function call
     - ::

         def Main(num: int):
          a = foo(num)
          ...
         
         def foo(num: int) -> int:
          ...
   * - ✅
     - Built in functions
     - ::

         a = len('hello')
         b = range(1, 5, 2)
         c = isinstance(5, str)
         print(42)
         d = abs(-5)
         e = max(7, 12)
         f = max(7, 0, 12, 8)
         g = min(1, 6)
         h = min(1, 6, 2)
         i = sum(list_of_num, 0)
         j = reversed([1, 2, 3, 4])
         k = pow(2, 2)

Other Features
--------------

.. list-table::
   :widths: 3 47 47
   :header-rows: 1
   :align: center

   * - Status
     - Feature
     - Sample
   * - ✅
     - Multiple expressions in the same line
     - ::

         i = i + h; a = 1; b = 3 + a; count = 0
   * - ✅
     - Chained assignment
     - ::

         x = y = foo()
   * - ✅
     - Sequence slicing
     - ::

         x = 'example'[2:4]
         x = [1, 2, 3][:2]
         x = 'example'[4:]
         x = (1, 2, 3)[:]
         x = 'example'[-4:-2]
         x = 'example'[:-4]
         x = 'example'[2:4:2]
         x = 'example'[::2]
   * - ✅
     - Assert
     - ::

         assert x % 2 == 0
         assert x % 3 != 2, 'error message'
   * - ✅
     - Continue, break
     - 
   * - 🔜
     - Pass
     - 
   * - ✅
     - Import
     -
       - Support to ``boa3.builtin`` packages
       - Support to user created modules.
   * - ✅
     - Class
     - ::

         class Foo:
           def __init__(self, bar: Any):
             pass
