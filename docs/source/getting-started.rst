1. Getting Started
##################

**Neo3-Boa** is a tool for creating **Neo Smart Contracts using Python**. It compiles ``.py`` files to ``.nef`` and ``.manisfest.json`` formats for usage in the **Neo Virtual Machine** which is used to execute contracts on the **Neo Blockchain**.

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

Test Engine
-----------

Downloading
***********

Clone neo-devpack-dotnet project and compile the TestEngine.

.. note:: 
    Until ``neo-devpack-dotnet#365`` is approved by Neo, you need to clone ``neo-devpack-dotnet`` from ``simplitech:test-engine-executable`` branch

::
    
    $ git clone https://github.com/simplitech/neo-devpack-dotnet.git -b test-engine-executable
    $ dotnet build ./neo-devpack-dotnet/src/Neo.TestEngine/Neo.TestEngine.csproj


Updating
********

Go into the neo-devpack-dotnet, pull and recompile.

::
    
    ${path-to-folder}/neo-devpack-dotnet git pull
    ${path-to-folder}/neo-devpack-dotnet dotnet build ./src/Neo.TestEngine/Neo.TestEngine.csproj

Testing
*******

.. note::
   If you didn't install TestEngine in neo3-boa's root folder, you need to change the value of `TEST_ENGINE_DIRECTORY` in the file ``boa3/env.py``

Create a Python Script, import the TestEngine class, and define a function to test your smart contract. In this function you'll need to call the method run(). Its parameters are the path of the compiled smart contract, the smart contract's method, and the arguments if necessary. Then assert your result to see if it's correct.

Your Python Script should look something like this:

::
    
    from boa3_test.tests.test_classes.testengine import TestEngine
    from boa3.neo.smart_contract.VoidType import VoidType

    def test_hello_world_main():
        root_folder = '{path-to-test-engine-folder}'
        path = '%s/boa3_test/examples/HelloWorld.nef' % root_folder
        engine = TestEngine(root_folder)

        result = engine.run(path, 'Main')
        assert result is VoidType

To run your tests use:

::

    python -m unittest discover boa3_tests