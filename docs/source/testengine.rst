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

Create a Python Script, import the TestEngine and BoaTest class, make a Test class that inherits BoaTest, and define a
method to test your smart contract. In this method you'll need to call `self.run_smart_contract()` and then assert to
see if your result is right.

Your Python Script should look something like this:

::

    from boa3_test.tests.boa_test import BoaTest
    from boa3_test.tests.test_classes.testengine import TestEngine

    class TestHelloWorld(BoaTest):
        def test_hello_world_main(self):
            path = '%s/boa3_test/examples/HelloWorld.py' % self.dirname
            engine = TestEngine(self.dirname)

            result = self.run_smart_contract(engine, path, 'Main')
            self.assertIsVoid(result)

Be sure to give `run_smart_contract()` a read to understand its parameters and check the plethora of `tests`_ if the
TestEngine usage is still unclear.

.. note::
    If you modify your smart contract, and the .nef file still exists, BoaTest won't automatically compile your contract again. Therefore, you should compile your contract whenever you change something in it and want to test it once more.

.. _tests: https://github.com/CityOfZion/neo3-boa/blob/development/boa3_test/tests/