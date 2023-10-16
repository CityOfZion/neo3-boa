
============================================
Python compiler for the Neo3 Virtual Machine
============================================

-  `Overview <#overview>`__

   -  `Product Strategy <#product-strategy>`__
-  `Quickstart <#quickstart>`__

   -  `Compiling your Smart Contract <#compiling-your-smart-contract>`__
-  `Docs <#docs>`__
-  `Reference Examples <#reference-examples>`__
-  `License <#license>`__

Overview
--------

Neo3-Boa is a tool for creating Neo Smart Contracts using Python. It compiles `.py` files to `.nef` and `.manifest.json` formats for usage in the `Neo Virtual Machine <https://github.com/neo-project/neo-vm/>`__ which is used to execute contracts on the `Neo Blockchain <https://github.com/neo-project/neo/>`__.

Neo-boa is part of the Neo Python Framework, aimed to allow the full development of dApps using Python alone.

Product Strategy
================

Pure Python
^^^^^^^^^^^
We want Python developers to feel comfortable when trying Neo3-Boa for the first time. It should look and behave like regular Python. For this reason we decided to avoid adding new keywords, but use decorators and helper functions instead.

Neo Python Framework
^^^^^^^^^^^^^^^^^^^^
In the real world, simply coding a smart contract is not enough. Developers need to debug, deploy and invoke it. Therefore, it’s important for this tool to be part of a bigger Python framework. To help the developers and avoid a bad user experience, we need to use logs and inform errors with details.

Testing against Neo VM
^^^^^^^^^^^^^^^^^^^^^^
We need to ensure that the code works as expected, and the only way to do that is to run our tests against the official Neo 3 VM. Neo repository already contains a class called TestEngine that is capable of running tests using C# smart-contracts. It will be adjusted to support compiled smart-contracts.

Maintenance
^^^^^^^^^^^
Create a product that is easy to maintain and upgrade. Use Unit tests, typed and documented code to ensure its maintainability.

Quickstart
----------

Installation requires Python 3.10 or later.

Compiling your Smart Contract
=============================

Using CLI
^^^^^^^^^

::

  $ neo3-boa compile path/to/your/file.py

.. note::  When resolving compilation errors it is recommended to resolve the first reported error and try to compile again. An error can have a cascading effect and throw more errors all caused by the first.

Using Python Script
^^^^^^^^^^^^^^^^^^^

::

  from boa3.boa3 import Boa3

  Boa3.compile_and_save('path/to/your/file.py')

Docs
----
You can `read the docs here <https://docs.coz.io/neo3/boa/index.html>`__. Please check our examples for reference.

Reference Examples
------------------

For an extensive collection of examples:

- `Smart contract examples <https://github.com/CityOfZion/neo3-boa/tree/master/boa3_test/examples>`__
- `Features tests <https://github.com/CityOfZion/neo3-boa/tree/master/boa3_test/test_sc>`__

License
-------

- Open-source `Apache 2.0 <https://github.com/CityOfZion/neo3-boa/blob/master/LICENSE>`__.
