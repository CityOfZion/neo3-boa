from boa3_test.tests import boatestcase

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo3.contracts import FindOptions


class TestLogical(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/logical_test'

    # region BoolAnd

    async def test_boolean_and_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.BOOLAND
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicBoolAnd.py')
        self.assertEqual(expected_output, output)

    async def test_boolean_and(self):
        await self.set_up_contract('LogicBoolAnd.py')

        result, _ = await self.call('Main', [True, True], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [True, False], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [False, True], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [False, False], return_type=bool)
        self.assertEqual(False, result)

    def test_mismatched_type_binary_operation(self):
        path = self.get_contract_path('LogicMismatchedOperandAnd.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region BoolNot

    async def test_boolean_not_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.NOT
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicBoolNot.py')
        self.assertEqual(expected_output, output)

    async def test_boolean_not(self):
        await self.set_up_contract('LogicBoolNot.py')

        result, _ = await self.call('Main', [True], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [False], return_type=bool)
        self.assertEqual(True, result)

    async def test_mismatched_type_unary_operation(self):
        path = self.get_contract_path('LogicMismatchedOperandNot.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region BoolOr

    async def test_boolean_or_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.BOOLOR
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicBoolOr.py')
        self.assertEqual(expected_output, output)

    async def test_boolean_or(self):
        await self.set_up_contract('LogicBoolOr.py')

        result, _ = await self.call('Main', [True, True], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [True, False], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [False, True], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [False, False], return_type=bool)
        self.assertEqual(False, result)

    async def test_sequence_boolean_or_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.BOOLOR
            + Opcode.LDARG2
            + Opcode.BOOLOR
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicBoolOrThreeElements.py')
        self.assertEqual(expected_output, output)

    async def test_sequence_boolean_or(self):
        await self.set_up_contract('LogicBoolOrThreeElements.py')

        result, _ = await self.call('Main', [True, False, False], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [False, True, False], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [False, False, False], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [True, True, True], return_type=bool)
        self.assertEqual(True, result)

    # endregion

    # region LeftShift

    async def test_left_shift_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SHL
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicLeftShift.py')
        self.assertEqual(expected_output, output)

    async def test_logic_left_shift(self):
        await self.set_up_contract('LogicLeftShift.py')

        result, _ = await self.call('Main', [int('100', 2), 2], return_type=int)
        self.assertEqual(int('10000', 2), result)

        result, _ = await self.call('Main', [int('11', 2), 1], return_type=int)
        self.assertEqual(int('110', 2), result)

        result, _ = await self.call('Main', [int('101010', 2), 4], return_type=int)
        self.assertEqual(int('1010100000', 2), result)

    async def test_logic_left_shift_builtin_type(self):
        await self.set_up_contract('LogicLeftShiftBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.NONE, FindOptions.DESERIALIZE_VALUES], return_type=int)
        self.assertEqual(FindOptions.NONE << FindOptions.DESERIALIZE_VALUES, result)

    async def test_mismatched_type_logic_left_shift(self):
        path = self.get_contract_path('LogicMismatchedOperandLogicLeftShift.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region LogicAnd

    async def test_logic_and_with_bool_operand_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.AND
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicAndBool.py')
        self.assertEqual(expected_output, output)

    async def test_logic_and_with_bool_operand(self):
        await self.set_up_contract('LogicAndBool.py')

        result, _ = await self.call('Main', [True, True], return_type=int)
        self.assertEqual(True, bool(result))

        result, _ = await self.call('Main', [True, False], return_type=int)
        self.assertEqual(False, bool(result))

        result, _ = await self.call('Main', [False, False], return_type=int)
        self.assertEqual(False, bool(result))


    async def test_logic_and_with_int_operand_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.AND
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicAndInt.py')
        self.assertEqual(expected_output, output)

    async def test_logic_and_with_int_operand(self):
        await self.set_up_contract('LogicAndInt.py')

        result, _ = await self.call('Main', [4, 6], return_type=int)
        self.assertEqual(4 & 6, result)

        result, _ = await self.call('Main', [40, 6], return_type=int)
        self.assertEqual(40 & 6, result)

        result, _ = await self.call('Main', [-4, 32], return_type=int)
        self.assertEqual(-4 & 32, result)

    async def test_logic_and_builtin_type(self):
        await self.set_up_contract('LogicAndBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.NONE, FindOptions.DESERIALIZE_VALUES], return_type=int)
        self.assertEqual(FindOptions.NONE & FindOptions.DESERIALIZE_VALUES, result)

    async def test_mismatched_type_logic_and(self):
        path = self.get_contract_path('LogicMismatchedOperandLogicAnd.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region LogicNot

    async def test_logic_not_with_bool_operand_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.INVERT
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicNotBool.py')
        self.assertEqual(expected_output, output)

    async def test_logic_not_with_bool_operand(self):
        await self.set_up_contract('LogicNotBool.py')

        result, _ = await self.call('Main', [True], return_type=int)
        self.assertEqual(-2, result)

        result, _ = await self.call('Main', [False], return_type=int)
        self.assertEqual(-1, result)

    async def test_logic_not_builtin_type(self):
        await self.set_up_contract('LogicNotBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.VALUES_ONLY], return_type=int)
        self.assertEqual(~FindOptions.VALUES_ONLY, result)

    async def test_logic_not_with_int_operand_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.INVERT
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicNotInt.py')
        self.assertEqual(expected_output, output)

    async def test_logic_not_with_int_operand(self):
        await self.set_up_contract('LogicNotInt.py')

        result, _ = await self.call('Main', [4], return_type=int)
        self.assertEqual(-5, result)

        result, _ = await self.call('Main', [40], return_type=int)
        self.assertEqual(-41, result)

        result, _ = await self.call('Main', [-4], return_type=int)
        self.assertEqual(3, result)

    async def test_mismatched_type_logic_not(self):
        path = self.get_contract_path('LogicMismatchedOperandLogicNot.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region LogicOr

    async def test_logic_or_with_bool_operand_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.OR
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicOrBool.py')
        self.assertEqual(expected_output, output)

    async def test_logic_or_with_bool_operand(self):
        await self.set_up_contract('LogicOrBool.py')

        result, _ = await self.call('Main', [True, True], return_type=int)
        self.assertEqual(True, bool(result))

        result, _ = await self.call('Main', [True, False], return_type=int)
        self.assertEqual(True, bool(result))

        result, _ = await self.call('Main', [False, False], return_type=int)
        self.assertEqual(False, bool(result))


    async def test_logic_or_with_int_operand_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.OR
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicOrInt.py')
        self.assertEqual(expected_output, output)

    async def test_logic_or_with_int_operand(self):
        await self.set_up_contract('LogicOrInt.py')

        result, _ = await self.call('Main', [4, 6], return_type=int)
        self.assertEqual(4 | 6, result)

        result, _ = await self.call('Main', [40, 6], return_type=int)
        self.assertEqual(40 | 6, result)

        result, _ = await self.call('Main', [-4, 32], return_type=int)
        self.assertEqual(-4 | 32, result)

    async def test_logic_or_builtin_type(self):
        await self.set_up_contract('LogicOrBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.REMOVE_PREFIX, FindOptions.KEYS_ONLY], return_type=int)
        self.assertEqual(int(FindOptions.REMOVE_PREFIX | FindOptions.KEYS_ONLY), result)

        result, _ = await self.call('main', [FindOptions.REMOVE_PREFIX, FindOptions.KEYS_ONLY], return_type=int)
        self.assertEqual(FindOptions.REMOVE_PREFIX | FindOptions.KEYS_ONLY, result)

        result, _ = await self.call('main', [2, 4], return_type=int)
        self.assertEqual(int(2 | 4), result)

        result, _ = await self.call('main', [0, 123456789], return_type=int)
        self.assertEqual(123456789, result)

        result, _ = await self.call('main', [123456789, 0], return_type=int)
        self.assertEqual(123456789, result)

    async def test_mismatched_type_logic_or(self):
        path = self.get_contract_path('LogicMismatchedOperandLogicOr.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region LogicXor

    async def test_logic_xor_with_bool_operand_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.XOR
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicXorBool.py')
        self.assertEqual(expected_output, output)

    async def test_logic_xor_with_bool_operand(self):
        await self.set_up_contract('LogicXorBool.py')

        result, _ = await self.call('Main', [True, True], return_type=int)
        self.assertEqual(False, bool(result))

        result, _ = await self.call('Main', [True, False], return_type=int)
        self.assertEqual(True, bool(result))

        result, _ = await self.call('Main', [False, False], return_type=int)
        self.assertEqual(False, bool(result))

    async def test_logic_xor_with_int_operand_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.XOR
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicXorInt.py')
        self.assertEqual(expected_output, output)

    async def test_logic_xor_with_int_operand(self):
        await self.set_up_contract('LogicXorInt.py')

        result, _ = await self.call('Main', [4, 6], return_type=int)
        self.assertEqual(4 ^ 6, result)

        result, _ = await self.call('Main', [40, 6], return_type=int)
        self.assertEqual(40 ^ 6, result)

        result, _ = await self.call('Main', [-4, 32], return_type=int)
        self.assertEqual(-4 ^ 32, result)

    async def test_logic_xor_builtin_type(self):
        await self.set_up_contract('LogicXorBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.NONE, FindOptions.DESERIALIZE_VALUES], return_type=int)
        self.assertEqual(FindOptions.NONE ^ FindOptions.DESERIALIZE_VALUES, result)

    async def test_mismatched_type_logic_xor(self):
        path = self.get_contract_path('LogicMismatchedOperandLogicXor.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region Mixed

    async def test_logic_augmented_assignment(self):
        await self.set_up_contract('LogicAugmentedAssignmentOperators.py')

        a = 1
        b = 4
        result, _ = await self.call('right_shift', [a, b], return_type=int)
        self.assertEqual(a >> b, result)

        a = 4
        b = 1
        result, _ = await self.call('left_shift', [a, b], return_type=int)
        self.assertEqual(a << b, result)

        a = 255
        b = 123
        result, _ = await self.call('l_and', [a, b], return_type=int)
        self.assertEqual(a & b, result)

        a = 255
        b = 123
        result, _ = await self.call('l_or', [a, b], return_type=int)
        self.assertEqual(a | b, result)

        a = 255
        b = 123
        result, _ = await self.call('xor', [a, b], return_type=int)
        self.assertEqual(a ^ b, result)

    async def test_boa2_logic_test(self):
        await self.set_up_contract('LogicBinOpBoa2Test.py')

        result, _ = await self.call('main', ['&', 4, 4], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', ['|', 4, 3], return_type=int)
        self.assertEqual(7, result)

        result, _ = await self.call('main', ['|', 4, 8], return_type=int)
        self.assertEqual(12, result)

        result, _ = await self.call('main', ['^', 4, 4], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', ['^', 4, 2], return_type=int)
        self.assertEqual(6, result)

        result, _ = await self.call('main', ['>>', 16, 2], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', ['>>', 16, 0], return_type=int)
        self.assertEqual(16, result)

        result, _ = await self.call('main', ['%', 16, 2], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', ['%', 16, 11], return_type=int)
        self.assertEqual(5, result)

        result, _ = await self.call('main', ['//', 16, 2], return_type=int)
        self.assertEqual(8, result)

        result, _ = await self.call('main', ['//', 16, 7], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', ['~', 16, 0], return_type=int)
        self.assertEqual(-17, result)

        result, _ = await self.call('main', ['~', -3, 0], return_type=int)
        self.assertEqual(2, result)

    async def test_mixed_operations_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG0
            + Opcode.NOT
            + Opcode.LDARG1
            + Opcode.LDARG2
            + Opcode.BOOLOR
            + Opcode.BOOLAND
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicMixedOperations.py')
        self.assertEqual(expected_output, output)

    async def test_mixed_operations(self):
        await self.set_up_contract('LogicMixedOperations.py')

        result, _ = await self.call('Main', [True, False, False], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [False, True, False], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [False, False, False], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [True, True, True], return_type=bool)
        self.assertEqual(False, result)

    async def test_logic_operation_with_return_and_stack_filled(self):
        await self.set_up_contract('LogicOperationWithReturnAndStackFilled.py')

        result, _ = await self.call('main', return_type=bool)
        self.assertEqual(True, result)

    # endregion

    # region RightShift

    async def test_logic_right_shift_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SHR
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogicRightShift.py')
        self.assertEqual(expected_output, output)
    async def test_logic_right_shift(self):
        await self.set_up_contract('LogicRightShift.py')

        result, _ = await self.call('Main', [int('10000', 2), 2], return_type=int)
        self.assertEqual(int('100', 2), result)

        result, _ = await self.call('Main', [int('110', 2), 1], return_type=int)
        self.assertEqual(int('11', 2), result)

        result, _ = await self.call('Main', [int('1010100000', 2), 4], return_type=int)
        self.assertEqual(int('101010', 2), result)

    async def test_logic_right_shift_builtin_type(self):
        await self.set_up_contract('LogicRightShiftBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.NONE, FindOptions.DESERIALIZE_VALUES], return_type=int)
        self.assertEqual(FindOptions.NONE >> FindOptions.DESERIALIZE_VALUES, result)

    async def test_mismatched_type_logic_right_shift(self):
        path = self.get_contract_path('LogicMismatchedOperandLogicRightShift.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion
