from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo3.contracts import FindOptions
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestLogical(BoaTest):
    default_folder: str = 'test_sc/logical_test'

    # region BoolAnd

    def test_boolean_and(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.BOOLAND
            + Opcode.RET
        )

        path = self.get_contract_path('BoolAnd.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, True))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', True, False))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', False, True))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', False, False))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_type_binary_operation(self):
        path = self.get_contract_path('MismatchedOperandAnd.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region BoolNot

    def test_boolean_not(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.NOT
            + Opcode.RET
        )

        path = self.get_contract_path('BoolNot.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_type_unary_operation(self):
        path = self.get_contract_path('MismatchedOperandNot.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region BoolOr

    def test_boolean_or(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.BOOLOR
            + Opcode.RET
        )

        path = self.get_contract_path('BoolOr.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, True))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', True, False))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', False, True))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', False, False))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_sequence_boolean_or(self):
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

        path = self.get_contract_path('BoolOrThreeElements.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, False, False))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', False, True, False))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', False, False, False))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', True, True, True))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region LeftShift

    def test_logic_left_shift(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SHL
            + Opcode.RET
        )

        path = self.get_contract_path('LogicLeftShift.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', int('100', 2), 2))
        expected_results.append(int('10000', 2))
        invokes.append(runner.call_contract(path, 'Main', int('11', 2), 1))
        expected_results.append(int('110', 2))
        invokes.append(runner.call_contract(path, 'Main', int('101010', 2), 4))
        expected_results.append(int('1010100000', 2))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_left_shift_builtin_type(self):
        path, _ = self.get_deploy_file_paths('LogicLeftShiftBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.NONE, FindOptions.DESERIALIZE_VALUES))
        expected_results.append(FindOptions.NONE << FindOptions.DESERIALIZE_VALUES)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_type_logic_left_shift(self):
        path = self.get_contract_path('MismatchedOperandLogicLeftShift.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region LogicAnd

    def test_logic_and_with_bool_operand(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.AND
            + Opcode.RET
        )

        path = self.get_contract_path('LogicAndBool.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, True))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', True, False))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', False, False))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_and_with_int_operand(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.AND
            + Opcode.RET
        )

        path = self.get_contract_path('LogicAndInt.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 4, 6))
        expected_results.append(4 & 6)
        invokes.append(runner.call_contract(path, 'Main', 40, 6))
        expected_results.append(40 & 6)
        invokes.append(runner.call_contract(path, 'Main', -4, 32))
        expected_results.append(-4 & 32)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_and_builtin_type(self):
        path, _ = self.get_deploy_file_paths('LogicAndBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.NONE, FindOptions.DESERIALIZE_VALUES))
        expected_results.append(FindOptions.NONE & FindOptions.DESERIALIZE_VALUES)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_type_logic_and(self):
        path = self.get_contract_path('MismatchedOperandLogicAnd.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region LogicNot

    def test_logic_not_with_bool_operand(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.INVERT
            + Opcode.RET
        )

        path = self.get_contract_path('LogicNotBool.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(-2)
        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_not_builtin_type(self):
        path, _ = self.get_deploy_file_paths('LogicNotBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.VALUES_ONLY))
        expected_results.append(~FindOptions.VALUES_ONLY)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_not_with_int_operand(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.INVERT
            + Opcode.RET
        )

        path = self.get_contract_path('LogicNotInt.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 4))
        expected_results.append(-5)
        invokes.append(runner.call_contract(path, 'Main', 40))
        expected_results.append(-41)
        invokes.append(runner.call_contract(path, 'Main', -4))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_type_logic_not(self):
        path = self.get_contract_path('MismatchedOperandLogicNot.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region LogicOr

    def test_logic_or_with_bool_operand(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.OR
            + Opcode.RET
        )

        path = self.get_contract_path('LogicOrBool.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, True))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', True, False))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', False, False))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_or_with_int_operand(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.OR
            + Opcode.RET
        )

        path = self.get_contract_path('LogicOrInt.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 4, 6))
        expected_results.append(4 | 6)
        invokes.append(runner.call_contract(path, 'Main', 40, 6))
        expected_results.append(40 | 6)
        invokes.append(runner.call_contract(path, 'Main', -4, 32))
        expected_results.append(-4 | 32)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_or_builtin_type(self):
        path, _ = self.get_deploy_file_paths('LogicOrBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.REMOVE_PREFIX, FindOptions.KEYS_ONLY,
                                            expected_result_type=int))
        expected_results.append(int(FindOptions.REMOVE_PREFIX | FindOptions.KEYS_ONLY))

        invokes.append(runner.call_contract(path, 'main', FindOptions.REMOVE_PREFIX, FindOptions.KEYS_ONLY,
                                            expected_result_type=FindOptions))
        expected_results.append(FindOptions.REMOVE_PREFIX | FindOptions.KEYS_ONLY)

        invokes.append(runner.call_contract(path, 'main', 2, 4,
                                            expected_result_type=int))
        expected_results.append(int(2 | 4))

        invokes.append(runner.call_contract(path, 'main', 0, 123456789,
                                            expected_result_type=int))
        expected_results.append(123456789)

        invokes.append(runner.call_contract(path, 'main', 123456789, 0,
                                            expected_result_type=int))
        expected_results.append(123456789)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_type_logic_or(self):
        path = self.get_contract_path('MismatchedOperandLogicOr.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region LogicXor

    def test_logic_xor_with_bool_operand(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.XOR
            + Opcode.RET
        )

        path = self.get_contract_path('LogicXorBool.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, True))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', True, False))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', False, False))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_xor_with_int_operand(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.XOR
            + Opcode.RET
        )

        path = self.get_contract_path('LogicXorInt.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 4, 6))
        expected_results.append(4 ^ 6)
        invokes.append(runner.call_contract(path, 'Main', 40, 6))
        expected_results.append(40 ^ 6)
        invokes.append(runner.call_contract(path, 'Main', -4, 32))
        expected_results.append(-4 ^ 32)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_xor_builtin_type(self):
        path, _ = self.get_deploy_file_paths('LogicXorBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.NONE, FindOptions.DESERIALIZE_VALUES))
        expected_results.append(FindOptions.NONE ^ FindOptions.DESERIALIZE_VALUES)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_type_logic_xor(self):
        path = self.get_contract_path('MismatchedOperandLogicXor.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region Mixed

    def test_logic_augmented_assignment(self):
        path, _ = self.get_deploy_file_paths('AugmentedAssignmentOperators.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = 1
        b = 4
        invokes.append(runner.call_contract(path, 'right_shift', a, b))
        expected_results.append(a >> b)

        a = 4
        b = 1
        invokes.append(runner.call_contract(path, 'left_shift', a, b))
        expected_results.append(a << b)

        a = 255
        b = 123
        invokes.append(runner.call_contract(path, 'l_and', a, b))
        expected_results.append(a & b)

        a = 255
        b = 123
        invokes.append(runner.call_contract(path, 'l_or', a, b))
        expected_results.append(a | b)

        a = 255
        b = 123
        invokes.append(runner.call_contract(path, 'xor', a, b))
        expected_results.append(a ^ b)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_logic_test(self):
        path, _ = self.get_deploy_file_paths('BinOpBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', '&', 4, 4))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', '|', 4, 3))
        expected_results.append(7)

        invokes.append(runner.call_contract(path, 'main', '|', 4, 8))
        expected_results.append(12)

        invokes.append(runner.call_contract(path, 'main', '^', 4, 4))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', '^', 4, 2))
        expected_results.append(6)

        invokes.append(runner.call_contract(path, 'main', '>>', 16, 2))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'main', '>>', 16, 0))
        expected_results.append(16)

        invokes.append(runner.call_contract(path, 'main', '%', 16, 2))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'main', '%', 16, 11))
        expected_results.append(5)

        invokes.append(runner.call_contract(path, 'main', '//', 16, 2))
        expected_results.append(8)

        invokes.append(runner.call_contract(path, 'main', '//', 16, 7))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'main', '~', 16, 0))
        expected_results.append(-17)

        invokes.append(runner.call_contract(path, 'main', '~', -3, 0))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mixed_operations(self):
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

        path = self.get_contract_path('MixedOperations.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True, False, False))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', False, True, False))
        expected_results.append(True)
        invokes.append(runner.call_contract(path, 'Main', False, False, False))
        expected_results.append(False)
        invokes.append(runner.call_contract(path, 'Main', True, True, True))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_operation_with_return_and_stack_filled(self):
        path, _ = self.get_deploy_file_paths('LogicOperationWithReturnAndStackFilled.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region RightShift

    def test_logic_right_shift(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SHR
            + Opcode.RET
        )

        path = self.get_contract_path('LogicRightShift.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', int('10000', 2), 2))
        expected_results.append(int('100', 2))
        invokes.append(runner.call_contract(path, 'Main', int('110', 2), 1))
        expected_results.append(int('11', 2))
        invokes.append(runner.call_contract(path, 'Main', int('1010100000', 2), 4))
        expected_results.append(int('101010', 2))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_logic_right_shift_builtin_type(self):
        path, _ = self.get_deploy_file_paths('LogicRightShiftBuiltinType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.NONE, FindOptions.DESERIALIZE_VALUES))
        expected_results.append(FindOptions.NONE >> FindOptions.DESERIALIZE_VALUES)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_type_logic_right_shift(self):
        path = self.get_contract_path('MismatchedOperandLogicRightShift.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion
