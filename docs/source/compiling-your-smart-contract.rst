Compiling your Smart Contract
=============================

Using CLI
^^^^^^^^^

::

    $ neo3-boa path/to/your/file.py

.. note::
   When resolving compilation errors it is recommended to resolve the first reported error and try to compile again. An error can have a cascading effect and throw more errors all caused by the first.


Using Python Script
^^^^^^^^^^^^^^^^^^^

::

    from boa3.boa3 import Boa3

    Boa3.compile_and_save('path/to/your/file.py')
