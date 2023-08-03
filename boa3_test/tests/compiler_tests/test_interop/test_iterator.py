from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestIteratorInterop(BoaTest):
    default_folder: str = 'test_sc/interop_test/iterator'

    def test_iterator_create(self):
        path = self.get_contract_path('IteratorCreate.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_iterator_next(self):
        path, _ = self.get_deploy_file_paths('IteratorNext.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        prefix = b'test_iterator_next'
        invokes.append(runner.call_contract(path, 'has_next', prefix))
        expected_results.append(False)

        key = prefix + b'example1'
        runner.call_contract(path, 'store_data', key, 1)
        invokes.append(runner.call_contract(path, 'has_next', prefix))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_iterator_value(self):
        path, _ = self.get_deploy_file_paths('IteratorValue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        prefix = b'test_iterator_value'
        invokes.append(runner.call_contract(path, 'test_iterator', prefix))
        expected_results.append(None)

        key = prefix + b'example1'
        key_str = String.from_bytes(key)
        runner.call_contract(path, 'store_data', key, 1)
        invokes.append(runner.call_contract(path, 'test_iterator', prefix))
        expected_results.append([key_str, '\x01'])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_iterator_value_dict_mismatched_type(self):
        path = self.get_contract_path('IteratorValueMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_import_iterator(self):
        path, _ = self.get_deploy_file_paths('ImportIterator.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'return_iterator'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_interop_iterator(self):
        path, _ = self.get_deploy_file_paths('ImportInteropIterator.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'return_iterator'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_iterator_implicit_typing(self):
        path, _ = self.get_deploy_file_paths('IteratorImplicitTyping.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        prefix = b'test_iterator_'
        prefix_str = String.from_bytes(prefix)
        invokes.append(runner.call_contract(path, 'search_storage', prefix))
        expected_results.append({})

        invokes.append(runner.call_contract(path, 'store', prefix + b'1', 1))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'store', prefix + b'2', 2))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'search_storage', prefix))
        expected_results.append({f'{prefix_str}1': 1, f'{prefix_str}2': 2})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_iterator_value_access(self):
        path, _ = self.get_deploy_file_paths('IteratorValueAccess.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        prefix = b'test_iterator_'
        prefix_str = String.from_bytes(prefix)
        invokes.append(runner.call_contract(path, 'search_storage', prefix))
        expected_results.append({})

        invokes.append(runner.call_contract(path, 'store', prefix + b'1', 1))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'store', prefix + b'2', 2))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'search_storage', prefix))
        expected_results.append({f'{prefix_str}1': 1, f'{prefix_str}2': 2})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
