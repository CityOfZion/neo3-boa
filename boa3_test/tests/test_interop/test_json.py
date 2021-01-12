import json

from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestJsonInterop(BoaTest):

    def test_json_serialize(self):
        path = '%s/boa3_test/test_sc/interop_test/json/JsonSerialize.py' % self.dirname

        engine = TestEngine(self.dirname)
        test_input = {"one": 1, "two": 2, "three": 3}
        expected_result = String(json.dumps(test_input, separators=(',', ':'))).to_bytes()
        result = self.run_smart_contract(engine, path, 'main', test_input,
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_json_serialize_int(self):
        path = '%s/boa3_test/test_sc/interop_test/json/JsonSerializeInt.py' % self.dirname

        engine = TestEngine(self.dirname)
        expected_result = String(json.dumps(10)).to_bytes()
        result = self.run_smart_contract(engine, path, 'main',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_json_serialize_bool(self):
        path = '%s/boa3_test/test_sc/interop_test/json/JsonSerializeBool.py' % self.dirname

        engine = TestEngine(self.dirname)
        expected_result = String(json.dumps(1)).to_bytes()
        result = self.run_smart_contract(engine, path, 'main',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_json_serialize_str(self):
        path = '%s/boa3_test/test_sc/interop_test/json/JsonSerializeStr.py' % self.dirname

        engine = TestEngine(self.dirname)
        expected_result = String(json.dumps('unit test')).to_bytes()
        result = self.run_smart_contract(engine, path, 'main',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_json_serialize_bytes(self):
        path = '%s/boa3_test/test_sc/interop_test/json/JsonSerializeBytes.py' % self.dirname

        engine = TestEngine(self.dirname)
        expected_result = b'"unit test"'
        result = self.run_smart_contract(engine, path, 'main',
                                         expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_json_deserialize(self):
        path = '%s/boa3_test/test_sc/interop_test/json/JsonDeserialize.py' % self.dirname

        engine = TestEngine(self.dirname)
        test_input = String(json.dumps(12345)).to_bytes()
        expected_result = json.loads(test_input)
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

        test_input = String(json.dumps('unit test')).to_bytes()
        expected_result = json.loads(test_input)
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)

        test_input = String(json.dumps(True)).to_bytes()
        expected_result = json.loads(test_input)
        result = self.run_smart_contract(engine, path, 'main', test_input)
        self.assertEqual(expected_result, result)
