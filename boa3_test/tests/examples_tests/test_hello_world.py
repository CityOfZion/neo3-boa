from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTemplate(BoaTest):
    default_folder: str = 'examples'

    def test_hello_world_compile(self):
        path = self.get_contract_path('hello_world.py')
        self.compile(path)

    def test_hello_world_main(self):
        path = self.get_contract_path('hello_world.py')
        engine = TestEngine()
        engine.use_contract_custom_name = self._use_custom_name
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

        storage_value = engine.storage_get(b'hello', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(b'world', storage_value)
