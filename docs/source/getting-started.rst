1. Getting Started
##################

**Neo3-Boa** is a tool for creating **Neo Smart Contracts using Python**. It compiles ``.py`` files to ``.nef`` and ``.manifest.json`` formats for usage in the **Neo Virtual Machine** which is used to execute contracts on the **Neo Blockchain**.

1.1 Installation
================

This version of the compiler requires Python 3.7 or later.

Set Virtual Environment
-----------------------

Make a Python 3 virtual environment and activate it:

On Linux/MacOS:
***************
::
    
    $ python3 -m venv venv
    $ source venv/bin/activate

On Windows:
***********
::
    
    $ python3 -m venv venv
    $ venv\Scripts\activate.bat

Pip Install (Recommended)
-------------------------

::

    pip install neo3-boa

Build From Source (Alternative)
-------------------------------

If neo3-boa is not available via pip, you can build it from source.

::
   
    git clone https://github.com/CityOfZion/neo3-boa.git
    pip install wheel
    pip install -e .

1.2 Creating a New Smart Contract
=================================

.. warning::
    
    **CONTENT MISSING:** Project Scaffold - GitHub `#307 <https://github.com/CityOfZion/neo3-boa/issues/307>`_ and `#308 <https://github.com/CityOfZion/neo3-boa/issues/308>`_


1.3 Compiling your Smart Contract
=================================

Using CLI
---------
::
    
    $ neo3-boa path/to/your/file.py

.. note::
    When resolving compilation errors it is recommended to resolve the first reported error and try to compile again. An error can have a cascading effect and throw more errors all caused by the first.

Using Python Script
-------------------

::

    from boa3.boa3 import Boa3

    Boa3.compile_and_save('path/to/your/file.py')


1.4 Testing and Debugging
=========================

Configuring the Debugger
------------------------

Neo3-boa is compatible with the Neo Debugger. Debugger launch configuration example:

::
    
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

It's necessary to generate the nef debugger info file to use Neo Debugger.

Using CLI
---------
::

    $ neo3-boa path/to/your/file.py -d|--debug

Using Python Script
-------------------

::

    from boa3.boa3 import Boa3

    Boa3.compile_and_save('path/to/your/file.py', debug=True)


Neo Test Runner
---------------

Downloading
***********

Install `Neo-Express <https://www.nuget.org/packages/Neo.Express>`_ and `NeoTestRunner <https://www.nuget.org/packages/Neo.Test.Runner>`_.

::
    
    $ dotnet tool install Neo.Express
    $ dotnet tool install Neo.Test.Runner


Testing
*******

Create a Python Script, import the NeoTestRunner class, and define a function to test your smart contract. In this function you'll need to call the method call_contract(). Its parameters are the path of the compiled smart contract, the smart contract's method, and the arguments if necessary. Then assert the result to see if it's correct.

Your Python Script should look something like this:

::
    
    from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner

    def test_hello_world_main():
        neoxp_folder = '{path-to-neo-express-directory}'
        path = '%s/boa3_test/examples/HelloWorld.nef' % root_folder
        runner = NeoTestRunner(neoxp_folder)

        invoke = runner.call_contract(path, 'Main')
        runner.execute()
        assert invoke.result is None

To run all tests run the python script at boa3_test/tests/run_unit_tests.py
