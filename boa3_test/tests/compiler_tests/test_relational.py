from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.contracts import FindOptions
from boa3_test.tests import boatestcase


class TestRelational(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/relational_test'

    # region GreaterThan

    async def test_builtin_type_greater_than_operation(self):
        await self.set_up_contract('BuiltinTypeGreaterThan.py')

        result, _ = await self.call('main', [FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES], return_type=bool)
        self.assertEqual(FindOptions.VALUES_ONLY > FindOptions.DESERIALIZE_VALUES, result)

    def test_mixed_greater_than_operation(self):
        path = self.get_contract_path('MixedGreaterThan.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_number_greater_than_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GT
            + Opcode.RET
        )

        output, _ = self.assertCompile('NumGreaterThan.py')
        self.assertEqual(expected_output, output)

    async def test_number_greater_than_operation_run(self):
        await self.set_up_contract('NumGreaterThan.py')

        result, _ = await self.call('Main', [1, 2], return_type=bool)
        self.assertEqual(1 > 2, result)

        result, _ = await self.call('Main', [2, 2], return_type=bool)
        self.assertEqual(2 > 2, result)

        result, _ = await self.call('Main', [2, 1], return_type=bool)
        self.assertEqual(2 > 1, result)

    def test_string_greater_than_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.PUSHM1
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('StrGreaterThan.py')
        self.assertEqual(expected_output, output)

    async def test_string_greater_than_operation_run(self):
        await self.set_up_contract('StrGreaterThan.py')

        result, _ = await self.call('Main', ['test', 'unit'], return_type=bool)
        self.assertEqual('test' > 'unit', result)

        result, _ = await self.call('Main', ['unit', 'unit'], return_type=bool)
        self.assertEqual('unit' > 'unit', result)

        result, _ = await self.call('Main', ['unit', 'test'], return_type=bool)
        self.assertEqual('unit' > 'test', result)

    # endregion

    # region GreaterThanOrEqual

    async def test_builtin_type_greater_than_or_equal_operation(self):
        await self.set_up_contract('BuiltinTypeGreaterThanOrEqual.py')

        result, _ = await self.call('main', [FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY], return_type=bool)
        self.assertEqual(FindOptions.VALUES_ONLY >= FindOptions.VALUES_ONLY, result)

    def test_mixed_greater_or_equal_than_operation(self):
        path = self.get_contract_path('MixedGreaterOrEqual.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_number_greater_or_equal_than_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GE
            + Opcode.RET
        )

        output, _ = self.assertCompile('NumGreaterOrEqual.py')
        self.assertEqual(expected_output, output)

    async def test_number_greater_or_equal_than_operation_run(self):
        await self.set_up_contract('NumGreaterOrEqual.py')

        result, _ = await self.call('Main', [1, 2], return_type=bool)
        self.assertEqual(1 >= 2, result)

        result, _ = await self.call('Main', [2, 2], return_type=bool)
        self.assertEqual(2 >= 2, result)

        result, _ = await self.call('Main', [2, 1], return_type=bool)
        self.assertEqual(2 >= 1, result)

    def test_string_greater_or_equal_than_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.PUSH1
            + Opcode.NUMNOTEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('StrGreaterOrEqual.py')
        self.assertEqual(expected_output, output)

    async def test_string_greater_or_equal_than_operation_run(self):
        await self.set_up_contract('StrGreaterOrEqual.py')

        result, _ = await self.call('Main', ['test', 'unit'], return_type=bool)
        self.assertEqual('test' >= 'unit', result)

        result, _ = await self.call('Main', ['unit', 'unit'], return_type=bool)
        self.assertEqual('unit' >= 'unit', result)

        result, _ = await self.call('Main', ['unit', 'test'], return_type=bool)
        self.assertEqual('unit' >= 'test', result)

    # endregion

    # region Identity

    async def test_boolean_identity_operation(self):
        await self.set_up_contract('BoolIdentity.py')

        a = True
        b = True
        result, _ = await self.call('without_attribution_true', [], return_type=bool)
        self.assertEqual(a is b, result)

        a = True
        b = False
        result, _ = await self.call('without_attribution_false', [], return_type=bool)
        self.assertEqual(a is b, result)

        c = True
        d = c
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(c is d, result)

    async def test_list_identity(self):
        await self.set_up_contract('ListIdentity.py')

        a = [1, 2, 3]
        b = a
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(a is b, result)

        a = [1, 2, 3]
        b = [1, 2, 3]
        result, _ = await self.call('without_attribution', [], return_type=bool)
        self.assertEqual(a is b, result)

    async def test_mixed_identity(self):
        await self.set_up_contract('MixedIdentity.py')

        # a mixed identity should always result in False, but will compile
        result, _ = await self.call('mixed', [], return_type=bool)
        self.assertEqual(False, result)

    async def test_none_identity_operation(self):
        await self.set_up_contract('NoneIdentity.py')

        result, _ = await self.call('main', [1], return_type=bool)
        self.assertEqual(1 is None, result)

        result, _ = await self.call('main', [True], return_type=bool)
        self.assertEqual(True is None, result)

        result, _ = await self.call('main', ['string'], return_type=bool)
        self.assertEqual('string' is None, result)

        result, _ = await self.call('main', [b'bytes'], return_type=bool)
        self.assertEqual(b'bytes' is None, result)

        result, _ = await self.call('main', [None], return_type=bool)
        self.assertEqual(None is None, result)

    async def test_number_identity_operation(self):
        await self.set_up_contract('NumIdentity.py')

        a = 1
        b = 1
        result, _ = await self.call('without_attribution_true', [], return_type=bool)
        self.assertEqual(a is b, result)

        a = 1
        b = 2
        result, _ = await self.call('without_attribution_false', [], return_type=bool)
        self.assertEqual(a is b, result)

        c = 1
        d = c
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(c is d, result)

    async def test_string_identity_operation(self):
        await self.set_up_contract('StrIdentity.py')

        a = 'unit'
        b = 'unit'
        result, _ = await self.call('without_attribution_true', [], return_type=bool)
        self.assertEqual(a is b, result)

        a = 'unit'
        b = 'test'
        result, _ = await self.call('without_attribution_false', [], return_type=bool)
        self.assertEqual(a is b, result)

        c = 'unit'
        d = c
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(c is d, result)

    async def test_tuple_identity(self):
        await self.set_up_contract('TupleIdentity.py')

        a = (1, 2, 3)
        b = a
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(a is b, result)

        # Python will try conserve memory and will make a and b reference the same position, since Tuples are immutable
        # this will deviate from Neo's expected behavior
        result, _ = await self.call('without_attribution', [], return_type=bool)
        self.assertEqual(False, result)

    # endregion

    # region LessThan

    async def test_builtin_type_less_than_operation(self):
        await self.set_up_contract('BuiltinTypeLessThan.py')

        result, _ = await self.call('main', [FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY], return_type=bool)
        self.assertEqual(FindOptions.VALUES_ONLY < FindOptions.VALUES_ONLY, result)

    def test_mixed_less_than_operation(self):
        path = self.get_contract_path('MixedLessThan.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_number_less_than_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LT
            + Opcode.RET
        )

        output, _ = self.assertCompile('NumLessThan.py')
        self.assertEqual(expected_output, output)

    async def test_number_less_than_operation_run(self):
        await self.set_up_contract('NumLessThan.py')

        result, _ = await self.call('Main', [1, 2], return_type=bool)
        self.assertEqual(1 < 2, result)

        result, _ = await self.call('Main', [2, 2], return_type=bool)
        self.assertEqual(2 < 2, result)

        result, _ = await self.call('Main', [2, 1], return_type=bool)
        self.assertEqual(2 < 1, result)

    def test_string_less_than_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.PUSH1
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('StrLessThan.py')
        self.assertEqual(expected_output, output)

    async def test_string_less_than_operation_run(self):
        await self.set_up_contract('StrLessThan.py')

        result, _ = await self.call('Main', ['test', 'unit'], return_type=bool)
        self.assertEqual('test' < 'unit', result)

        result, _ = await self.call('Main', ['unit', 'unit'], return_type=bool)
        self.assertEqual('unit' < 'unit', result)

        result, _ = await self.call('Main', ['unit', 'test'], return_type=bool)
        self.assertEqual('unit' < 'test', result)

    # endregion

    # region LessThanOrEqual

    async def test_builtin_type_less_than_or_equal_operation(self):
        await self.set_up_contract('BuiltinTypeLessThanOrEqual.py')

        result, _ = await self.call('main', [FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY], return_type=bool)
        self.assertEqual(FindOptions.VALUES_ONLY <= FindOptions.VALUES_ONLY, result)

    def test_mixed_less_or_equal_than_operation(self):
        path = self.get_contract_path('MixedLessOrEqual.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_number_less_or_equal_than_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LE
            + Opcode.RET
        )

        output, _ = self.assertCompile('NumLessOrEqual.py')
        self.assertEqual(expected_output, output)

    async def test_number_less_or_equal_than_operation_run(self):
        await self.set_up_contract('NumLessOrEqual.py')

        result, _ = await self.call('Main', [1, 2], return_type=bool)
        self.assertEqual(1 <= 2, result)

        result, _ = await self.call('Main', [2, 2], return_type=bool)
        self.assertEqual(2 <= 2, result)

        result, _ = await self.call('Main', [2, 1], return_type=bool)
        self.assertEqual(2 <= 1, result)

    def test_string_less_or_equal_than_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CALLT + b'\x00\x00'
            + Opcode.PUSHM1
            + Opcode.NUMNOTEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('StrLessOrEqual.py')
        self.assertEqual(expected_output, output)

    async def test_string_less_or_equal_than_operation_run(self):
        await self.set_up_contract('StrLessOrEqual.py')

        result, _ = await self.call('Main', ['test', 'unit'], return_type=bool)
        self.assertEqual('test' <= 'unit', result)

        result, _ = await self.call('Main', ['unit', 'unit'], return_type=bool)
        self.assertEqual('unit' <= 'unit', result)

        result, _ = await self.call('Main', ['unit', 'test'], return_type=bool)
        self.assertEqual('unit' <= 'test', result)

    # endregion

    # region MixedEquality

    def test_mixed_equality_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.EQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('MixedEquality.py')
        self.assertEqual(expected_output, output)

    async def test_mixed_equality_operation_run(self):
        await self.set_up_contract('MixedEquality.py')

        result, _ = await self.call('Main', [1, 'unit'], return_type=bool)
        self.assertEqual(1 == 'unit', result)

        result, _ = await self.call('Main', [123, '123'], return_type=bool)
        self.assertEqual(123 == '123', result)

        result, _ = await self.call('Main', [Integer.from_bytes(b'123'), '123'], return_type=bool)
        self.assertEqual(Integer.from_bytes(b'123') == '123', result)

    async def test_boa2_equality_test2(self):
        await self.set_up_contract('Equality2Boa2Test.py')

        result, _ = await self.call('main', [1], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [2], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [3], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [4], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [5], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [6], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [7], return_type=bool)
        self.assertEqual(False, result)

    # endregion

    # region MixedInequality

    def test_mixed_inequality_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NOTEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('MixedInequality.py')
        self.assertEqual(expected_output, output)

    async def test_mixed_inequality_operation_run(self):
        await self.set_up_contract('MixedInequality.py')

        result, _ = await self.call('Main', [1, 'unit'], return_type=bool)
        self.assertEqual(1 != 'unit', result)

        result, _ = await self.call('Main', [123, '123'], return_type=bool)
        self.assertEqual(123 != '123', result)

        result, _ = await self.call('Main', [Integer.from_bytes(b'123'), '123'], return_type=bool)
        self.assertEqual(Integer.from_bytes(b'123') != '123', result)

    # endregion

    # region NotIdentity

    async def test_boolean_not_identity_operation(self):
        await self.set_up_contract('BoolNotIdentity.py')

        a = True
        b = False
        result, _ = await self.call('without_attribution_true', [], return_type=bool)
        self.assertEqual(a is not b, result)

        a = True
        b = True
        result, _ = await self.call('without_attribution_false', [], return_type=bool)
        self.assertEqual(a is not b, result)

        c = True
        d = c
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(c is not d, result)

    async def test_list_not_identity(self):
        await self.set_up_contract('ListNotIdentity.py')

        a = [1, 2, 3]
        b = a
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(a is not b, result)

        a = [1, 2, 3]
        b = [1, 2, 3]
        result, _ = await self.call('without_attribution', [], return_type=bool)
        self.assertEqual(a is not b, result)

    async def test_none_not_identity_operation(self):
        await self.set_up_contract('NoneNotIdentity.py')

        result, _ = await self.call('main', [1], return_type=bool)
        self.assertEqual(1 is not None, result)

        result, _ = await self.call('main', [True], return_type=bool)
        self.assertEqual(True is not None, result)

        result, _ = await self.call('main', ['string'], return_type=bool)
        self.assertEqual('string' is not None, result)

        result, _ = await self.call('main', [b'bytes'], return_type=bool)
        self.assertEqual(b'bytes' is not None, result)

        result, _ = await self.call('main', [None], return_type=bool)
        self.assertEqual(None is not None, result)

    async def test_number_not_identity_operation(self):
        await self.set_up_contract('NumNotIdentity.py')

        a = 1
        b = 2
        result, _ = await self.call('without_attribution_true', [], return_type=bool)
        self.assertEqual(a is not b, result)

        a = 1
        b = 1
        result, _ = await self.call('without_attribution_false', [], return_type=bool)
        self.assertEqual(a is not b, result)

        c = 1
        d = c
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(c is not d, result)

    async def test_string_not_identity_operation(self):
        await self.set_up_contract('StrNotIdentity.py')

        a = 'unit'
        b = 'test'
        result, _ = await self.call('without_attribution_true', [], return_type=bool)
        self.assertEqual(a is not b, result)

        a = 'unit'
        b = 'unit'
        result, _ = await self.call('without_attribution_false', [], return_type=bool)
        self.assertEqual(a is not b, result)

        c = 'unit'
        d = c
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(c is not d, result)

    async def test_tuple_not_identity(self):
        await self.set_up_contract('TupleNotIdentity.py')

        a = (1, 2, 3)
        b = a
        result, _ = await self.call('with_attribution', [], return_type=bool)
        self.assertEqual(a is not b, result)

        # Python will try conserve memory and will make a and b reference the same position, since Tuples are immutable
        # this will deviate from Neo's expected behavior
        result, _ = await self.call('without_attribution', [], return_type=bool)
        self.assertEqual(True, result)

    # endregion

    # region NumericEquality

    def test_boolean_equality_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('BoolEquality.py')
        self.assertEqual(expected_output, output)

    async def test_boolean_equality_operation_run(self):
        await self.set_up_contract('BoolEquality.py')

        result, _ = await self.call('Main', [True, False], return_type=bool)
        self.assertEqual(True == False, result)

        result, _ = await self.call('Main', [True, True], return_type=bool)
        self.assertEqual(True == True, result)

    async def test_builtin_equality_operation(self):
        await self.set_up_contract('BuiltinTypeEquality.py')

        result, _ = await self.call('main', [FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY], return_type=bool)
        self.assertEqual(FindOptions.VALUES_ONLY == FindOptions.VALUES_ONLY, result)

    def test_multiple_comparisons_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.LE
            + Opcode.LDARG0
            + Opcode.LDARG2
            + Opcode.LE
            + Opcode.BOOLAND
            + Opcode.RET
        )

        output, _ = self.assertCompile('NumRange.py')
        self.assertEqual(expected_output, output)

    async def test_multiple_comparisons_compile_run(self):
        await self.set_up_contract('NumRange.py')

        result, _ = await self.call('Main', [1, 2, 5], return_type=bool)
        self.assertEqual(2 <= 1 <= 5, result)

        result, _ = await self.call('Main', [2, 1, 5], return_type=bool)
        self.assertEqual(1 <= 2 <= 5, result)

        result, _ = await self.call('Main', [5, 1, 2], return_type=bool)
        self.assertEqual(1 <= 5 <= 2, result)

        result, _ = await self.call('Main', [2, 5, 1], return_type=bool)
        self.assertEqual(5 <= 2 <= 1, result)

    def test_number_equality_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('NumEquality.py')
        self.assertEqual(expected_output, output)

    async def test_number_equality_operation_run(self):
        await self.set_up_contract('NumEquality.py')

        result, _ = await self.call('Main', [1, 2], return_type=bool)
        self.assertEqual(1 == 2, result)

        result, _ = await self.call('Main', [2, 2], return_type=bool)
        self.assertEqual(2 == 2, result)

    # endregion

    # region NumericInequality

    def test_boolean_inequality_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMNOTEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('BoolInequality.py')
        self.assertEqual(expected_output, output)

    async def test_boolean_inequality_operation_run(self):
        await self.set_up_contract('BoolInequality.py')

        result, _ = await self.call('Main', [True, False], return_type=bool)
        self.assertEqual(True != False, result)

        result, _ = await self.call('Main', [True, True], return_type=bool)
        self.assertEqual(True != True, result)

    async def test_builtin_inequality_operation(self):
        await self.set_up_contract('BuiltinTypeInequality.py')

        result, _ = await self.call('main', [FindOptions.VALUES_ONLY, FindOptions.VALUES_ONLY], return_type=bool)
        self.assertEqual(FindOptions.VALUES_ONLY != FindOptions.VALUES_ONLY, result)

    def test_number_inequality_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMNOTEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('NumInequality.py')
        self.assertEqual(expected_output, output)

    async def test_number_inequality_operation_run(self):
        await self.set_up_contract('NumInequality.py')

        result, _ = await self.call('Main', [1, 2], return_type=bool)
        self.assertEqual(1 != 2, result)

        result, _ = await self.call('Main', [2, 2], return_type=bool)
        self.assertEqual(2 != 2, result)

    def test_number_inequality_operation_2(self):
        path = self.get_contract_path('NumInequalityPython2.py')

        with self.assertRaises(SyntaxError):
            self.compile(path)

    # endregion

    # region ObjectEquality

    async def test_compare_same_value_argument(self):
        await self.set_up_contract('CompareSameValueArgument.py')

        result, _ = await self.call('testing_something', [bytes(20)], return_type=bool)
        self.assertEqual(True, result)

    async def test_compare_same_value_hard_coded(self):
        await self.set_up_contract('CompareSameValueHardCoded.py')

        result, _ = await self.call('testing_something', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_compare_string(self):
        await self.set_up_contract('CompareString.py')

        result, _ = await self.call('test1', ['|'], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('test2', ['|'], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('test3', ['|'], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('test4', ['|'], return_type=bool)
        self.assertEqual(True, result)

    async def test_list_equality_with_slice(self):
        await self.set_up_contract('ListEqualityWithSlice.py')

        result, _ = await self.call('main', [['unittest', '123'], 'unittest'], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [['unittest', '123'], '123'], return_type=bool)
        self.assertEqual(False, result)

        with self.assertRaises(boatestcase.FaultException):
            await self.call('main', [[], ''], return_type=bool)

    def test_string_equality_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.EQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('StrEquality.py')
        self.assertEqual(expected_output, output)

    async def test_string_equality_operation_run(self):
        await self.set_up_contract('StrEquality.py')

        result, _ = await self.call('Main', ['unit', 'test'], return_type=bool)
        self.assertEqual('unit' == 'test', result)

        result, _ = await self.call('Main', ['unit', 'unit'], return_type=bool)
        self.assertEqual('unit' == 'unit', result)

    # endregion

    # region ObjectInequality

    def test_string_inequality_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NOTEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('StrInequality.py')
        self.assertEqual(expected_output, output)

    async def test_string_inequality_operation_run(self):
        await self.set_up_contract('StrInequality.py')

        result, _ = await self.call('Main', ['unit', 'test'], return_type=bool)
        self.assertEqual('unit' != 'test', result)

        result, _ = await self.call('Main', ['unit', 'unit'], return_type=bool)
        self.assertEqual('unit' != 'unit', result)

    # endregion
