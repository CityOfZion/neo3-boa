TestEngine
==========

Downloading
^^^^^^^^^^^

Clone neo-devpack-dotnet on neo3-boa root folder and compile the TestEngine.

::

    $ git clone https://github.com/simplitech/neo-devpack-dotnet.git -b test-engine-executable --single-branch
    $ dotnet build ./neo-devpack-dotnet/src/Neo.TestEngine/Neo.TestEngine.csproj -o ./Neo.TestEngine

Updating
^^^^^^^^

Go into the neo-devpack-dotnet, pull and recompile.

::

    ${path-to-folder}/neo-devpack-dotnet git pull
    ${path-to-folder}/neo-devpack-dotnet dotnet build ./src/Neo.TestEngine/Neo.TestEngine.csproj -o ./Neo.TestEngine

Testing
^^^^^^^

Create a Python Script, import the TestEngine class, and define a function to test your smart contract. In this function
you'll need to call the method `run()`. Its parameters are the path of the compiled smart contract, the smart
contract's method, and the arguments if necessary. Then assert your result to see if it's correct.

Your Python Script should look something like this:

::

    from boa3_test.tests.test_classes.testengine import TestEngine
    from boa3.neo.smart_contract.VoidType import VoidType

    def test_hello_world_main():
        root_folder = '{path-to-folder}'
        path = '%s/boa3_test/examples/HelloWorld.nef' % root_folder
        engine = TestEngine(root_folder)

        result = engine.run(path, 'Main')
        assert result is VoidType
