from boa3.exception import CompilerError
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestPythonOperation(BoaTest):

    default_folder: str = 'test_sc/python_operation_test'

    def test_in_str(self):
        path = self.get_contract_path('StringIn.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', '123', '1234')
        self.assertEqual('123' in '1234', result)

        result = self.run_smart_contract(engine, path, 'main', '42', '1234')
        self.assertEqual('42' in '1234', result)

    def test_not_in_str(self):
        path = self.get_contract_path('StringNotIn.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', '123', '1234')
        self.assertEqual('123' not in '1234', result)

        result = self.run_smart_contract(engine, path, 'main', '42', '1234')
        self.assertEqual('42' not in '1234', result)

    def test_str_membership_mismatched_type(self):
        path = self.get_contract_path('StringMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_in_bytes(self):
        path = self.get_contract_path('BytesIn.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', b'123', b'1234')
        self.assertEqual(b'123' in b'1234', result)

        result = self.run_smart_contract(engine, path, 'main', b'42', b'1234')
        self.assertEqual(b'42' in b'1234', result)

        result = self.run_smart_contract(engine, path, 'main', b'34', b'1234')
        self.assertEqual(b'34' in b'1234', result)

    def test_not_in_bytes(self):
        path = self.get_contract_path('BytesNotIn.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', b'123', b'1234')
        self.assertEqual(b'123' not in b'1234', result)

        result = self.run_smart_contract(engine, path, 'main', b'42', b'1234')
        self.assertEqual(b'42' not in b'1234', result)

    def test_int_in_bytes(self):
        path = self.get_contract_path('BytesMembershipWithInt.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, b'1234')
        self.assertEqual(1 in b'1234', result)

        result = self.run_smart_contract(engine, path, 'main', 50, b'1234')
        self.assertEqual(50 in b'1234', result)

    def test_bytes_membership_mismatched_type(self):
        path = self.get_contract_path('BytesMembershipMismatchedType.py')
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

    def test_in_typed_list(self):
        path = self.get_contract_path('TypedListIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, [1, 2, 3, 4])
        self.assertEqual(1 in [1, 2, 3, 4], result)

        result = self.run_smart_contract(engine, path, 'main', 6, [1, 2, 3, 4])
        self.assertEqual(6 in [1, 2, 3, 4], result)

    def test_not_in_list(self):
        path = self.get_contract_path('ListNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, [1, 2, '3', '4'])
        self.assertEqual(1 not in [1, 2, '3', '4'], result)

        result = self.run_smart_contract(engine, path, 'main', 3, [1, 2, '3', '4'])
        self.assertEqual(3 not in [1, 2, '3', '4'], result)

        result = self.run_smart_contract(engine, path, 'main', '4', [1, 2, '3', '4'])
        self.assertEqual('4' not in [1, 2, '3', '4'], result)

    def test_not_in_typed_list(self):
        path = self.get_contract_path('TypedListNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, [1, 2, 3, 4])
        self.assertEqual(1 not in [1, 2, 3, 4], result)

        result = self.run_smart_contract(engine, path, 'main', 6, [1, 2, 3, 4])
        self.assertEqual(6 not in [1, 2, 3, 4], result)

    def test_list_membership_mismatched_type(self):
        path = self.get_contract_path('ListMembershipMismatchedType.py')
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

    def test_in_typed_tuple(self):
        path = self.get_contract_path('TypedTupleIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, (1, 2, 3, 4))
        self.assertEqual(1 in (1, 2, 3, 4), result)

        result = self.run_smart_contract(engine, path, 'main', 6, (1, 2, 3, 4))
        self.assertEqual(6 in (1, 2, 3, 4), result)

    def test_not_in_tuple(self):
        path = self.get_contract_path('TupleNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, (1, 2, '3', '4'))
        self.assertEqual(1 not in (1, 2, '3', '4'), result)

        result = self.run_smart_contract(engine, path, 'main', 3, (1, 2, '3', '4'))
        self.assertEqual(3 not in (1, 2, '3', '4'), result)

        result = self.run_smart_contract(engine, path, 'main', '4', (1, 2, '3', '4'))
        self.assertEqual('4' not in (1, 2, '3', '4'), result)

    def test_not_in_typed_tuple(self):
        path = self.get_contract_path('TypedTupleNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, (1, 2, 3, 4))
        self.assertEqual(1 not in (1, 2, 3, 4), result)

        result = self.run_smart_contract(engine, path, 'main', 6, (1, 2, 3, 4))
        self.assertEqual(6 not in (1, 2, 3, 4), result)

    def test_tuple_membership_mismatched_type(self):
        path = self.get_contract_path('TupleMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

    def test_in_typed_dict(self):
        path = self.get_contract_path('TypedDictIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, {1: '2', 4: '8'})
        self.assertEqual(1 in {1: '2', 4: '8'}, result)

        result = self.run_smart_contract(engine, path, 'main', 3, {1: '2', 4: '8'})
        self.assertEqual(3 in {1: '2', 4: '8'}, result)

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

    def test_not_in_typed_dict(self):
        path = self.get_contract_path('TypedDictNotIn.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 1, {1: '2', 4: '8'})
        self.assertEqual(1 not in {1: '2', 4: '8'}, result)

        result = self.run_smart_contract(engine, path, 'main', 3, {1: '2', 4: '8'})
        self.assertEqual(3 not in {1: '2', 4: '8'}, result)

    def test_dict_membership_mismatched_type(self):
        path = self.get_contract_path('DictMembershipMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
