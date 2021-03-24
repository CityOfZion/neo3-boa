
============================================
Python compiler for the Neo3 Virtual Machine
============================================

-  `Overview <#overview>`__

Overview
--------

The ``neo3-boa`` compiler is a tool for compiling Python files to the
``.nef`` and ``.manisfest.json`` formats for usage in the `Neo Virtual
Machine <https://github.com/neo-project/neo-vm/>`__ which is used to
execute contracts on the `Neo
Blockchain <https://github.com/neo-project/neo/>`__.

What it currently does...
^^^^^^^^^^^^^^^^^^^^^^^^^

-  Compiles a subset of the Python language to the ``.nef`` and
   ``.manisfest.json`` format for use in the `Neo Virtual
   Machine <https://github.com/neo-project/neo-vm>`__

-  Works for Python 3.7+

-  Logs compiler errors and warnings

-  Logs when the main method is analysed

-  Logs method inclusions in ``.abi`` file to work with Neo Debuggers.

-  Converts Functions

-  Converts Local Variable Declarations and Assignments

.. code:: python

    foo: int = 42
    bar = foo

-  Converts Number Arithmetic Operations (``+``, ``-``, ``*``, ``//``,
   ``%``)

-  Converts Numeric Arithmetic Augmented assignment Operators (``+=``,
   ``-=``, ``*=``, ``//=``, ``%=``)

-  Converts Relational Operations (``==``, ``!=``, ``<``, ``<=``, ``>``,
   ``>=``)

-  Converts Boolean Logic Operations and chained comparisons (``and``,
   ``or``, ``not``)

-  Converts Tuple type (``get`` and ``set`` operations)

-  Converts List type

-  Converts While Statement

.. code:: python

    foo = 0
    while condition:
        foo = foo + 2

-  Converts If, elif, else Statements

.. code:: python

    if condition1:
        foo = 0
    elif condition2:
        foo = 1
    else:
        bar = 2

-  Converts For Statement

.. code:: python

    for x in (1, 2, 3):
        ...

-  Converts Function Call

.. code:: python

    def Main(num: int):
        a = foo(num)
        ...

    def foo(num: int) -> int:
        ...

-  Converts ``len()`` for ``str``, ``tuple`` and ``list``

-  Converts Multiple Expressions in the same line
   (``i = i + h; a = 1; b = 3 + a; count = 0``)

-  Converts String Slicing (``x = 'example'[2:4]``,
   ``x = 'example'[:4]``, ``x = 'example'[4:]``, ``x = 'example'[:]``)

What it will do...
^^^^^^^^^^^^^^^^^^

-  ``continue``, ``break`` and ``pass``

-  Convert Numeric Arithmetic Augmented assignment Operators (``/=``)

-  Convert Number Arithmetic Operations (``/``, ``**``)

-  Convert Relational Operations (``is``, ``is not``)

-  Convert String Slicing (``x = 'example'[2:4:2]``,
   ``x = 'example'[::2]``)
