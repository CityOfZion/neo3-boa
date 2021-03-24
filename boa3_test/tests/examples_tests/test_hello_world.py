from boa3.boa3 import Boa3
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTemplate(BoaTest):

    default_folder: str = 'examples'

    def test_hello_world_compile(self):
        path = self.get_contract_path('HelloWorld.py')
        Boa3.compile(path)

    def test_hello_world_main(self):
        path = self.get_contract_path('HelloWorld.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

        storage_value = engine.storage_get(b'hello', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(b'world', storage_value)
