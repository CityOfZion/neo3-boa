from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestLogical(BoaTest):

    default_folder: str = 'test_sc/logical_test'

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True, True)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', True, False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False, True)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False, False)
        self.assertEqual(False, result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True, True)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', True, False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False, True)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False, False)
        self.assertEqual(False, result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(True, result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True, False, False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False, True, False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False, False, False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', True, True, True)
        self.assertEqual(True, result)

    def test_mismatched_type_binary_operation(self):
        path = self.get_contract_path('MismatchedOperandAnd.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_type_unary_operation(self):
        path = self.get_contract_path('MismatchedOperandNot.py')
        self.assertCompilerLogs(MismatchedTypes, path)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True, False, False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False, True, False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False, False, False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', True, True, True)
        self.assertEqual(False, result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True, True)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', True, False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', False, False)
        self.assertEqual(False, result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 4, 6)
        self.assertEqual(4 & 6, result)
        result = self.run_smart_contract(engine, path, 'Main', 40, 6)
        self.assertEqual(40 & 6, result)
        result = self.run_smart_contract(engine, path, 'Main', -4, 32)
        self.assertEqual(-4 & 32, result)

    def test_mismatched_type_logic_and(self):
        path = self.get_contract_path('MismatchedOperandLogicAnd.py')
        self.assertCompilerLogs(MismatchedTypes, path)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True, True)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', True, False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False, False)
        self.assertEqual(False, result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 4, 6)
        self.assertEqual(4 | 6, result)
        result = self.run_smart_contract(engine, path, 'Main', 40, 6)
        self.assertEqual(40 | 6, result)
        result = self.run_smart_contract(engine, path, 'Main', -4, 32)
        self.assertEqual(-4 | 32, result)

    def test_mismatched_type_logic_or(self):
        path = self.get_contract_path('MismatchedOperandLogicOr.py')
        self.assertCompilerLogs(MismatchedTypes, path)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True)
        self.assertEqual(-2, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(-1, result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 4)
        self.assertEqual(-5, result)
        result = self.run_smart_contract(engine, path, 'Main', 40)
        self.assertEqual(-41, result)
        result = self.run_smart_contract(engine, path, 'Main', -4)
        self.assertEqual(3, result)

    def test_mismatched_type_logic_not(self):
        path = self.get_contract_path('MismatchedOperandLogicNot.py')
        self.assertCompilerLogs(MismatchedTypes, path)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', True, True)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', True, False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', False, False)
        self.assertEqual(False, result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 4, 6)
        self.assertEqual(4 ^ 6, result)
        result = self.run_smart_contract(engine, path, 'Main', 40, 6)
        self.assertEqual(40 ^ 6, result)
        result = self.run_smart_contract(engine, path, 'Main', -4, 32)
        self.assertEqual(-4 ^ 32, result)

    def test_mismatched_type_logic_xor(self):
        path = self.get_contract_path('MismatchedOperandLogicXor.py')
        self.assertCompilerLogs(MismatchedTypes, path)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', int('100', 2), 2)
        self.assertEqual(int('10000', 2), result)
        result = self.run_smart_contract(engine, path, 'Main', int('11', 2), 1)
        self.assertEqual(int('110', 2), result)
        result = self.run_smart_contract(engine, path, 'Main', int('101010', 2), 4)
        self.assertEqual(int('1010100000', 2), result)

    def test_mismatched_type_logic_left_shift(self):
        path = self.get_contract_path('MismatchedOperandLogicLeftShift.py')
        self.assertCompilerLogs(MismatchedTypes, path)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', int('10000', 2), 2)
        self.assertEqual(int('100', 2), result)
        result = self.run_smart_contract(engine, path, 'Main', int('110', 2), 1)
        self.assertEqual(int('11', 2), result)
        result = self.run_smart_contract(engine, path, 'Main', int('1010100000', 2), 4)
        self.assertEqual(int('101010', 2), result)

    def test_mismatched_type_logic_right_shift(self):
        path = self.get_contract_path('MismatchedOperandLogicRightShift.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_boa2_logic_test(self):
        path = self.get_contract_path('BinOpBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', '&', 4, 4)
        self.assertEqual(4, result)

        result = self.run_smart_contract(engine, path, 'main', '|', 4, 3)
        self.assertEqual(7, result)

        result = self.run_smart_contract(engine, path, 'main', '|', 4, 8)
        self.assertEqual(12, result)

        result = self.run_smart_contract(engine, path, 'main', '^', 4, 4)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', '^', 4, 2)
        self.assertEqual(6, result)

        result = self.run_smart_contract(engine, path, 'main', '>>', 16, 2)
        self.assertEqual(4, result)

        result = self.run_smart_contract(engine, path, 'main', '>>', 16, 0)
        self.assertEqual(16, result)

        result = self.run_smart_contract(engine, path, 'main', '%', 16, 2)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'main', '%', 16, 11)
        self.assertEqual(5, result)

        result = self.run_smart_contract(engine, path, 'main', '//', 16, 2)
        self.assertEqual(8, result)

        result = self.run_smart_contract(engine, path, 'main', '//', 16, 7)
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'main', '~', 16, 0)
        self.assertEqual(-17, result)

        result = self.run_smart_contract(engine, path, 'main', '~', -3, 0)
        self.assertEqual(2, result)
