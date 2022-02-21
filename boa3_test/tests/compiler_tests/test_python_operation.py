from boa3.exception import CompilerError
from boa3.neo3.contracts import FindOptions
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestPythonOperation(BoaTest):
    default_folder: str = 'test_sc/python_operation_test'

    # region Membership

    def test_in_bytes(self):
        path = self.get_contract_path('BytesIn.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', b'123', b'1234')
        self.assertEqual(b'123' in b'1234', result)

        result = self.run_smart_contract(engine, path, 'main', b'42', b'1234')
        self.assertEqual(b'42' in b'1234', result)

        result = self.run_smart_contract(engine, path, 'main', b'34', b'1234')
        self.assertEqual(b'34' in b'1234', result)

    def test_bytes_membership_mismatched_type(self):
        path = self.get_contract_path('BytesMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_int_in_bytes(self):
        path = self.get_contract_path('BytesMembershipWithInt.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, b'1234')
        self.assertEqual(1 in b'1234', result)

        result = self.run_smart_contract(engine, path, 'main', 50, b'1234')
        self.assertEqual(50 in b'1234', result)

    def test_in_dict(self):
        path = self.get_contract_path('DictIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, {1: '2', '4': 8})
        self.assertEqual(1 in {1: '2', '4': 8}, result)

        result = self.run_smart_contract(engine, path, 'main', '1', {1: '2', '4': 8})
        self.assertEqual('1' in {1: '2', '4': 8}, result)

        result = self.run_smart_contract(engine, path, 'main', 8, {1: '2', '4': 8})
        self.assertEqual(8 in {1: '2', '4': 8}, result)

        result = self.run_smart_contract(engine, path, 'main', '4', {1: '2', '4': 8})
        self.assertEqual('4' in {1: '2', '4': 8}, result)

    def test_dict_membership_mismatched_type(self):
        path = self.get_contract_path('DictMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_in_list(self):
        path = self.get_contract_path('ListIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, [1, 2, '3', '4'])
        self.assertEqual(1 in [1, 2, '3', '4'], result)

        result = self.run_smart_contract(engine, path, 'main', 3, [1, 2, '3', '4'])
        self.assertEqual(3 in [1, 2, '3', '4'], result)

        result = self.run_smart_contract(engine, path, 'main', '4', [1, 2, '3', '4'])
        self.assertEqual('4' in [1, 2, '3', '4'], result)

    def test_list_membership_mismatched_type(self):
        path = self.get_contract_path('ListMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_in_str(self):
        path = self.get_contract_path('StringIn.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', '123', '1234')
        self.assertEqual('123' in '1234', result)

        result = self.run_smart_contract(engine, path, 'main', '42', '1234')
        self.assertEqual('42' in '1234', result)

    def test_str_membership_mismatched_type(self):
        path = self.get_contract_path('StringMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_in_tuple(self):
        path = self.get_contract_path('TupleIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, (1, 2, '3', '4'))
        self.assertEqual(1 in (1, 2, '3', '4'), result)

        result = self.run_smart_contract(engine, path, 'main', 3, (1, 2, '3', '4'))
        self.assertEqual(3 in (1, 2, '3', '4'), result)

        result = self.run_smart_contract(engine, path, 'main', '4', (1, 2, '3', '4'))
        self.assertEqual('4' in (1, 2, '3', '4'), result)

    def test_tuple_membership_mismatched_type(self):
        path = self.get_contract_path('TupleMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_in_typed_dict_builtin_type(self):
        path = self.get_contract_path('TypedDictBuiltinTypeIn.py')
        engine = TestEngine()

        element = FindOptions.VALUES_ONLY
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        result = self.run_smart_contract(engine, path, 'main', element, dict_)
        self.assertEqual(element in dict_, result)

        element = FindOptions.PICK_FIELD_0
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        result = self.run_smart_contract(engine, path, 'main', element, dict_)
        self.assertEqual(element in dict_, result)

    def test_in_typed_dict(self):
        path = self.get_contract_path('TypedDictIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, {1: '2', 4: '8'})
        self.assertEqual(1 in {1: '2', 4: '8'}, result)

        result = self.run_smart_contract(engine, path, 'main', 3, {1: '2', 4: '8'})
        self.assertEqual(3 in {1: '2', 4: '8'}, result)

    def test_in_typed_list_builtin_type(self):
        path = self.get_contract_path('TypedListBuiltinTypeIn.py')
        engine = TestEngine()

        element = FindOptions.VALUES_ONLY
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        result = self.run_smart_contract(engine, path, 'main', element, list_)
        self.assertEqual(element in list_, result)

        element = FindOptions.PICK_FIELD_0
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        result = self.run_smart_contract(engine, path, 'main', element, list_)
        self.assertEqual(element in list_, result)

    def test_in_typed_list(self):
        path = self.get_contract_path('TypedListIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, [1, 2, 3, 4])
        self.assertEqual(1 in [1, 2, 3, 4], result)

        result = self.run_smart_contract(engine, path, 'main', 6, [1, 2, 3, 4])
        self.assertEqual(6 in [1, 2, 3, 4], result)

    def test_in_typed_tuple_builtin_type(self):
        path = self.get_contract_path('TypedTupleBuiltinTypeIn.py')
        engine = TestEngine()

        element = FindOptions.VALUES_ONLY
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        result = self.run_smart_contract(engine, path, 'main', element, tuple_)
        self.assertEqual(element in tuple_, result)

        element = FindOptions.PICK_FIELD_0
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        result = self.run_smart_contract(engine, path, 'main', element, tuple_)
        self.assertEqual(element in tuple_, result)

    def test_in_typed_tuple(self):
        path = self.get_contract_path('TypedTupleIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, (1, 2, 3, 4))
        self.assertEqual(1 in (1, 2, 3, 4), result)

        result = self.run_smart_contract(engine, path, 'main', 6, (1, 2, 3, 4))
        self.assertEqual(6 in (1, 2, 3, 4), result)

    # endregion

    # region NotMembership

    def test_not_in_bytes(self):
        path = self.get_contract_path('BytesNotIn.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', b'123', b'1234')
        self.assertEqual(b'123' not in b'1234', result)

        result = self.run_smart_contract(engine, path, 'main', b'42', b'1234')
        self.assertEqual(b'42' not in b'1234', result)

    def test_not_in_dict(self):
        path = self.get_contract_path('DictNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, {1: '2', '4': 8})
        self.assertEqual(1 not in {1: '2', '4': 8}, result)

        result = self.run_smart_contract(engine, path, 'main', '1', {1: '2', '4': 8})
        self.assertEqual('1' not in {1: '2', '4': 8}, result)

        result = self.run_smart_contract(engine, path, 'main', 8, {1: '2', '4': 8})
        self.assertEqual(8 not in {1: '2', '4': 8}, result)

        result = self.run_smart_contract(engine, path, 'main', '4', {1: '2', '4': 8})
        self.assertEqual('4' not in {1: '2', '4': 8}, result)

    def test_not_in_list(self):
        path = self.get_contract_path('ListNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, [1, 2, '3', '4'])
        self.assertEqual(1 not in [1, 2, '3', '4'], result)

        result = self.run_smart_contract(engine, path, 'main', 3, [1, 2, '3', '4'])
        self.assertEqual(3 not in [1, 2, '3', '4'], result)

        result = self.run_smart_contract(engine, path, 'main', '4', [1, 2, '3', '4'])
        self.assertEqual('4' not in [1, 2, '3', '4'], result)

    def test_not_in_str(self):
        path = self.get_contract_path('StringNotIn.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', '123', '1234')
        self.assertEqual('123' not in '1234', result)

        result = self.run_smart_contract(engine, path, 'main', '42', '1234')
        self.assertEqual('42' not in '1234', result)

    def test_not_in_tuple(self):
        path = self.get_contract_path('TupleNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, (1, 2, '3', '4'))
        self.assertEqual(1 not in (1, 2, '3', '4'), result)

        result = self.run_smart_contract(engine, path, 'main', 3, (1, 2, '3', '4'))
        self.assertEqual(3 not in (1, 2, '3', '4'), result)

        result = self.run_smart_contract(engine, path, 'main', '4', (1, 2, '3', '4'))
        self.assertEqual('4' not in (1, 2, '3', '4'), result)

    def test_not_in_typed_dict_builtin_type(self):
        path = self.get_contract_path('TypedDictBuiltinTypeNotIn.py')
        engine = TestEngine()

        element = FindOptions.VALUES_ONLY
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        result = self.run_smart_contract(engine, path, 'main', element, dict_)
        self.assertEqual(element not in dict_, result)

        element = FindOptions.PICK_FIELD_0
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        result = self.run_smart_contract(engine, path, 'main', element, dict_)
        self.assertEqual(element not in dict_, result)

    def test_not_in_typed_dict(self):
        path = self.get_contract_path('TypedDictNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, {1: '2', 4: '8'})
        self.assertEqual(1 not in {1: '2', 4: '8'}, result)

        result = self.run_smart_contract(engine, path, 'main', 3, {1: '2', 4: '8'})
        self.assertEqual(3 not in {1: '2', 4: '8'}, result)

    def test_not_in_typed_list_builtin_type(self):
        path = self.get_contract_path('TypedListBuiltinTypeNotIn.py')
        engine = TestEngine()

        element = FindOptions.VALUES_ONLY
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        result = self.run_smart_contract(engine, path, 'main', element, list_)
        self.assertEqual(element not in list_, result)

        element = FindOptions.PICK_FIELD_0
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        result = self.run_smart_contract(engine, path, 'main', element, list_)
        self.assertEqual(element not in list_, result)

    def test_not_in_typed_list(self):
        path = self.get_contract_path('TypedListNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, [1, 2, 3, 4])
        self.assertEqual(1 not in [1, 2, 3, 4], result)

        result = self.run_smart_contract(engine, path, 'main', 6, [1, 2, 3, 4])
        self.assertEqual(6 not in [1, 2, 3, 4], result)

    def test_not_in_typed_tuple_builtin_type(self):
        path = self.get_contract_path('TypedTupleBuiltinTypeNotIn.py')
        engine = TestEngine()

        element = FindOptions.VALUES_ONLY
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        result = self.run_smart_contract(engine, path, 'main', element, tuple_)
        self.assertEqual(element not in tuple_, result)

        element = FindOptions.PICK_FIELD_0
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        result = self.run_smart_contract(engine, path, 'main', element, tuple_)
        self.assertEqual(element not in tuple_, result)

    def test_not_in_typed_tuple(self):
        path = self.get_contract_path('TypedTupleNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, (1, 2, 3, 4))
        self.assertEqual(1 not in (1, 2, 3, 4), result)

        result = self.run_smart_contract(engine, path, 'main', 6, (1, 2, 3, 4))
        self.assertEqual(6 not in (1, 2, 3, 4), result)

    # endregion
