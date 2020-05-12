from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation, UnresolvedReference
from boa3.neo.vm.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest


class TestArithmetic(BoaTest):

    def test_addition_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH4
            + Opcode.PUSH2
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/Addition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_subtraction_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH4
            + Opcode.PUSH2
            + Opcode.SUB
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/Subtraction.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_multiplication_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH4
            + Opcode.PUSH2
            + Opcode.MUL
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/Multiplication.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_division_operation(self):
        path = '%s/boa3_test/example/arithmetic_test/Division.py' % self.dirname

        with self.assertRaises(UnresolvedReference):
            output = Boa3.compile(path)

    def test_integer_division_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH4
            + Opcode.PUSH2
            + Opcode.DIV
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/IntegerDivision.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_modulo_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH4
            + Opcode.PUSH2
            + Opcode.MOD
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/Modulo.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_positive_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH8
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/Positive.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_negative_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH8
            + Opcode.NEGATE
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/Negative.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_concatenation_operation(self):
        path = '%s/boa3_test/example/arithmetic_test/Concatenation.py' % self.dirname

        with self.assertRaises(NotSupportedOperation):
            output = Boa3.compile(path)

    def test_exponentiation_operation(self):
        path = '%s/boa3_test/example/arithmetic_test/Exponentiation.py' % self.dirname

        with self.assertRaises(UnresolvedReference):
            output = Boa3.compile(path)

    def test_mismatched_type_binary_operation(self):
        path = '%s/boa3_test/example/arithmetic_test/MismatchedOperandBinary.py' % self.dirname

        with self.assertRaises(MismatchedTypes):
            output = Boa3.compile(path)

    def test_mismatched_type_unary_operation(self):
        path = '%s/boa3_test/example/arithmetic_test/MismatchedOperandUnary.py' % self.dirname

        with self.assertRaises(MismatchedTypes):
            output = Boa3.compile(path)

    def test_sequence_addition(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH8
            + Opcode.PUSH4
            + Opcode.ADD
            + Opcode.PUSH2
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/AdditionThreeElements.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mixed_operations(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PUSH5
            + Opcode.MUL        # multiplicative operations
            + Opcode.ADD        # additive operations
            + Opcode.PUSH4
            + Opcode.NEGATE     # parentheses
            + Opcode.PUSH2
            + Opcode.DIV        # multiplicative
            + Opcode.SUB        # additive
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/MixedOperations.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mixed_operations_with_parentheses(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x00'
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.NEGATE     # inside parentheses
            + Opcode.SUB        # parentheses
            + Opcode.MUL        # multiplicative operations
            + Opcode.PUSH2
            + Opcode.DIV        # multiplicative
            + Opcode.ADD        # additive operations
            + Opcode.RET
        )

        path = '%s/boa3_test/example/arithmetic_test/WithParentheses.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)
