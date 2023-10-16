from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestReversed(BoaTest):
    default_folder: str = 'test_sc/reversed_test'

    def test_reversed_list_bool(self):
        path, _ = self.get_deploy_file_paths('ReversedListBool.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_bool = [True, True, False]
        invokes.append(runner.call_contract(path, 'main'))

        reversed_list = list(reversed(list_bool))
        expected_results.append(reversed_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reversed_list_bytes(self):
        path, _ = self.get_deploy_file_paths('ReversedListBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_bytes = [b'1', b'2', b'3']
        reversed_list = [String.from_bytes(element) for element in reversed(list_bytes)]

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(reversed_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reversed_list_int(self):
        path, _ = self.get_deploy_file_paths('ReversedListInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_int = [1, 2, 3]
        invokes.append(runner.call_contract(path, 'main'))

        reversed_list = list(reversed(list_int))
        expected_results.append(reversed_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reversed_list_str(self):
        path, _ = self.get_deploy_file_paths('ReversedListStr.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_str = ['neo3-boa', 'unit', 'test']
        invokes.append(runner.call_contract(path, 'main'))

        reversed_list = list(reversed(list_str))
        expected_results.append(reversed_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reversed_list(self):
        path, _ = self.get_deploy_file_paths('ReversedList.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_any = [1, 'string', False]
        invokes.append(runner.call_contract(path, 'main', list_any))

        reversed_list = list(reversed(list_any))
        expected_results.append(reversed_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reversed_string(self):
        path, _ = self.get_deploy_file_paths('ReversedString.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        string = 'unit_test'
        invokes.append(runner.call_contract(path, 'main', string))

        reversed_list = list(reversed(string))
        expected_results.append(reversed_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reversed_bytes(self):
        path, _ = self.get_deploy_file_paths('ReversedBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'unit_test'
        reversed_list = list(reversed(bytes_value))

        invokes.append(runner.call_contract(path, 'main', bytes_value))
        expected_results.append(reversed_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reversed_range(self):
        path, _ = self.get_deploy_file_paths('ReversedRange.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        reversed_list = list(reversed(range(3)))

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(reversed_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reversed_tuple(self):
        path, _ = self.get_deploy_file_paths('ReversedTuple.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        tuple_value = (1, 2, 3)
        reversed_list = list(reversed(tuple_value))

        invokes.append(runner.call_contract(path, 'main', tuple_value))
        expected_results.append(reversed_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_type(self):
        path = self.get_contract_path('ReversedParameterMismatchedType')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
