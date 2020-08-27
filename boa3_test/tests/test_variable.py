from typing import Dict

from boa3.boa3 import Boa3
from boa3.compiler.compiler import Compiler
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation, UnresolvedReference
from boa3.model.method import Method
from boa3.model.symbol import ISymbol
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestVariable(BoaTest):

    def test_declaration_with_type(self):
        path = '%s/boa3_test/test_sc/variable_test/DeclarationWithType.py' % self.dirname

        test_variable_id = 'a'
        test_method_id = 'Main'
        compiler = Compiler()

        expected_compiler_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHNULL
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
        path = '%s/boa3_test/test_sc/variable_test/DeclarationWithoutType.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_assignment_with_type(self):
        input = 'unit_test'
        byte_input = String(input).to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # assignment value
            + Integer(len(byte_input)).to_byte_array(min_length=1)
            + byte_input
            + Opcode.STLOC0     # variable address
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/variable_test/AssignmentWithType.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_assignment_without_type(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # assignment value
            + Opcode.STLOC0     # variable address
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/variable_test/AssignmentWithoutType.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_argument_assignment(self):
        input = 'unit_test'
        byte_input = String(input).to_bytes()
        expected_output = (
            Opcode.INITSLOT         # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.PUSHDATA1      # assignment value
            + Integer(len(byte_input)).to_byte_array(min_length=1)
            + byte_input
            + Opcode.STARG0         # variable address
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/variable_test/ArgumentAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_multiple_assignments(self):
        path = '%s/boa3_test/test_sc/variable_test/MultipleAssignments.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_tuple_multiple_assignments(self):
        path = '%s/boa3_test/test_sc/variable_test/AssignmentWithTuples.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/variable_test/ManyAssignments.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_return_arg_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # variable address
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/variable_test/ReturnArgument.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_return_local_var_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH1
            + Opcode.STLOC0
            + Opcode.LDLOC0     # variable address
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/variable_test/ReturnLocalVariable.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_assign_local_with_arg_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0     # variable address
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/variable_test/AssignLocalWithArgument.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_using_undeclared_variable(self):
        path = '%s/boa3_test/test_sc/variable_test/UsingUndeclaredVariable.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_return_undeclared_variable(self):
        path = '%s/boa3_test/test_sc/variable_test/ReturnUndeclaredVariable.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_assign_value_mismatched_type(self):
        path = '%s/boa3_test/test_sc/variable_test/MismatchedTypeAssignValue.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_assign_binary_operation_mismatched_type(self):
        path = '%s/boa3_test/test_sc/variable_test/MismatchedTypeAssignBinOp.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_assign_unary_operation_mismatched_type(self):
        path = '%s/boa3_test/test_sc/variable_test/MismatchedTypeAssignUnOp.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_assign_mixed_operations_mismatched_type(self):
        path = '%s/boa3_test/test_sc/variable_test/MismatchedTypeAssignMixedOp.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_assign_sequence_get_mismatched_type(self):
        path = '%s/boa3_test/test_sc/variable_test/MismatchedTypeAssignSequenceGet.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_assign_sequence_set_mismatched_type(self):
        path = '%s/boa3_test/test_sc/variable_test/MismatchedTypeAssignSequenceSet.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_aug_assign_mismatched_type(self):
        path = '%s/boa3_test/test_sc/variable_test/MismatchedTypeAugAssign.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_global_declaration_with_assignment(self):
        expected_output = (
            Opcode.LDSFLD0
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH10
            + Opcode.STSFLD0    # a = 10
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/variable_test/GlobalDeclarationWithArgumentWrittenAfter.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_global_declaration_without_assignment(self):
        path = '%s/boa3_test/test_sc/variable_test/GlobalDeclarationWithoutAssignment.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_global_assignment_with_type(self):
        expected_output = (
            Opcode.LDSFLD0
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH10
            + Opcode.STSFLD0    # a = 10
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/variable_test/GlobalAssignmentWithType.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_global_assignment_without_type(self):
        expected_output = (
            Opcode.LDSFLD0
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH10
            + Opcode.STSFLD0    # a = 10
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/variable_test/GlobalAssignmentWithoutType.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_global_tuple_multiple_assignments(self):
        path = '%s/boa3_test/test_sc/variable_test/GlobalAssignmentWithTuples.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_many_global_assignments(self):
        expected_output = (
            Opcode.LDSFLD + b'\x07'
            + Opcode.LDSFLD6    # [a, b, c, d, e, f, g, h]
            + Opcode.LDSFLD5
            + Opcode.LDSFLD4
            + Opcode.LDSFLD3
            + Opcode.LDSFLD2
            + Opcode.LDSFLD1
            + Opcode.LDSFLD0
            + Opcode.PUSH8
            + Opcode.PACK       # return [a, b, c, d, e, f, g, h]
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x08'           # number of globals
            + Opcode.PUSH0      # a = 0
            + Opcode.STSFLD0
            + Opcode.PUSH1      # b = 1
            + Opcode.STSFLD1
            + Opcode.PUSH2      # c = 2
            + Opcode.STSFLD2
            + Opcode.PUSH3      # d = 3
            + Opcode.STSFLD3
            + Opcode.PUSH4      # e = 4
            + Opcode.STSFLD4
            + Opcode.PUSH5      # f = 5
            + Opcode.STSFLD5
            + Opcode.PUSH6      # g = 6
            + Opcode.STSFLD6
            + Opcode.PUSH7      # h = 7
            + Opcode.STSFLD + b'\x07'   # variable index greater than 6 uses another opcode
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/variable_test/ManyGlobalAssignments.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_global_assignment_between_functions(self):
        expected_output = (
            Opcode.LDSFLD0
            + Opcode.RET
            + Opcode.LDSFLD1
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x02'           # number of globals
            + Opcode.PUSH10     # a = 10
            + Opcode.STSFLD0
            + Opcode.PUSH5      # b = 5
            + Opcode.STSFLD1
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/variable_test/GlobalAssignmentBetweenFunctions.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_get_global_variable_value_written_after(self):
        expected_output = (
            Opcode.LDSFLD + b'\x07'
            + Opcode.LDSFLD6    # [a, b, c, d, e, f, g, h]
            + Opcode.LDSFLD5
            + Opcode.LDSFLD4
            + Opcode.LDSFLD3
            + Opcode.LDSFLD2
            + Opcode.LDSFLD1
            + Opcode.LDSFLD0
            + Opcode.PUSH8
            + Opcode.PACK       # return [a, b, c, d, e, f, g, h]
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x08'           # number of globals
            + Opcode.PUSH0      # a = 0
            + Opcode.STSFLD0
            + Opcode.PUSH1      # b = 1
            + Opcode.STSFLD1
            + Opcode.PUSH2      # c = 2
            + Opcode.STSFLD2
            + Opcode.PUSH3      # d = 3
            + Opcode.STSFLD3
            + Opcode.PUSH4      # e = 4
            + Opcode.STSFLD4
            + Opcode.PUSH5      # f = 5
            + Opcode.STSFLD5
            + Opcode.PUSH6      # g = 6
            + Opcode.STSFLD6
            + Opcode.PUSH7      # h = 7
            + Opcode.STSFLD + b'\x07'   # variable index greater than 6 uses another opcode
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/variable_test/GetGlobalValueWrittenAfter.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_assign_local_shadowing_global_with_arg_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # b = a  // this b is not the global b
            + Opcode.STLOC0
            + Opcode.LDLOC0     # variable address
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH0      # b = 0
            + Opcode.STSFLD0
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/variable_test/AssignLocalWithArgumentShadowingGlobal.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_assign_global_in_function(self):
        path = '%s/boa3_test/test_sc/variable_test/GlobalAssignmentInFunctionWithArgument.py' % self.dirname

        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)
