import json

from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestJsonInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/json'

    def test_json_serialize(self):
        path = self.get_contract_path('JsonSerialize.py')

        engine = TestEngine()
        test_input = {"one": 1, "two": 2, "three": 3}
        expected_result = json.dumps(test_input, separators=(',', ':'))
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

    def test_json_serialize_int(self):
        path = self.get_contract_path('JsonSerializeInt.py')

        engine = TestEngine()
        expected_result = json.dumps(10)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_json_serialize_bool(self):
        path = self.get_contract_path('JsonSerializeBool.py')

        engine = TestEngine()
        expected_result = json.dumps(1)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_json_serialize_str(self):
        path = self.get_contract_path('JsonSerializeStr.py')

        engine = TestEngine()
        expected_result = json.dumps('unit test')
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_json_serialize_bytes(self):
        path = self.get_contract_path('JsonSerializeBytes.py')

        engine = TestEngine()
        # Python does not accept bytes as parameter for json.dumps() method, since string and bytes ends up being the
        # same on Neo, it's being converted to string, before using dumps
        expected_result = json.dumps(String().from_bytes(b'unit test'))
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(expected_result, result)

    def test_json_deserialize(self):
        path = self.get_contract_path('JsonDeserialize.py')

        engine = TestEngine()
        test_input = json.dumps(12345)
        expected_result = json.loads(test_input)
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

        test_input = json.dumps('unit test')
        expected_result = json.loads(test_input)
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

        test_input = json.dumps(True)
        expected_result = json.loads(test_input)
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

    def test_import_json(self):
        path = self.get_contract_path('ImportJson.py')
        engine = TestEngine()

        value = 123
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(value, result)

        value = 'string'
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(value, result)

    def test_import_interop_json(self):
        path = self.get_contract_path('ImportInteropJson.py')
        engine = TestEngine()

        value = 123
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(value, result)

        value = 'string'
        result = self.run_smart_contract(engine, path, 'main', value)
        self.assertEqual(value, result)
