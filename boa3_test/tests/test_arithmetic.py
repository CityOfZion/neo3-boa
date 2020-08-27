from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation
from boa3.model.operation.binaryop import BinaryOp
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest


class TestArithmetic(BoaTest):

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

        path = '%s/boa3_test/test_sc/arithmetic_test/Addition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/test_sc/arithmetic_test/Subtraction.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/test_sc/arithmetic_test/Multiplication.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_division_operation(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/Division.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

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

        path = '%s/boa3_test/test_sc/arithmetic_test/IntegerDivision.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_modulo_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MOD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Modulo.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_positive_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Positive.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_negative_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.NEGATE
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Negative.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_concatenation_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CAT
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Concatenation.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_power_operation(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/Power.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_str_multiplication_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + BinaryOp.StrMul.bytecode
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/StringMultiplication.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mismatched_type_binary_operation(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/MismatchedOperandBinary.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_type_unary_operation(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/MismatchedOperandUnary.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_sequence_addition(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH4
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/AdditionThreeElements.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mixed_operations(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x05'
            + Opcode.LDARG0
            + Opcode.LDARG2
            + Opcode.LDARG4
            + Opcode.MUL        # multiplicative operations
            + Opcode.ADD        # additive operations
            + Opcode.LDARG3
            + Opcode.NEGATE     # parentheses
            + Opcode.LDARG1
            + Opcode.DIV        # multiplicative
            + Opcode.SUB        # additive
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/MixedOperations.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_mixed_operations_with_parentheses(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x05'
            + Opcode.LDARG0
            + Opcode.LDARG2
            + Opcode.LDARG4
            + Opcode.LDARG3
            + Opcode.NEGATE     # inside parentheses
            + Opcode.SUB        # parentheses
            + Opcode.MUL        # multiplicative operations
            + Opcode.LDARG1
            + Opcode.DIV        # multiplicative
            + Opcode.ADD        # additive operations
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/WithParentheses.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_addition_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/AdditionAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_subtraction_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SUB
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/SubtractionAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_multiplication_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MUL
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/MultiplicationAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_division_augmented_assignment(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/DivisionAugmentedAssignment.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_integer_division_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.DIV
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/IntegerDivisionAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_modulo_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MOD
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/ModuloAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_concatenation_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CAT
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/ConcatenationAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_power_augmented_assignment(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/PowerAugmentedAssignment.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_str_multiplication_operation_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + BinaryOp.StrMul.bytecode
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/StringMultiplicationAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)
