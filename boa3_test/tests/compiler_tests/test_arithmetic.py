from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.contracts import FindOptions
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestArithmetic(BoaTest):
    default_folder: str = 'test_sc/arithmetic_test'

    # region Addition

    def test_boa2_add_test(self):
        path, _ = self.get_deploy_file_paths('AddBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 2))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', 23234))
        expected_results.append(23236)

        invokes.append(runner.call_contract(path, 'main', 0))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', -112))
        expected_results.append(-110)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_add_test1(self):
        path, _ = self.get_deploy_file_paths('AddBoa2Test1.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, 2, 3, 4))
        expected_results.append(9)

        invokes.append(runner.call_contract(path, 'main', 0, 0, 0, 2))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', -2, 3, -6, 2))
        expected_results.append(-2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_add_test2(self):
        path, _ = self.get_deploy_file_paths('AddBoa2Test2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_add_test3(self):
        path, _ = self.get_deploy_file_paths('AddBoa2Test3.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(-9)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_add_test4(self):
        path, _ = self.get_deploy_file_paths('AddBoa2Test4.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, 2, 3, 4))
        expected_results.append(-9)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_add_test_void(self):
        path, _ = self.get_deploy_file_paths('AddBoa2TestVoid.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 3))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_addition_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET
        )

        path = self.get_contract_path('Addition.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'add', 1, 2))
        expected_results.append(3)
        invokes.append(runner.call_contract(path, 'add', -42, -24))
        expected_results.append(-66)
        invokes.append(runner.call_contract(path, 'add', -42, 24))
        expected_results.append(-18)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_addition_augmented_assignment(self):
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

        path = self.get_contract_path('AdditionAugmentedAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_addition_builtin_type(self):
        path, _ = self.get_deploy_file_paths('AdditionBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.VALUES_ONLY, FindOptions.DESERIALIZE_VALUES))
        expected_results.append(FindOptions.VALUES_ONLY + FindOptions.DESERIALIZE_VALUES)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_addition_literal_operation(self):
        expected_output = (
            Opcode.PUSH3
            + Opcode.RET
        )

        path = self.get_contract_path('AdditionLiteral.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'add_one_two'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_addition_literal_and_variable(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.PUSH1
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.RET
        )

        path = self.get_contract_path('AdditionLiteralAndVariable.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'add_one', 1))
        expected_results.append(2)
        invokes.append(runner.call_contract(path, 'add_one', -10))
        expected_results.append(-9)
        invokes.append(runner.call_contract(path, 'add_one', -1))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_sequence_addition(self):
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

        path = self.get_contract_path('AdditionThreeElements.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'add_four', 1, 2))
        expected_results.append(7)
        invokes.append(runner.call_contract(path, 'add_four', -42, -24))
        expected_results.append(-62)
        invokes.append(runner.call_contract(path, 'add_four', -42, 24))
        expected_results.append(-14)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_sequence_addition_different_orders(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.PUSH6
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.RET
        )
        path_1 = self.get_contract_path('AdditionThreeValuesUnordered1.py')
        output_1 = self.compile(path_1)
        self.assertEqual(expected_output, output_1)

        path_2 = self.get_contract_path('AdditionThreeValuesUnordered2.py')
        output_2 = self.compile(path_2)
        self.assertEqual(expected_output, output_2)

        path_3 = self.get_contract_path('AdditionThreeValuesUnordered3.py')
        output_3 = self.compile(path_3)
        self.assertEqual(expected_output, output_3)

        path_1, _ = self.get_deploy_file_paths(path_1)
        path_2, _ = self.get_deploy_file_paths(path_2)
        path_3, _ = self.get_deploy_file_paths(path_3)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path_1, 'add_six', 5))
        expected_results.append(11)
        invokes.append(runner.call_contract(path_2, 'add_six', 5))
        expected_results.append(11)
        invokes.append(runner.call_contract(path_3, 'add_six', 5))
        expected_results.append(11)

        invokes.append(runner.call_contract(path_1, 'add_six', -42))
        expected_results.append(-36)
        invokes.append(runner.call_contract(path_2, 'add_six', -42))
        expected_results.append(-36)
        invokes.append(runner.call_contract(path_3, 'add_six', -42))
        expected_results.append(-36)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_addition_variable_and_literal(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.RET
        )

        path = self.get_contract_path('AdditionVariableAndLiteral.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'add_one', 1))
        expected_results.append(2)
        invokes.append(runner.call_contract(path, 'add_one', -10))
        expected_results.append(-9)
        invokes.append(runner.call_contract(path, 'add_one', -1))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region Concatenation

    def test_concat_bytes_variables_and_constants(self):
        path, _ = self.get_deploy_file_paths('ConcatBytesVariablesAndConstants.py')
        address_version = Integer(neoxp.utils.get_address_version()).to_byte_array()
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'concat1',
                                            expected_result_type=bytes))
        expected_results.append(b'value1  value2  value3  ' + address_version + b'some_bytes_after')

        invokes.append(runner.call_contract(path, 'concat2',
                                            expected_result_type=bytes))
        expected_results.append(b'value1value2value3' + address_version + b'some_bytes_after')

        invokes.append(runner.call_contract(path, 'concat3',
                                            expected_result_type=bytes))
        expected_results.append(b'value1__value2__value3__' + address_version + b'some_bytes_after')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_concatenation_operation(self):
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

        path = self.get_contract_path('Concatenation.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'concat', 'a', 'b'))
        expected_results.append('ab')
        invokes.append(runner.call_contract(path, 'concat', 'unit', 'test'))
        expected_results.append('unittest')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_concatenation_augmented_assignment(self):
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

        path = self.get_contract_path('ConcatenationAugmentedAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_concat_string_variables_and_constants(self):
        path, _ = self.get_deploy_file_paths('ConcatStringVariablesAndConstants.py')

        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'concat'))
        expected_results.append('[1,2]')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region Division

    def test_division_operation(self):
        path = self.get_contract_path('Division.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_division_augmented_assignment(self):
        path = self.get_contract_path('DivisionAugmentedAssignment.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_division_builtin_type(self):
        path, _ = self.get_deploy_file_paths('DivisionBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.DESERIALIZE_VALUES // FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_integer_division_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.DIV
            + Opcode.RET
        )

        path = self.get_contract_path('IntegerDivision.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'floor_div', 10, 3))
        expected_results.append(3)
        invokes.append(runner.call_contract(path, 'floor_div', -42, -9))
        expected_results.append(4)
        invokes.append(runner.call_contract(path, 'floor_div', -100, 3))
        expected_results.append(-33)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_integer_division_augmented_assignment(self):
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

        path = self.get_contract_path('IntegerDivisionAugmentedAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    # endregion

    # region ListAddition

    def test_list_addition(self):
        path, _ = self.get_deploy_file_paths('ListAddition.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'add_any', [1, 'str', '123'], [2, True, False]))
        expected_results.append([1, 'str', '123'] + [2, True, False])
        invokes.append(runner.call_contract(path, 'add_int', [1, 3], [2, 5]))
        expected_results.append([1, 3] + [2, 5])
        invokes.append(runner.call_contract(path, 'add_bool', [True], [False, True]))
        expected_results.append([True] + [False, True])
        invokes.append(runner.call_contract(path, 'add_str', ['unit', ' '], ['test', '.']))
        expected_results.append(['unit', ' '] + ['test', '.'])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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

    def test_mixed_operations(self):
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

        path = self.get_contract_path('MixedOperations.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'mixed', 10, 20, 30, 40, 50))
        expected_results.append(10 + 30 * 50 + 40 // 20)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mixed_operations_with_parentheses(self):
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

        path = self.get_contract_path('WithParentheses.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'mixed', 10, 20, 30, 40, 50))
        expected_results.append(10 + 30 * (50 + 40) // 20)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region Modulo

    def test_modulo_operation(self):
        path, _ = self.get_deploy_file_paths('Modulo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        op1 = 10
        op2 = 3
        expected_output = op1 % op2
        invokes.append(runner.call_contract(path, 'mod', op1, op2))
        expected_results.append(expected_output)

        op1 = -42
        op2 = -9
        expected_output = op1 % op2
        invokes.append(runner.call_contract(path, 'mod', op1, op2))
        expected_results.append(expected_output)

        op1 = -100
        op2 = 3
        expected_output = op1 % op2
        invokes.append(runner.call_contract(path, 'mod', op1, op2))
        expected_results.append(expected_output)

        op1 = 100
        op2 = -3
        expected_output = op1 % op2
        invokes.append(runner.call_contract(path, 'mod', op1, op2))
        expected_results.append(expected_output)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_modulo_augmented_assignment(self):
        path, _ = self.get_deploy_file_paths('ModuloAugmentedAssignment.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        op1 = 10
        op2 = 3
        expected_output = op1 % op2
        invokes.append(runner.call_contract(path, 'mod', op1, op2))
        expected_results.append(expected_output)

        op1 = -42
        op2 = -9
        expected_output = op1 % op2
        invokes.append(runner.call_contract(path, 'mod', op1, op2))
        expected_results.append(expected_output)

        op1 = -100
        op2 = 3
        expected_output = op1 % op2
        invokes.append(runner.call_contract(path, 'mod', op1, op2))
        expected_results.append(expected_output)

        op1 = 100
        op2 = -3
        expected_output = op1 % op2
        invokes.append(runner.call_contract(path, 'mod', op1, op2))
        expected_results.append(expected_output)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_modulo_builtin_type(self):
        path, _ = self.get_deploy_file_paths('ModuloBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.DESERIALIZE_VALUES % FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region Multiplication

    def test_multiplication_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MUL
            + Opcode.RET
        )

        path = self.get_contract_path('Multiplication.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'mult', 10, 3))
        expected_results.append(30)
        invokes.append(runner.call_contract(path, 'mult', -42, -2))
        expected_results.append(84)
        invokes.append(runner.call_contract(path, 'mult', -4, 20))
        expected_results.append(-80)
        invokes.append(runner.call_contract(path, 'mult', 0, 20))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_multiplication_augmented_assignment(self):
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

        path = self.get_contract_path('MultiplicationAugmentedAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_multiplication_builtin_type(self):
        path, _ = self.get_deploy_file_paths('MultiplicationBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.DESERIALIZE_VALUES * FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region Power

    def test_power_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.POW
            + Opcode.RET
        )
        path = self.get_contract_path('Power.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'pow', 10, 3))
        expected_results.append(1000)
        invokes.append(runner.call_contract(path, 'pow', 1, 15))
        expected_results.append(1)
        invokes.append(runner.call_contract(path, 'pow', -2, 2))
        expected_results.append(4)
        invokes.append(runner.call_contract(path, 'pow', 0, 20))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'pow', 1, -2)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, '^Invalid shift value')

    def test_power_augmented_assignment(self):
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
        path = self.get_contract_path('PowerAugmentedAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_power_builtin_type(self):
        path, _ = self.get_deploy_file_paths('PowerBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.DESERIALIZE_VALUES ** FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region Sign

    def test_negative_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.NEGATE
            + Opcode.RET
        )

        path = self.get_contract_path('Negative.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'minus', 10))
        expected_results.append(-10)
        invokes.append(runner.call_contract(path, 'minus', -1))
        expected_results.append(1)
        invokes.append(runner.call_contract(path, 'minus', 0))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_negative_builtin_type(self):
        path, _ = self.get_deploy_file_paths('NegativeBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'minus', FindOptions.DESERIALIZE_VALUES))
        expected_results.append(-FindOptions.DESERIALIZE_VALUES)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_positive_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.RET
        )

        path = self.get_contract_path('Positive.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'plus', 10))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'plus', -1))
        expected_results.append(-1)
        invokes.append(runner.call_contract(path, 'plus', 0))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_positive_builtin_type(self):
        path, _ = self.get_deploy_file_paths('PositiveBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'plus', FindOptions.DESERIALIZE_VALUES))
        expected_results.append(+FindOptions.DESERIALIZE_VALUES)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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

    def test_bytes_multiplication_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + self.byte_str_mult
            + Opcode.RET
        )

        path = self.get_contract_path('BytesMultiplication.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'bytes_mult', b'a', 4,
                                            expected_result_type=bytes))
        expected_results.append(b'aaaa')
        invokes.append(runner.call_contract(path, 'bytes_mult', b'unit', 50,
                                            expected_result_type=bytes))
        expected_results.append(b'unit' * 50)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_multiplication_operation_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + self.byte_str_mult
            + Opcode.STARG0
            + Opcode.LDARG0
            + Opcode.RET
        )

        path = self.get_contract_path('BytesMultiplicationAugmentedAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', b'unit', 50,
                                            expected_result_type=bytes))
        expected_results.append(b'unit' * 50)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_multiplication_builtin_type(self):
        path, _ = self.get_deploy_file_paths('BytesMultiplicationBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'bytes_mult', b'unit test', FindOptions.VALUES_ONLY,
                                            expected_result_type=bytes))
        expected_results.append(b'unit test' * FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_multiplication_operation(self):
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

        path = self.get_contract_path('StringMultiplication.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'str_mult', 'a', 4))
        expected_results.append('aaaa')
        invokes.append(runner.call_contract(path, 'str_mult', 'unit', 50))
        expected_results.append('unit' * 50)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_multiplication_operation_augmented_assignment(self):
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

        path = self.get_contract_path('StringMultiplicationAugmentedAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'unit', 50))
        expected_results.append('unit' * 50)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_multiplication_builtin_type(self):
        path, _ = self.get_deploy_file_paths('StringMultiplicationBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'str_mult', 'unit test', FindOptions.VALUES_ONLY))
        expected_results.append('unit test' * FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region Subtraction

    def test_subtraction_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SUB
            + Opcode.RET
        )

        path = self.get_contract_path('Subtraction.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'sub', 10, 3))
        expected_results.append(7)
        invokes.append(runner.call_contract(path, 'sub', -42, -24))
        expected_results.append(-18)
        invokes.append(runner.call_contract(path, 'sub', -42, 24))
        expected_results.append(-66)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_subtraction_augmented_assignment(self):
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

        path = self.get_contract_path('SubtractionAugmentedAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_subtraction_builtin_type(self):
        path, _ = self.get_deploy_file_paths('SubtractionBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.DESERIALIZE_VALUES, FindOptions.VALUES_ONLY))
        expected_results.append(FindOptions.DESERIALIZE_VALUES - FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion
