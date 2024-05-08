from boa3.internal.exception import CompilerError
from boa3.internal.neo3.contracts import FindOptions
from boa3_test.tests import boatestcase


class TestPythonOperation(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/python_operation_test'

    # region Membership

    async def test_in_bytes(self):
        await self.set_up_contract('BytesIn.py')

        result, _ = await self.call('main', [b'123', b'1234'], return_type=bool)
        self.assertEqual(b'123' in b'1234', result)

        result, _ = await self.call('main', [b'42', b'1234'], return_type=bool)
        self.assertEqual(b'42' in b'1234', result)

        result, _ = await self.call('main', [b'34', b'1234'], return_type=bool)
        self.assertEqual(b'34' in b'1234', result)

    def test_bytes_membership_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'BytesMembershipMismatchedType.py')

    async def test_int_in_bytes(self):
        await self.set_up_contract('BytesMembershipWithInt.py')

        result, _ = await self.call('main', [1, b'1234'], return_type=bool)
        self.assertEqual(1 in b'1234', result)

        result, _ = await self.call('main', [50, b'1234'], return_type=bool)
        self.assertEqual(50 in b'1234', result)

    async def test_in_dict(self):
        await self.set_up_contract('DictIn.py')

        result, _ = await self.call('main', [1, {1: '2', '4': 8}], return_type=bool)
        self.assertEqual(1 in {1: '2', '4': 8}, result)

        result, _ = await self.call('main', ['1', {1: '2', '4': 8}], return_type=bool)
        self.assertEqual('1' in {1: '2', '4': 8}, result)

        result, _ = await self.call('main', [8, {1: '2', '4': 8}], return_type=bool)
        self.assertEqual(8 in {1: '2', '4': 8}, result)

        result, _ = await self.call('main', ['4', {1: '2', '4': 8}], return_type=bool)
        self.assertEqual('4' in {1: '2', '4': 8}, result)

    def test_dict_membership_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'DictMembershipMismatchedType.py')

    async def test_in_list(self):
        await self.set_up_contract('ListIn.py')

        result, _ = await self.call('main', [1, [1, 2, '3', '4']], return_type=bool)
        self.assertEqual(1 in [1, 2, '3', '4'], result)

        result, _ = await self.call('main', [3, [1, 2, '3', '4']], return_type=bool)
        self.assertEqual(3 in [1, 2, '3', '4'], result)

        result, _ = await self.call('main', ['4', [1, 2, '3', '4']], return_type=bool)
        self.assertEqual('4' in [1, 2, '3', '4'], result)

    def test_list_membership_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ListMembershipMismatchedType.py')

    async def test_in_str(self):
        await self.set_up_contract('StringIn.py')

        result, _ = await self.call('main', ['123', '1234'], return_type=bool)
        self.assertEqual('123' in '1234', result)

        result, _ = await self.call('main', ['42', '1234'], return_type=bool)
        self.assertEqual('42' in '1234', result)

    def test_str_membership_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'StringMembershipMismatchedType.py')

    async def test_in_tuple(self):
        await self.set_up_contract('TupleIn.py')

        result, _ = await self.call('main', [1, (1, 2, '3', '4')], return_type=bool)
        self.assertEqual(1 in (1, 2, '3', '4'), result)

        result, _ = await self.call('main', [3, (1, 2, '3', '4')], return_type=bool)
        self.assertEqual(3 in (1, 2, '3', '4'), result)

        result, _ = await self.call('main', ['4', (1, 2, '3', '4')], return_type=bool)
        self.assertEqual('4' in (1, 2, '3', '4'), result)

    def test_tuple_membership_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'TupleMembershipMismatchedType.py')

    async def test_in_typed_dict_builtin_type(self):
        await self.set_up_contract('TypedDictBuiltinTypeIn.py')

        element = FindOptions.VALUES_ONLY
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        result, _ = await self.call('main', [element, dict_], return_type=bool)
        self.assertEqual(element in dict_, result)

        element = FindOptions.PICK_FIELD_0
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        result, _ = await self.call('main', [element, dict_], return_type=bool)
        self.assertEqual(element in dict_, result)

    async def test_in_typed_dict(self):
        await self.set_up_contract('TypedDictIn.py')

        result, _ = await self.call('main', [1, {1: '2', 4: '8'}], return_type=bool)
        self.assertEqual(1 in {1: '2', 4: '8'}, result)

        result, _ = await self.call('main', [3, {1: '2', 4: '8'}], return_type=bool)
        self.assertEqual(3 in {1: '2', 4: '8'}, result)

    async def test_in_typed_list_builtin_type(self):
        await self.set_up_contract('TypedListBuiltinTypeIn.py')

        element = FindOptions.VALUES_ONLY
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        result, _ = await self.call('main', [element, list_], return_type=bool)
        self.assertEqual(element in list_, result)

        element = FindOptions.PICK_FIELD_0
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        result, _ = await self.call('main', [element, list_], return_type=bool)
        self.assertEqual(element in list_, result)

    async def test_in_typed_list(self):
        await self.set_up_contract('TypedListIn.py')

        result, _ = await self.call('main', [1, [1, 2, 3, 4]], return_type=bool)
        self.assertEqual(1 in [1, 2, 3, 4], result)

        result, _ = await self.call('main', [6, [1, 2, 3, 4]], return_type=bool)
        self.assertEqual(6 in [1, 2, 3, 4], result)

    async def test_in_typed_tuple_builtin_type(self):
        await self.set_up_contract('TypedTupleBuiltinTypeIn.py')

        element = FindOptions.VALUES_ONLY
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        result, _ = await self.call('main', [element, tuple_], return_type=bool)
        self.assertEqual(element in tuple_, result)

        element = FindOptions.PICK_FIELD_0
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        result, _ = await self.call('main', [element, tuple_], return_type=bool)
        self.assertEqual(element in tuple_, result)

    async def test_in_typed_tuple(self):
        await self.set_up_contract('TypedTupleIn.py')

        result, _ = await self.call('main', [1, (1, 2, 3, 4)], return_type=bool)
        self.assertEqual(1 in (1, 2, 3, 4), result)

        result, _ = await self.call('main', [6, (1, 2, 3, 4)], return_type=bool)
        self.assertEqual(6 in (1, 2, 3, 4), result)

    # endregion

    # region NotMembership

    async def test_not_in_bytes(self):
        await self.set_up_contract('BytesNotIn.py')

        result, _ = await self.call('main', [b'123', b'1234'], return_type=bool)
        self.assertEqual(b'123' not in b'1234', result)

        result, _ = await self.call('main', [b'42', b'1234'], return_type=bool)
        self.assertEqual(b'42' not in b'1234', result)

    async def test_not_in_dict(self):
        await self.set_up_contract('DictNotIn.py')

        result, _ = await self.call('main', [1, {1: '2', '4': 8}], return_type=bool)
        self.assertEqual(1 not in {1: '2', '4': 8}, result)

        result, _ = await self.call('main', ['1', {1: '2', '4': 8}], return_type=bool)
        self.assertEqual('1' not in {1: '2', '4': 8}, result)

        result, _ = await self.call('main', [8, {1: '2', '4': 8}], return_type=bool)
        self.assertEqual(8 not in {1: '2', '4': 8}, result)

        result, _ = await self.call('main', ['4', {1: '2', '4': 8}], return_type=bool)
        self.assertEqual('4' not in {1: '2', '4': 8}, result)

    async def test_not_in_list(self):
        await self.set_up_contract('ListNotIn.py')

        result, _ = await self.call('main', [1, [1, 2, '3', '4']], return_type=bool)
        self.assertEqual(1 not in [1, 2, '3', '4'], result)

        result, _ = await self.call('main', [3, [1, 2, '3', '4']], return_type=bool)
        self.assertEqual(3 not in [1, 2, '3', '4'], result)

        result, _ = await self.call('main', ['4', [1, 2, '3', '4']], return_type=bool)
        self.assertEqual('4' not in [1, 2, '3', '4'], result)

    async def test_not_in_str(self):
        await self.set_up_contract('StringNotIn.py')

        result, _ = await self.call('main', ['123', '1234'], return_type=bool)
        self.assertEqual('123' not in '1234', result)

        result, _ = await self.call('main', ['42', '1234'], return_type=bool)
        self.assertEqual('42' not in '1234', result)

    async def test_not_in_tuple(self):
        await self.set_up_contract('TupleNotIn.py')

        result, _ = await self.call('main', [1, (1, 2, '3', '4')], return_type=bool)
        self.assertEqual(1 not in (1, 2, '3', '4'), result)

        result, _ = await self.call('main', [3, (1, 2, '3', '4')], return_type=bool)
        self.assertEqual(3 not in (1, 2, '3', '4'), result)

        result, _ = await self.call('main', ['4', (1, 2, '3', '4')], return_type=bool)
        self.assertEqual('4' not in (1, 2, '3', '4'), result)

    async def test_not_in_typed_dict_builtin_type(self):
        await self.set_up_contract('TypedDictBuiltinTypeNotIn.py')

        element = FindOptions.VALUES_ONLY
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        result, _ = await self.call('main', [element, dict_], return_type=bool)
        self.assertEqual(element not in dict_, result)

        element = FindOptions.PICK_FIELD_0
        dict_ = {FindOptions.NONE: 'FindOptions.NONE', FindOptions.DESERIALIZE_VALUES: 'FindOptions.DESERIALIZE_VALUES'}
        result, _ = await self.call('main', [element, dict_], return_type=bool)
        self.assertEqual(element not in dict_, result)

    async def test_not_in_typed_dict(self):
        await self.set_up_contract('TypedDictNotIn.py')

        result, _ = await self.call('main', [1, {1: '2', 4: '8'}], return_type=bool)
        self.assertEqual(1 not in {1: '2', 4: '8'}, result)

        result, _ = await self.call('main', [3, {1: '2', 4: '8'}], return_type=bool)
        self.assertEqual(3 not in {1: '2', 4: '8'}, result)

    async def test_not_in_typed_list_builtin_type(self):
        await self.set_up_contract('TypedListBuiltinTypeNotIn.py')

        element = FindOptions.VALUES_ONLY
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        result, _ = await self.call('main', [element, list_], return_type=bool)
        self.assertEqual(element not in list_, result)

        element = FindOptions.PICK_FIELD_0
        list_ = [FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY]
        result, _ = await self.call('main', [element, list_], return_type=bool)
        self.assertEqual(element not in list_, result)

    async def test_not_in_typed_list(self):
        await self.set_up_contract('TypedListNotIn.py')

        result, _ = await self.call('main', [1, [1, 2, 3, 4]], return_type=bool)
        self.assertEqual(1 not in [1, 2, 3, 4], result)

        result, _ = await self.call('main', [6, [1, 2, 3, 4]], return_type=bool)
        self.assertEqual(6 not in [1, 2, 3, 4], result)

    async def test_not_in_typed_tuple_builtin_type(self):
        await self.set_up_contract('TypedTupleBuiltinTypeNotIn.py')

        element = FindOptions.VALUES_ONLY
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        result, _ = await self.call('main', [element, tuple_], return_type=bool)
        self.assertEqual(element not in tuple_, result)

        element = FindOptions.PICK_FIELD_0
        tuple_ = (FindOptions.NONE, FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES, FindOptions.KEYS_ONLY)
        result, _ = await self.call('main', [element, tuple_], return_type=bool)
        self.assertEqual(element not in tuple_, result)

    async def test_not_in_typed_tuple(self):
        await self.set_up_contract('TypedTupleNotIn.py')

        result, _ = await self.call('main', [1, (1, 2, 3, 4)], return_type=bool)
        self.assertEqual(1 not in (1, 2, 3, 4), result)

        result, _ = await self.call('main', [6, (1, 2, 3, 4)], return_type=bool)
        self.assertEqual(6 not in (1, 2, 3, 4), result)

    # endregion
