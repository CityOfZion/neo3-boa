from typing import Dict

from boa3.boa3 import Boa3
from boa3.compiler.compiler import Compiler
from boa3.exception import CompilerError, CompilerWarning
from boa3.model.method import Method
from boa3.model.symbol import ISymbol
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestVariable(BoaTest):

    default_folder: str = 'test_sc/variable_test'

    def test_declaration_with_type(self):
        path = self.get_contract_path('DeclarationWithType.py')

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
        path = self.get_contract_path('DeclarationWithoutType.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

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
            + Opcode.RET
        )

        path = self.get_contract_path('AssignmentWithType.py')
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

        path = self.get_contract_path('AssignmentWithoutType.py')
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
            + Opcode.RET
        )

        path = self.get_contract_path('ArgumentAssignment.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_multiple_assignments(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH1      # a = b = c = True
            + Opcode.DUP            # c = True
            + Opcode.STLOC2
            + Opcode.DUP            # b = True
            + Opcode.STLOC1
            + Opcode.STLOC0         # a = True
            + Opcode.RET        # return
        )

        path = self.get_contract_path('MultipleAssignments.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_multiple_assignments_set_sequence(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSH2      # c = a[2] = b = 2
            + Opcode.DUP            # b = 2
            + Opcode.STLOC2
            + Opcode.LDLOC0         # a[2] = 2
            + Opcode.PUSH2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SETITEM
            + Opcode.STLOC1         # c = 2
            + Opcode.RET        # return
        )

        path = self.get_contract_path('MultipleAssignmentsSetSequence.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_multiple_assignments_set_sequence_last(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSH2      # a[2] = c = b = 2
            + Opcode.DUP            # b = 2
            + Opcode.STLOC2
            + Opcode.DUP            # c = 2
            + Opcode.STLOC1
            + Opcode.PUSH2          # a[2] = 2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.LDLOC0
            + Opcode.REVERSE3
            + Opcode.SETITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('MultipleAssignmentsSetSequenceLast.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_multiple_assignments_mismatched_type(self):
        string = String('str').to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSHDATA1      # c = 'str'
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.STLOC0
            + Opcode.PUSH1      # a = b = c = True
            + Opcode.DUP            # c = True
            + Opcode.STLOC0
            + Opcode.DUP            # b = True
            + Opcode.STLOC2
            + Opcode.STLOC1         # a = True
            + Opcode.RET        # return
        )

        path = self.get_contract_path('MismatchedTypeMultipleAssignments.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_multiple_assignments(self):
        path = self.get_contract_path('AssignmentWithTuples.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

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

        path = self.get_contract_path('ManyAssignments.py')
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

        path = self.get_contract_path('ReturnArgument.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', -140)
        self.assertEqual(-140, result)

    def test_return_local_var_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH1
            + Opcode.STLOC0
            + Opcode.PUSH1      # variable address
            + Opcode.RET
        )

        path = self.get_contract_path('ReturnLocalVariable.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', -140)
        self.assertEqual(1, result)

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

        path = self.get_contract_path('AssignLocalWithArgument.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', -140)
        self.assertEqual(-140, result)

    def test_using_undeclared_variable(self):
        path = self.get_contract_path('UsingUndeclaredVariable.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_return_undeclared_variable(self):
        path = self.get_contract_path('ReturnUndeclaredVariable.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_assign_value_mismatched_type(self):
        string_value = '1'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1    # a = '1'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeAssignValue.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_assign_binary_operation_mismatched_type(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3    # a = 1 + 2
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeAssignBinOp.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_assign_unary_operation_mismatched_type(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5    # a = -5
            + Opcode.NEGATE
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeAssignUnOp.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_assign_mixed_operations_mismatched_type(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x03'
            + Opcode.LDARG1     # b = min <= a - 2 <= max
            + Opcode.LDARG0
            + Opcode.PUSH2
            + Opcode.SUB
            + Opcode.LE
            + Opcode.LDARG0
            + Opcode.PUSH2
            + Opcode.SUB
            + Opcode.LDARG2
            + Opcode.LE
            + Opcode.BOOLAND
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeAssignMixedOp.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_assign_sequence_get_mismatched_type(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # b = a[0]
            + Opcode.PUSH0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeAssignSequenceGet.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_assign_sequence_set_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeAssignSequenceSet.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_aug_assign_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeAugAssign.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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
        path = self.get_contract_path('GlobalDeclarationWithArgumentWrittenAfter.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(10, result)

    def test_global_declaration_without_assignment(self):
        path = self.get_contract_path('GlobalDeclarationWithoutAssignment.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

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
        path = self.get_contract_path('GlobalAssignmentWithType.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(10, result)

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
        path = self.get_contract_path('GlobalAssignmentWithoutType.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(10, result)

    def test_global_tuple_multiple_assignments(self):
        path = self.get_contract_path('GlobalAssignmentWithTuples.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

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

        path = self.get_contract_path('ManyGlobalAssignments.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7], result)

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
        path = self.get_contract_path('GlobalAssignmentBetweenFunctions.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'example')
        self.assertEqual(5, result)

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
        path = self.get_contract_path('GetGlobalValueWrittenAfter.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7], result)

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
        path = self.get_contract_path('AssignLocalWithArgumentShadowingGlobal.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', -140)
        self.assertEqual(-140, result)

    def test_assign_global_in_function_with_global_keyword(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # b = a
            + Opcode.STSFLD0
            + Opcode.LDSFLD0    # return b
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH0      # b = 0
            + Opcode.STSFLD0
            + Opcode.RET
        )
        path = self.get_contract_path('GlobalAssignmentInFunctionWithArgument.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(10, result)

        result = self.run_smart_contract(engine, path, 'Main', -140)
        self.assertEqual(-140, result)

    def test_assign_void_function_call(self):
        path = self.get_contract_path('AssignVoidFunctionCall.py')
        self.compile_and_save(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(None, result)

    def test_anonymous_variable(self):
        path = self.get_contract_path('AnonymousVariable')
        self.compile_and_save(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(400, result)
