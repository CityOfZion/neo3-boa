from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo3.contracts import FindOptions
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestPythonOperation(BoaTest):
    default_folder: str = 'test_sc/python_operation_test'

    # region Membership

    def test_in_bytes(self):
        path, _ = self.get_deploy_file_paths('BytesIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', b'123', b'1234'))
        expected_results.append(b'123' in b'1234')

        invokes.append(runner.call_contract(path, 'main', b'42', b'1234'))
        expected_results.append(b'42' in b'1234')

        invokes.append(runner.call_contract(path, 'main', b'34', b'1234'))
        expected_results.append(b'34' in b'1234')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_membership_mismatched_type(self):
        path = self.get_contract_path('BytesMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_int_in_bytes(self):
        path, _ = self.get_deploy_file_paths('BytesMembershipWithInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, b'1234'))
        expected_results.append(1 in b'1234')

        invokes.append(runner.call_contract(path, 'main', 50, b'1234'))
        expected_results.append(50 in b'1234')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_in_dict(self):
        path, _ = self.get_deploy_file_paths('DictIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, {1: '2', '4': 8}))
        expected_results.append(1 in {1: '2', '4': 8})

        invokes.append(runner.call_contract(path, 'main', '1', {1: '2', '4': 8}))
        expected_results.append('1' in {1: '2', '4': 8})

        invokes.append(runner.call_contract(path, 'main', 8, {1: '2', '4': 8}))
        expected_results.append(8 in {1: '2', '4': 8})

        invokes.append(runner.call_contract(path, 'main', '4', {1: '2', '4': 8}))
        expected_results.append('4' in {1: '2', '4': 8})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_membership_mismatched_type(self):
        path = self.get_contract_path('DictMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_in_list(self):
        path, _ = self.get_deploy_file_paths('ListIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, [1, 2, '3', '4']))
        expected_results.append(1 in [1, 2, '3', '4'])

        invokes.append(runner.call_contract(path, 'main', 3, [1, 2, '3', '4']))
        expected_results.append(3 in [1, 2, '3', '4'])

        invokes.append(runner.call_contract(path, 'main', '4', [1, 2, '3', '4']))
        expected_results.append('4' in [1, 2, '3', '4'])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_membership_mismatched_type(self):
        path = self.get_contract_path('ListMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_in_str(self):
        path, _ = self.get_deploy_file_paths('StringIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', '123', '1234'))
        expected_results.append('123' in '1234')

        invokes.append(runner.call_contract(path, 'main', '42', '1234'))
        expected_results.append('42' in '1234')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_membership_mismatched_type(self):
        path = self.get_contract_path('StringMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_in_tuple(self):
        path, _ = self.get_deploy_file_paths('TupleIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, (1, 2, '3', '4')))
        expected_results.append(1 in (1, 2, '3', '4'))

        invokes.append(runner.call_contract(path, 'main', 3, (1, 2, '3', '4')))
        expected_results.append(3 in (1, 2, '3', '4'))

        invokes.append(runner.call_contract(path, 'main', '4', (1, 2, '3', '4')))
        expected_results.append('4' in (1, 2, '3', '4'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_tuple_membership_mismatched_type(self):
        path = self.get_contract_path('TupleMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_in_typed_dict_builtin_type(self):
        path, _ = self.get_deploy_file_paths('TypedDictBuiltinTypeIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        element = FindOptions.VALUES_ONLY
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        invokes.append(runner.call_contract(path, 'main', element, dict_))
        expected_results.append(element in dict_)

        element = FindOptions.PICK_FIELD_0
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        invokes.append(runner.call_contract(path, 'main', element, dict_))
        expected_results.append(element in dict_)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_in_typed_dict(self):
        path, _ = self.get_deploy_file_paths('TypedDictIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, {1: '2', 4: '8'}))
        expected_results.append(1 in {1: '2', 4: '8'})

        invokes.append(runner.call_contract(path, 'main', 3, {1: '2', 4: '8'}))
        expected_results.append(3 in {1: '2', 4: '8'})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_in_typed_list_builtin_type(self):
        path, _ = self.get_deploy_file_paths('TypedListBuiltinTypeIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        element = FindOptions.VALUES_ONLY
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        invokes.append(runner.call_contract(path, 'main', element, list_))
        expected_results.append(element in list_)

        element = FindOptions.PICK_FIELD_0
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        invokes.append(runner.call_contract(path, 'main', element, list_))
        expected_results.append(element in list_)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_in_typed_list(self):
        path, _ = self.get_deploy_file_paths('TypedListIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, [1, 2, 3, 4]))
        expected_results.append(1 in [1, 2, 3, 4])

        invokes.append(runner.call_contract(path, 'main', 6, [1, 2, 3, 4]))
        expected_results.append(6 in [1, 2, 3, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_in_typed_tuple_builtin_type(self):
        path, _ = self.get_deploy_file_paths('TypedTupleBuiltinTypeIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        element = FindOptions.VALUES_ONLY
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        invokes.append(runner.call_contract(path, 'main', element, tuple_))
        expected_results.append(element in tuple_)

        element = FindOptions.PICK_FIELD_0
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        invokes.append(runner.call_contract(path, 'main', element, tuple_))
        expected_results.append(element in tuple_)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_in_typed_tuple(self):
        path, _ = self.get_deploy_file_paths('TypedTupleIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, (1, 2, 3, 4)))
        expected_results.append(1 in (1, 2, 3, 4))

        invokes.append(runner.call_contract(path, 'main', 6, (1, 2, 3, 4)))
        expected_results.append(6 in (1, 2, 3, 4))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region NotMembership

    def test_not_in_bytes(self):
        path, _ = self.get_deploy_file_paths('BytesNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', b'123', b'1234'))
        expected_results.append(b'123' not in b'1234')

        invokes.append(runner.call_contract(path, 'main', b'42', b'1234'))
        expected_results.append(b'42' not in b'1234')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_dict(self):
        path, _ = self.get_deploy_file_paths('DictNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, {1: '2', '4': 8}))
        expected_results.append(1 not in {1: '2', '4': 8})

        invokes.append(runner.call_contract(path, 'main', '1', {1: '2', '4': 8}))
        expected_results.append('1' not in {1: '2', '4': 8})

        invokes.append(runner.call_contract(path, 'main', 8, {1: '2', '4': 8}))
        expected_results.append(8 not in {1: '2', '4': 8})

        invokes.append(runner.call_contract(path, 'main', '4', {1: '2', '4': 8}))
        expected_results.append('4' not in {1: '2', '4': 8})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_list(self):
        path, _ = self.get_deploy_file_paths('ListNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, [1, 2, '3', '4']))
        expected_results.append(1 not in [1, 2, '3', '4'])

        invokes.append(runner.call_contract(path, 'main', 3, [1, 2, '3', '4']))
        expected_results.append(3 not in [1, 2, '3', '4'])

        invokes.append(runner.call_contract(path, 'main', '4', [1, 2, '3', '4']))
        expected_results.append('4' not in [1, 2, '3', '4'])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_str(self):
        path, _ = self.get_deploy_file_paths('StringNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', '123', '1234'))
        expected_results.append('123' not in '1234')

        invokes.append(runner.call_contract(path, 'main', '42', '1234'))
        expected_results.append('42' not in '1234')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_tuple(self):
        path, _ = self.get_deploy_file_paths('TupleNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, (1, 2, '3', '4')))
        expected_results.append(1 not in (1, 2, '3', '4'))

        invokes.append(runner.call_contract(path, 'main', 3, (1, 2, '3', '4')))
        expected_results.append(3 not in (1, 2, '3', '4'))

        invokes.append(runner.call_contract(path, 'main', '4', (1, 2, '3', '4')))
        expected_results.append('4' not in (1, 2, '3', '4'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_typed_dict_builtin_type(self):
        path, _ = self.get_deploy_file_paths('TypedDictBuiltinTypeNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        element = FindOptions.VALUES_ONLY
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        invokes.append(runner.call_contract(path, 'main', element, dict_))
        expected_results.append(element not in dict_)

        element = FindOptions.PICK_FIELD_0
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        invokes.append(runner.call_contract(path, 'main', element, dict_))
        expected_results.append(element not in dict_)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_typed_dict(self):
        path, _ = self.get_deploy_file_paths('TypedDictNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, {1: '2', 4: '8'}))
        expected_results.append(1 not in {1: '2', 4: '8'})

        invokes.append(runner.call_contract(path, 'main', 3, {1: '2', 4: '8'}))
        expected_results.append(3 not in {1: '2', 4: '8'})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_typed_list_builtin_type(self):
        path, _ = self.get_deploy_file_paths('TypedListBuiltinTypeNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        element = FindOptions.VALUES_ONLY
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        invokes.append(runner.call_contract(path, 'main', element, list_))
        expected_results.append(element not in list_)

        element = FindOptions.PICK_FIELD_0
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        invokes.append(runner.call_contract(path, 'main', element, list_))
        expected_results.append(element not in list_)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_typed_list(self):
        path, _ = self.get_deploy_file_paths('TypedListNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, [1, 2, 3, 4]))
        expected_results.append(1 not in [1, 2, 3, 4])

        invokes.append(runner.call_contract(path, 'main', 6, [1, 2, 3, 4]))
        expected_results.append(6 not in [1, 2, 3, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_typed_tuple_builtin_type(self):
        path, _ = self.get_deploy_file_paths('TypedTupleBuiltinTypeNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        element = FindOptions.VALUES_ONLY
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        invokes.append(runner.call_contract(path, 'main', element, tuple_))
        expected_results.append(element not in tuple_)

        element = FindOptions.PICK_FIELD_0
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        invokes.append(runner.call_contract(path, 'main', element, tuple_))
        expected_results.append(element not in tuple_)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_not_in_typed_tuple(self):
        path, _ = self.get_deploy_file_paths('TypedTupleNotIn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, (1, 2, 3, 4)))
        expected_results.append(1 not in (1, 2, 3, 4))

        invokes.append(runner.call_contract(path, 'main', 6, (1, 2, 3, 4)))
        expected_results.append(6 not in (1, 2, 3, 4))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion
