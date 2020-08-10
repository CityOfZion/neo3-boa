from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest


class TestLogical(BoaTest):

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

        path = '%s/boa3_test/test_sc/logical_test/BoolAnd.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/test_sc/logical_test/BoolOr.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_boolean_not(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.NOT
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/logical_test/BoolNot.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/test_sc/logical_test/BoolOrThreeElements.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mismatched_type_binary_operation(self):
        path = '%s/boa3_test/test_sc/logical_test/MismatchedOperandAnd.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_type_unary_operation(self):
        path = '%s/boa3_test/test_sc/logical_test/MismatchedOperandNot.py' % self.dirname
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

        path = '%s/boa3_test/test_sc/logical_test/MixedOperations.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/test_sc/logical_test/LogicAndBool.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/test_sc/logical_test/LogicAndInt.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mismatched_type_logic_and(self):
        path = '%s/boa3_test/test_sc/logical_test/MismatchedOperandLogicAnd.py' % self.dirname
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

        path = '%s/boa3_test/test_sc/logical_test/LogicOrBool.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/test_sc/logical_test/LogicOrInt.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mismatched_type_logic_or(self):
        path = '%s/boa3_test/test_sc/logical_test/MismatchedOperandLogicOr.py' % self.dirname
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

        path = '%s/boa3_test/test_sc/logical_test/LogicNotBool.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_logic_not_with_int_operand(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.INVERT
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/logical_test/LogicNotInt.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mismatched_type_logic_not(self):
        path = '%s/boa3_test/test_sc/logical_test/MismatchedOperandLogicNot.py' % self.dirname
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

        path = '%s/boa3_test/test_sc/logical_test/LogicXorBool.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/test_sc/logical_test/LogicXorInt.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mismatched_type_logic_xor(self):
        path = '%s/boa3_test/test_sc/logical_test/MismatchedOperandLogicXor.py' % self.dirname
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

        path = '%s/boa3_test/test_sc/logical_test/LogicLeftShift.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mismatched_type_logic_left_shift(self):
        path = '%s/boa3_test/test_sc/logical_test/MismatchedOperandLogicLeftShift.py' % self.dirname
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

        path = '%s/boa3_test/test_sc/logical_test/LogicRightShift.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mismatched_type_logic_right_shift(self):
        path = '%s/boa3_test/test_sc/logical_test/MismatchedOperandLogicRightShift.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
