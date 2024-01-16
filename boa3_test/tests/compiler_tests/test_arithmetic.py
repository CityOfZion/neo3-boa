from boa3.internal.exception import CompilerError
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.contracts import FindOptions
from boa3_test.tests import boatestcase


class TestArithmetic(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/arithmetic_test'

    # region Addition

    async def test_boa2_add_test(self):
        await self.set_up_contract('AddBoa2Test.py')

        result, _ = await self.call('main', [2], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', [23234], return_type=int)
        self.assertEqual(23236, result)

        result, _ = await self.call('main', [0], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [-112], return_type=int)
        self.assertEqual(-110, result)

    async def test_boa2_add_test1(self):
        await self.set_up_contract('AddBoa2Test1.py')

        result, _ = await self.call('main', [1, 2, 3, 4], return_type=int)
        self.assertEqual(9, result)

        result, _ = await self.call('main', [0, 0, 0, 2], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [-2, 3, -6, 2], return_type=int)
        self.assertEqual(-2, result)

    async def test_boa2_add_test2(self):
        await self.set_up_contract('AddBoa2Test2.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(3, result)

    async def test_boa2_add_test3(self):
        await self.set_up_contract('AddBoa2Test3.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(-9, result)

    async def test_boa2_add_test4(self):
        await self.set_up_contract('AddBoa2Test4.py')

        result, _ = await self.call('main', [1, 2, 3, 4], return_type=int)
        self.assertEqual(-9, result)

    async def test_boa2_add_test_void(self):
        await self.set_up_contract('AddBoa2TestVoid.py')

        result, _ = await self.call('main', [3], return_type=None)
        self.assertIsNone(result)

    def test_addition_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET
        )

        output, _ = self.assertCompile('Addition.py')
        self.assertEqual(expected_output, output)

    async def test_addition_operation_run(self):
        await self.set_up_contract('Addition.py')

        result, _ = await self.call('add', [1, 2], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('add', [-42, -24], return_type=int)
        self.assertEqual(-66, result)

        result, _ = await self.call('add', [-42, 24], return_type=int)
        self.assertEqual(-18, result)

    def test_addition_augmented_assignment_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STARG0
            + Opcode.RET
        )

        output, _ = self.assertCompile('AdditionAugmentedAssignment.py')
        self.assertEqual(expected_output, output)

    async def test_addition_builtin_type(self):
        await self.set_up_contract('AdditionBuiltinType.py')

        args = [FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES]
        expected = args[0] + args[1]
        result, _ = await self.call('main', args, return_type=int)
        self.assertEqual(expected, result)

    def test_addition_literal_operation_compile(self):
        expected_output = (
            Opcode.PUSH3
            + Opcode.RET
        )

        output, _ = self.assertCompile('AdditionLiteral.py')
        self.assertEqual(expected_output, output)

    async def test_addition_literal_operation_run(self):
        await self.set_up_contract('AdditionLiteral.py')

        result, _ = await self.call('add_one_two', [], return_type=int)
        self.assertEqual(3, result)

    def test_addition_literal_and_variable_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.PUSH1
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.RET
        )

        output, _ = self.assertCompile('AdditionLiteralAndVariable.py')
        self.assertEqual(expected_output, output)

    async def test_addition_literal_and_variable_run(self):
        await self.set_up_contract('AdditionLiteralAndVariable.py')

        result, _ = await self.call('add_one', [1], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('add_one', [-10], return_type=int)
        self.assertEqual(-9, result)

        result, _ = await self.call('add_one', [-1], return_type=int)
        self.assertEqual(0, result)

    def test_sequence_addition_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.PUSH4
            + Opcode.ADD
            + Opcode.RET
        )

        output, _ = self.assertCompile('AdditionThreeElements.py')
        self.assertEqual(expected_output, output)

    async def test_sequence_addition_run(self):
        await self.set_up_contract('AdditionThreeElements.py')

        result, _ = await self.call('add_four', [1, 2], return_type=int)
        self.assertEqual(7, result)

        result, _ = await self.call('add_four', [-42, -24], return_type=int)
        self.assertEqual(-62, result)

        result, _ = await self.call('add_four', [-42, 24], return_type=int)
        self.assertEqual(-14, result)

    def test_sequence_addition_different_orders_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.PUSH6
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.RET
        )

        output, _ = self.assertCompile('AdditionThreeValuesUnordered1.py')
        self.assertEqual(expected_output, output)

        output, _ = self.assertCompile('AdditionThreeValuesUnordered2.py')
        self.assertEqual(expected_output, output)

        output, _ = self.assertCompile('AdditionThreeValuesUnordered3.py')
        self.assertEqual(expected_output, output)

    async def test_sequence_addition_different_orders_run(self):
        await self.set_up_contract('AdditionThreeValuesUnordered1.py')
        contract_2 = await self.compile_and_deploy('AdditionThreeValuesUnordered2.py')
        contract_3 = await self.compile_and_deploy('AdditionThreeValuesUnordered3.py')

        result, _ = await self.call('add_six', [5], return_type=int)
        self.assertEqual(11, result)
        result, _ = await self.call('add_six', [5], return_type=int, target_contract=contract_2)
        self.assertEqual(11, result)
        result, _ = await self.call('add_six', [5], return_type=int, target_contract=contract_3)
        self.assertEqual(11, result)

        result, _ = await self.call('add_six', [-42], return_type=int)
        self.assertEqual(-36, result)
        result, _ = await self.call('add_six', [-42], return_type=int, target_contract=contract_2)
        self.assertEqual(-36, result)
        result, _ = await self.call('add_six', [-42], return_type=int, target_contract=contract_3)
        self.assertEqual(-36, result)

    def test_addition_variable_and_literal_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.RET
        )

        output, _ = self.assertCompile('AdditionVariableAndLiteral.py')
        self.assertEqual(expected_output, output)

    async def test_addition_variable_and_literal_run(self):
        await self.set_up_contract('AdditionVariableAndLiteral.py')

        result, _ = await self.call('add_one', [1], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('add_one', [-10], return_type=int)
        self.assertEqual(-9, result)

        result, _ = await self.call('add_one', [-1], return_type=int)
        self.assertEqual(0, result)

    # endregion

    # region Concatenation

    async def test_concat_bytes_variables_and_constants(self):
        await self.set_up_contract('ConcatBytesVariablesAndConstants.py')

        address_version = Integer(53).to_byte_array()

        expected = b'value1  value2  value3  ' + address_version + b'some_bytes_after'
        result, _ = await self.call('concat1', [], return_type=bytes)
        self.assertEqual(expected, result)

        expected = b'value1value2value3' + address_version + b'some_bytes_after'
        result, _ = await self.call('concat2', [], return_type=bytes)
        self.assertEqual(expected, result)

        expected = b'value1__value2__value3__' + address_version + b'some_bytes_after'
        result, _ = await self.call('concat3', [], return_type=bytes)
        self.assertEqual(expected, result)

    def test_concatenation_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CAT
            + Opcode.CONVERT
            + Type.str.stack_item
            + Opcode.RET
        )

        output, _ = self.assertCompile('Concatenation.py')
        self.assertEqual(expected_output, output)

    async def test_concatenation_operation_run(self):
        await self.set_up_contract('Concatenation.py')

        result, _ = await self.call('concat', ['a', 'b'], return_type=str)
        self.assertEqual('ab', result)

        result, _ = await self.call('concat', ['unit', 'test'], return_type=str)
        self.assertEqual('unittest', result)

    def test_concatenation_augmented_assignment_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CAT
            + Opcode.CONVERT
            + Type.str.stack_item
            + Opcode.STARG0
            + Opcode.RET
        )

        output, _ = self.assertCompile('ConcatenationAugmentedAssignment.py')
        self.assertEqual(expected_output, output)

    async def test_concat_string_variables_and_constants(self):
        await self.set_up_contract('ConcatStringVariablesAndConstants.py')

        result, _ = await self.call('concat', [], return_type=str)
        self.assertEqual('[1,2]', result)

    # endregion

    # region Division

    def test_division_operation(self):
        path = self.get_contract_path('Division.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_division_augmented_assignment(self):
        path = self.get_contract_path('DivisionAugmentedAssignment.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    async def test_division_builtin_type(self):
        await self.set_up_contract('DivisionBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY], return_type=int)
        self.assertEqual(FindOptions.DESERIALIZE_VALUES // FindOptions.VALUES_ONLY, result)

    def test_integer_division_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.DIV
            + Opcode.RET
        )

        output, _ = self.assertCompile('IntegerDivision.py')
        self.assertEqual(expected_output, output)

    async def test_integer_division_operation_run(self):
        await self.set_up_contract('IntegerDivision.py')

        result, _ = await self.call('floor_div', [10, 3], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('floor_div', [-42, -9], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('floor_div', [-100, 3], return_type=int)
        self.assertEqual(-33, result)

    def test_integer_division_augmented_assignment_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.DIV
            + Opcode.STARG0
            + Opcode.RET
        )

        output, _ = self.assertCompile('IntegerDivisionAugmentedAssignment.py')
        self.assertEqual(expected_output, output)

    # endregion

    # region ListAddition

    async def test_list_addition(self):
        await self.set_up_contract('ListAddition.py')

        arg0 = [1, 'str', '123']
        arg1 = [2, True, False]
        result, _ = await self.call('add_any', [arg0, arg1], return_type=list)
        self.assertEqual(arg0 + arg1, result)

        arg0 = [1, 3]
        arg1 = [2, 5]
        result, _ = await self.call('add_any', [arg0, arg1], return_type=list)
        self.assertEqual(arg0 + arg1, result)

        arg0 = [True]
        arg1 = [False, True]
        result, _ = await self.call('add_any', [arg0, arg1], return_type=list)
        self.assertEqual(arg0 + arg1, result)

        arg0 = ['unit', ' ']
        arg1 = ['test', '.']
        result, _ = await self.call('add_any', [arg0, arg1], return_type=list)
        self.assertEqual(arg0 + arg1, result)

    # endregion

    # region Mismatched

    def test_mismatched_type_binary_operation(self):
        path = self.get_contract_path('MismatchedOperandBinary.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_mismatched_type_unary_operation(self):
        path = self.get_contract_path('MismatchedOperandUnary.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region Mixed

    def test_mixed_operations_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x05'
            + Opcode.LDARG0
            + Opcode.LDARG2
            + Opcode.LDARG4
            + Opcode.MUL  # multiplicative operations
            + Opcode.ADD  # additive operations
            + Opcode.LDARG3
            + Opcode.NEGATE  # parentheses
            + Opcode.LDARG1
            + Opcode.DIV  # multiplicative
            + Opcode.SUB  # additive
            + Opcode.RET
        )

        output, _ = self.assertCompile('MixedOperations.py')
        self.assertEqual(expected_output, output)

    async def test_mixed_operations_run(self):
        await self.set_up_contract('MixedOperations.py')

        result, _ = await self.call('mixed', [10, 20, 30, 40, 50], return_type=int)
        self.assertEqual(10 + 30 * 50 + 40 // 20, result)

    def test_mixed_operations_with_parentheses_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x05'
            + Opcode.LDARG0
            + Opcode.LDARG2
            + Opcode.LDARG4
            + Opcode.LDARG3
            + Opcode.NEGATE  # inside parentheses
            + Opcode.SUB  # parentheses
            + Opcode.MUL  # multiplicative operations
            + Opcode.LDARG1
            + Opcode.DIV  # multiplicative
            + Opcode.ADD  # additive operations
            + Opcode.RET
        )

        output, _ = self.assertCompile('WithParentheses.py')
        self.assertEqual(expected_output, output)

    async def test_mixed_operations_with_parentheses_run(self):
        await self.set_up_contract('WithParentheses.py')

        result, _ = await self.call('mixed', [10, 20, 30, 40, 50], return_type=int)
        self.assertEqual(10 + 30 * (50 + 40) // 20, result)

    # endregion

    # region Modulo

    async def test_modulo_operation(self):
        await self.set_up_contract('Modulo.py')

        op1 = 10
        op2 = 3
        expected_output = op1 % op2
        result, _ = await self.call('mod', [op1, op2], return_type=int)
        self.assertEqual(expected_output, result)

        op1 = -42
        op2 = -9
        expected_output = op1 % op2
        result, _ = await self.call('mod', [op1, op2], return_type=int)
        self.assertEqual(expected_output, result)

        op1 = -100
        op2 = 3
        expected_output = op1 % op2
        result, _ = await self.call('mod', [op1, op2], return_type=int)
        self.assertEqual(expected_output, result)

        op1 = 100
        op2 = -3
        expected_output = op1 % op2
        result, _ = await self.call('mod', [op1, op2], return_type=int)
        self.assertEqual(expected_output, result)

    async def test_modulo_augmented_assignment(self):
        await self.set_up_contract('ModuloAugmentedAssignment.py')

        op1 = 10
        op2 = 3
        expected_output = op1 % op2
        result, _ = await self.call('mod', [op1, op2], return_type=int)
        self.assertEqual(expected_output, result)

        op1 = -42
        op2 = -9
        expected_output = op1 % op2
        result, _ = await self.call('mod', [op1, op2], return_type=int)
        self.assertEqual(expected_output, result)

        op1 = -100
        op2 = 3
        expected_output = op1 % op2
        result, _ = await self.call('mod', [op1, op2], return_type=int)
        self.assertEqual(expected_output, result)

        op1 = 100
        op2 = -3
        expected_output = op1 % op2
        result, _ = await self.call('mod', [op1, op2], return_type=int)
        self.assertEqual(expected_output, result)

    async def test_modulo_builtin_type(self):
        await self.set_up_contract('ModuloBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY], return_type=int)
        self.assertEqual(FindOptions.DESERIALIZE_VALUES % FindOptions.VALUES_ONLY, result)

    # endregion

    # region Multiplication

    def test_multiplication_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MUL
            + Opcode.RET
        )

        output, _ = self.assertCompile('Multiplication.py')
        self.assertEqual(expected_output, output)

    async def test_multiplication_operation_run(self):
        await self.set_up_contract('Multiplication.py')

        result, _ = await self.call('mult', [10, 3], return_type=int)
        self.assertEqual(30, result)

        result, _ = await self.call('mult', [-42, -2], return_type=int)
        self.assertEqual(84, result)

        result, _ = await self.call('mult', [-4, 20], return_type=int)
        self.assertEqual(-80, result)

        result, _ = await self.call('mult', [0, 20], return_type=int)
        self.assertEqual(0, result)

    def test_multiplication_augmented_assignment_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MUL
            + Opcode.STARG0
            + Opcode.RET
        )

        output, _ = self.assertCompile('MultiplicationAugmentedAssignment.py')
        self.assertEqual(expected_output, output)

    async def test_multiplication_builtin_type(self):
        await self.set_up_contract('MultiplicationBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY], return_type=int)
        self.assertEqual(FindOptions.DESERIALIZE_VALUES * FindOptions.VALUES_ONLY, result)

    # endregion

    # region Power

    def test_power_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.POW
            + Opcode.RET
        )

        output, _ = self.assertCompile('Power.py')
        self.assertEqual(expected_output, output)

    async def test_power_operation_run(self):
        await self.set_up_contract('Power.py')

        result, _ = await self.call('pow', [10, 3], return_type=int)
        self.assertEqual(1000, result)

        result, _ = await self.call('pow', [1, 15], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('pow', [-2, 2], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('pow', [0, 20], return_type=int)
        self.assertEqual(0, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('pow', [1, -2], return_type=int)

        self.assertRegex(str(context.exception), 'invalid exponent')

    def test_power_augmented_assignment_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.POW
            + Opcode.STARG0
            + Opcode.RET
        )

        output, _ = self.assertCompile('PowerAugmentedAssignment.py')
        self.assertEqual(expected_output, output)

    async def test_power_builtin_type(self):
        await self.set_up_contract('PowerBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY], return_type=int)
        self.assertEqual(FindOptions.DESERIALIZE_VALUES ** FindOptions.VALUES_ONLY, result)

    # endregion

    # region Sign

    def test_negative_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.NEGATE
            + Opcode.RET
        )

        output, _ = self.assertCompile('Negative.py')
        self.assertEqual(expected_output, output)

    async def test_negative_operation_run(self):
        await self.set_up_contract('Negative.py')

        result, _ = await self.call('minus', [10], return_type=int)
        self.assertEqual(-10, result)

        result, _ = await self.call('minus', [-1], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('minus', [0], return_type=int)
        self.assertEqual(0, result)

    async def test_negative_builtin_type(self):
        await self.set_up_contract('NegativeBuiltinType.py')

        result, _ = await self.call('minus', [FindOptions.DESERIALIZE_VALUES], return_type=int)
        self.assertEqual(-FindOptions.DESERIALIZE_VALUES, result)

    def test_positive_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.RET
        )

        output, _ = self.assertCompile('Positive.py')
        self.assertEqual(expected_output, output)

    async def test_positive_operation_run(self):
        await self.set_up_contract('Positive.py')

        result, _ = await self.call('plus', [10], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('plus', [-1], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('plus', [0], return_type=int)
        self.assertEqual(0, result)

    async def test_positive_builtin_type(self):
        await self.set_up_contract('PositiveBuiltinType.py')

        result, _ = await self.call('plus', [FindOptions.DESERIALIZE_VALUES], return_type=int)
        self.assertEqual(+FindOptions.DESERIALIZE_VALUES, result)

    # endregion

    # region StrBytesMultiplication

    byte_str_mult = (
        Opcode.PUSHDATA1 + Integer(0).to_byte_array(min_length=1)
        + Opcode.ROT
        + Opcode.ROT
        + Opcode.JMP + Integer(7).to_byte_array()
        + Opcode.REVERSE3
        + Opcode.OVER
        + Opcode.CAT
        + Opcode.REVERSE3
        + Opcode.DEC
        + Opcode.DUP
        + Opcode.PUSH0
        + Opcode.GT
        + Opcode.JMPIF + Integer(-8).to_byte_array()
        + Opcode.DROP
        + Opcode.DROP
    )

    def test_bytes_multiplication_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + self.byte_str_mult
            + Opcode.CONVERT + Type.bytes.stack_item
            + Opcode.RET
        )

        output, _ = self.assertCompile('BytesMultiplication.py')
        self.assertEqual(expected_output, output)

    async def test_bytes_multiplication_operation_run(self):
        await self.set_up_contract('BytesMultiplication.py')

        result, _ = await self.call('bytes_mult',
                                    [b'a', 4],
                                    return_type=bytes)
        self.assertEqual(b'aaaa', result)

        result, _ = await self.call('bytes_mult',
                                    [b'unit', 50],
                                    return_type=bytes)
        self.assertEqual(b'unit' * 50, result)

    def test_bytes_multiplication_operation_augmented_assignment_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + self.byte_str_mult
            + Opcode.CONVERT + Type.bytes.stack_item
            + Opcode.STARG0
            + Opcode.LDARG0
            + Opcode.RET
        )

        output, _ = self.assertCompile('BytesMultiplicationAugmentedAssignment.py')
        self.assertEqual(expected_output, output)

    async def test_bytes_multiplication_operation_augmented_assignment_run(self):
        await self.set_up_contract('BytesMultiplicationAugmentedAssignment.py')

        result, _ = await self.call('Main', [b'unit', 50],
                                    return_type=bytes)
        self.assertEqual(b'unit' * 50, result)

    async def test_bytes_multiplication_builtin_type(self):
        await self.set_up_contract('BytesMultiplicationBuiltinType.py')

        result, _ = await self.call('bytes_mult', [b'unit test', FindOptions.VALUES_ONLY],
                                    return_type=bytes)
        self.assertEqual(b'unit test' * FindOptions.VALUES_ONLY, result)

    def test_str_multiplication_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + self.byte_str_mult
            + Opcode.CONVERT + Type.str.stack_item
            + Opcode.RET
        )

        output, _ = self.assertCompile('StringMultiplication.py')
        self.assertEqual(expected_output, output)

    async def test_str_multiplication_operation_run(self):
        await self.set_up_contract('StringMultiplication.py')

        result, _ = await self.call('str_mult', ['a', 4], return_type=str)
        self.assertEqual('aaaa', result)

        result, _ = await self.call('str_mult', ['unit', 50], return_type=str)
        self.assertEqual('unit' * 50, result)

    def test_str_multiplication_operation_augmented_assignment_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + self.byte_str_mult
            + Opcode.CONVERT + Type.str.stack_item
            + Opcode.STARG0
            + Opcode.LDARG0
            + Opcode.RET
        )

        output, _ = self.assertCompile('StringMultiplicationAugmentedAssignment.py')
        self.assertEqual(expected_output, output)

    async def test_str_multiplication_operation_augmented_assignment_run(self):
        await self.set_up_contract('StringMultiplicationAugmentedAssignment.py')

        result, _ = await self.call('Main', ['unit', 50], return_type=str)
        self.assertEqual('unit' * 50, result)

    async def test_str_multiplication_builtin_type(self):
        await self.set_up_contract('StringMultiplicationBuiltinType.py')

        result, _ = await self.call('str_mult', ['unit test', FindOptions.VALUES_ONLY], return_type=str)
        self.assertEqual('unit test' * FindOptions.VALUES_ONLY, result)

    # endregion

    # region Subtraction

    def test_subtraction_operation_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SUB
            + Opcode.RET
        )

        output, _ = self.assertCompile('Subtraction.py')
        self.assertEqual(expected_output, output)

    async def test_subtraction_operation_run(self):
        await self.set_up_contract('Subtraction.py')

        result, _ = await self.call('sub', [10, 3], return_type=int)
        self.assertEqual(7, result)

        result, _ = await self.call('sub', [-42, -24], return_type=int)
        self.assertEqual(-18, result)

        result, _ = await self.call('sub', [-42, 24], return_type=int)
        self.assertEqual(-66, result)

    def test_subtraction_augmented_assignment_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SUB
            + Opcode.STARG0
            + Opcode.RET
        )

        output, _ = self.assertCompile('SubtractionAugmentedAssignment.py')
        self.assertEqual(expected_output, output)

    async def test_subtraction_builtin_type(self):
        await self.set_up_contract('SubtractionBuiltinType.py')

        result, _ = await self.call('main', [FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY], return_type=int)
        self.assertEqual(FindOptions.DESERIALIZE_VALUES - FindOptions.VALUES_ONLY, result)

    # endregion
