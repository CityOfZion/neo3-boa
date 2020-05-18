import sys
from typing import Dict

from boa3.boa3 import Boa3
from boa3.compiler.compiler import Compiler
from boa3.exception.CompilerError import NotSupportedOperation, UnresolvedReference
from boa3.model.method import Method
from boa3.model.symbol import ISymbol
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest


class TestVariable(BoaTest):

    def test_declaration_with_type(self):
        path = '%s/boa3_test/example/variable_test/DeclarationWithType.py' % self.dirname

        test_variable_id = 'a'
        test_method_id = 'Main'
        compiler = Compiler()

        expected_compiler_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.RET        # return
        )
        compiler_output = compiler.compile(path)
        self.assertEqual(expected_compiler_output, compiler_output)

        main_symbol_table: Dict[str, ISymbol] = self.get_compiler_analyser(compiler).symbol_table
        # the variable is local to a method, so it shouldn't be in the main symbol table
        self.assertFalse(test_variable_id in main_symbol_table)

        self.assertTrue(test_method_id in main_symbol_table)
        self.assertIsInstance(main_symbol_table[test_method_id], Method)
        method: Method = main_symbol_table[test_method_id]

        method_symbol_table: Dict[str, Variable] = method.symbols
        # the variable is local to this method, so it should be in the method symbol table
        self.assertTrue(test_variable_id in method_symbol_table)

    def test_declaration_without_type(self):
        path = '%s/boa3_test/example/variable_test/DeclarationWithoutType.py' % self.dirname

        with self.assertRaises(UnresolvedReference):
            output = Boa3.compile(path)

    def test_assignment_with_type(self):
        input = 'unit_test'
        byte_input = bytes(input, sys.getdefaultencoding())
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # assignment value
            + len(byte_input).to_bytes(1, sys.byteorder)
            + byte_input
            + Opcode.STLOC0     # variable address
            + Opcode.RET
        )

        path = '%s/boa3_test/example/variable_test/AssignmentWithType.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_assignment_without_type(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # assignment value
            + Opcode.STLOC0     # variable address
            + Opcode.RET
        )

        path = '%s/boa3_test/example/variable_test/AssignmentWithoutType.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_argument_assignment(self):
        input = 'unit_test'
        byte_input = bytes(input, sys.getdefaultencoding())
        expected_output = (
                Opcode.INITSLOT         # function signature
                + b'\x00'
                + b'\x01'
                + Opcode.PUSHDATA1      # assignment value
                + len(byte_input).to_bytes(1, sys.byteorder)
                + byte_input
                + Opcode.STARG0         # variable address
                + Opcode.RET
        )

        path = '%s/boa3_test/example/variable_test/ArgumentAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_multiple_assignments(self):
        path = '%s/boa3_test/example/variable_test/MultipleAssignments.py' % self.dirname

        with self.assertRaises(NotSupportedOperation):
            output = Boa3.compile(path)

    def test_tuple_multiple_assignments(self):
        path = '%s/boa3_test/example/variable_test/AssignmentWithTuples.py' % self.dirname

        with self.assertRaises(NotSupportedOperation):
            output = Boa3.compile(path)

    def test_many_assignments(self):
        expected_output = (
            Opcode.INITSLOT         # function signature
            + b'\x08'
            + b'\x00'
            + Opcode.PUSH0          # function body
            + Opcode.STLOC0
            + Opcode.PUSH1
            + Opcode.STLOC1
            + Opcode.PUSH2
            + Opcode.STLOC2
            + Opcode.PUSH3
            + Opcode.STLOC3
            + Opcode.PUSH4
            + Opcode.STLOC4
            + Opcode.PUSH5
            + Opcode.STLOC5
            + Opcode.PUSH6
            + Opcode.STLOC6
            + Opcode.PUSH7
            + Opcode.STLOC          # variable index greater than 6 uses another opcode
            + b'\x07'
            + Opcode.RET
        )

        path = '%s/boa3_test/example/variable_test/ManyAssignments.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_return_arg_value(self):
        expected_output = (
            Opcode.INITSLOT.value       # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0.value       # variable address
            + Opcode.RET.value
        )

        path = '%s/boa3_test/example/variable_test/ReturnArgument.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_return_local_var_value(self):
        expected_output = (
            Opcode.INITSLOT.value       # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH1.value
            + Opcode.STLOC0.value
            + Opcode.LDLOC0.value       # variable address
            + Opcode.RET.value
        )

        path = '%s/boa3_test/example/variable_test/ReturnLocalVariable.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_assign_local_with_arg_value(self):
        expected_output = (
            Opcode.INITSLOT.value       # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0.value
            + Opcode.STLOC0.value
            + Opcode.LDLOC0.value       # variable address
            + Opcode.RET.value
        )

        path = '%s/boa3_test/example/variable_test/AssignLocalWithArgument.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_using_undeclared_variable(self):
        path = '%s/boa3_test/example/variable_test/UsingUndeclaredVariable.py' % self.dirname

        with self.assertRaises(UnresolvedReference):
            output = Boa3.compile(path)

    def test_return_undeclared_variable(self):
        path = '%s/boa3_test/example/variable_test/ReturnUndeclaredVariable.py' % self.dirname

        with self.assertRaises(UnresolvedReference):
            output = Boa3.compile(path)
