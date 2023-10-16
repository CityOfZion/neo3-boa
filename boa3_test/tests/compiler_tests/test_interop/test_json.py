import json

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestJsonInterop(BoaTest):
    default_folder: str = 'test_sc/interop_test/json'

    def test_json_serialize(self):
        path, _ = self.get_deploy_file_paths('JsonSerialize.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_input = {"one": 1, "two": 2, "three": 3}
        expected_result = json.dumps(test_input, separators=(',', ':'))
        invokes.append(runner.call_contract(path, 'main', test_input))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_serialize_int(self):
        path, _ = self.get_deploy_file_paths('JsonSerializeInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = json.dumps(10)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_serialize_bool(self):
        path, _ = self.get_deploy_file_paths('JsonSerializeBool.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = json.dumps(True)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_serialize_str(self):
        path, _ = self.get_deploy_file_paths('JsonSerializeStr.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = json.dumps('unit test')
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_serialize_bytes(self):
        path, _ = self.get_deploy_file_paths('JsonSerializeBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        # Python does not accept bytes as parameter for json.dumps() method, since string and bytes ends up being the
        # same on Neo, it's being converted to string, before using dumps
        expected_result = json.dumps(String().from_bytes(b'unit test'))
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_json_deserialize(self):
        path, _ = self.get_deploy_file_paths('JsonDeserialize.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_input = json.dumps(12345)
        expected_result = json.loads(test_input)
        invokes.append(runner.call_contract(path, 'main', test_input))
        expected_results.append(expected_result)

        test_input = json.dumps('unit test')
        expected_result = json.loads(test_input)
        invokes.append(runner.call_contract(path, 'main', test_input))
        expected_results.append(expected_result)

        test_input = json.dumps(True)
        expected_result = json.loads(test_input)
        invokes.append(runner.call_contract(path, 'main', test_input))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_json(self):
        path, _ = self.get_deploy_file_paths('ImportJson.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = 123
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(value)

        value = 'string'
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_interop_json(self):
        path, _ = self.get_deploy_file_paths('ImportInteropJson.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = 123
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(value)

        value = 'string'
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
