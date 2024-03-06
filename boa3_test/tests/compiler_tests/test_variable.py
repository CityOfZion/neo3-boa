from boa3.internal.compiler.compiler import Compiler
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestVariable(boatestcase.BoaTestCase):
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

        from boa3_test.tests.boa_test import _COMPILER_LOCK as LOCK
        with LOCK:
            compiler_output = compiler.compile(path)
            main_symbol_table: dict[str, ISymbol] = self.get_compiler_analyser(compiler).symbol_table

        self.assertEqual(expected_compiler_output, compiler_output)

        # the variable is local to a method, so it shouldn't be in the main symbol table
        self.assertFalse(test_variable_id in main_symbol_table)

        self.assertTrue(test_method_id in main_symbol_table)
        self.assertIsInstance(main_symbol_table[test_method_id], Method)
        method: Method = main_symbol_table[test_method_id]

        method_symbol_table: dict[str, Variable] = method.symbols
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

        output, _ = self.assertCompile('AssignmentWithType.py')
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

        output, _ = self.assertCompile('AssignmentWithoutType.py')
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

        output, _ = self.assertCompile('ArgumentAssignment.py')
        self.assertEqual(expected_output, output)

    def test_multiple_assignments(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSHT      # a = b = c = True
            + Opcode.DUP            # c = True
            + Opcode.STLOC2
            + Opcode.DUP            # b = True
            + Opcode.STLOC1
            + Opcode.STLOC0         # a = True
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('MultipleAssignments.py')
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

        output, _ = self.assertCompile('MultipleAssignmentsSetSequence.py')
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

        output, _ = self.assertCompile('MultipleAssignmentsSetSequenceLast.py')
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
            + Opcode.PUSHT      # a = b = c = True
            + Opcode.DUP            # c = True
            + Opcode.STLOC0
            + Opcode.DUP            # b = True
            + Opcode.STLOC2
            + Opcode.STLOC1         # a = True
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('MismatchedTypeMultipleAssignments.py')
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

        output, _ = self.assertCompile('ManyAssignments.py')
        self.assertEqual(expected_output, output)

    def test_return_arg_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # variable address
            + Opcode.RET
        )

        output, _ = self.assertCompile('ReturnArgument.py')
        self.assertEqual(expected_output, output)

    async def test_return_arg_value(self):
        await self.set_up_contract('ReturnArgument.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)
        result, _ = await self.call('Main', [-140], return_type=int)
        self.assertEqual(-140, result)

    def test_return_local_var_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH1
            + Opcode.STLOC0
            + Opcode.PUSH1      # variable address
            + Opcode.RET
        )

        output, _ = self.assertCompile('ReturnLocalVariable.py')
        self.assertEqual(expected_output, output)

    async def test_return_local_var_value(self):
        await self.set_up_contract('ReturnLocalVariable.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(1, result)
        result, _ = await self.call('Main', [-140], return_type=int)
        self.assertEqual(1, result)

    def test_assign_local_with_arg_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0     # variable address
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssignLocalWithArgument.py')
        self.assertEqual(expected_output, output)

    async def test_assign_local_with_arg_value(self):
        await self.set_up_contract('AssignLocalWithArgument.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)
        result, _ = await self.call('Main', [-140], return_type=int)
        self.assertEqual(-140, result)

    def test_using_undeclared_variable(self):
        path = self.get_contract_path('UsingUndeclaredVariable.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_return_undeclared_variable(self):
        path = self.get_contract_path('ReturnUndeclaredVariable.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_assign_value_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeAssignValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_assign_binary_operation_mismatched_type(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3  # a = 1 + 2
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeAssignBinOp.py')
        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_assign_unary_operation_mismatched_type(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH5  # a = -5
            + Opcode.NEGATE
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeAssignUnOp.py')
        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_assign_mixed_operations_mismatched_type(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x03'
            + Opcode.LDARG1  # b = min <= a - 2 <= max
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
        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_assign_sequence_get_mismatched_type(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0  # b = a[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeAssignSequenceGet.py')
        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_assign_sequence_set_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeAssignSequenceSet.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_aug_assign_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeAugAssign.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_invalid_type_format_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeInvalidTypeFormat.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_global_declaration_with_assignment_compile(self):
        expected_output = (
            Opcode.LDSFLD0
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH10
            + Opcode.STSFLD0    # a = 10
            + Opcode.RET
        )
        output, _ = self.assertCompile('GlobalDeclarationWithArgumentWrittenAfter.py')
        self.assertEqual(expected_output, output)

    async def test_global_declaration_with_assignment(self):
        await self.set_up_contract('GlobalDeclarationWithArgumentWrittenAfter.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(10, result)

    def test_global_declaration_without_assignment(self):
        path = self.get_contract_path('GlobalDeclarationWithoutAssignment.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_global_assignment_with_type_compile(self):
        expected_output = (
            Opcode.PUSH10
            + Opcode.RET
        )

        output, _ = self.assertCompile('GlobalAssignmentWithType.py')
        self.assertEqual(expected_output, output)

    def test_global_assignment_with_type_compile_no_optimization(self):
        expected_output = (
            Opcode.LDSFLD0
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH10
            + Opcode.STSFLD0    # a = 10
            + Opcode.RET
        )

        output, _ = self.assertCompile('GlobalAssignmentWithType.py', optimize=False)
        self.assertEqual(expected_output, output)

    async def test_global_assignment_with_type(self):
        await self.set_up_contract('GlobalAssignmentWithType.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(10, result)

    def test_global_assignment_without_type_compile(self):
        expected_output = (
            Opcode.PUSH10
            + Opcode.RET
        )

        output, _ = self.assertCompile('GlobalAssignmentWithoutType.py')
        self.assertEqual(expected_output, output)

    def test_global_assignment_without_type_compile_no_optimization(self):
        expected_output = (
            Opcode.LDSFLD0
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH10
            + Opcode.STSFLD0    # a = 10
            + Opcode.RET
        )

        output, _ = self.assertCompile('GlobalAssignmentWithoutType.py', optimize=False)
        self.assertEqual(expected_output, output)

    async def test_global_assignment_without_type(self):
        await self.set_up_contract('GlobalAssignmentWithoutType.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(10, result)

    def test_global_tuple_multiple_assignments(self):
        path = self.get_contract_path('GlobalAssignmentWithTuples.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    async def test_global_chained_multiple_assignments(self):
        await self.set_up_contract('GlobalMultipleAssignments.py', compile_if_found=True)

        result, _ = await self.call('get_a', [], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('get_c', [], return_type=int)
        self.assertEqual(15, result)

        result, _ = await self.call('set_a', [100], return_type=None)
        self.assertEqual(None, result)

        result, _ = await self.call('get_a', [], return_type=int)
        self.assertEqual(100, result)

    def test_many_global_assignments_compile(self):
        expected_output = (
            Opcode.PUSH7
            + Opcode.PUSH6
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH8
            + Opcode.PACK       # return [a, b, c, d, e, f, g, h]
            + Opcode.RET
        )

        output, _ = self.assertCompile('ManyGlobalAssignments.py')
        self.assertEqual(expected_output, output)

    def test_many_global_assignments_compile_no_optimization(self):
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
        output, _ = self.assertCompile('ManyGlobalAssignments.py', optimize=False)
        self.assertEqual(expected_output, output)

    async def test_many_global_assignments(self):
        await self.set_up_contract('ManyGlobalAssignments.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7], result)

    async def test_list_global_assignment(self):
        await self.set_up_contract('ListGlobalAssignment.py')

        expected_value = [1, 2, 3, 4]
        result, _ = await self.call('get_from_global', [], return_type=list)
        self.assertEqual(expected_value, result)

        result, _ = await self.call('get_from_class', [], return_type=list)
        self.assertEqual(expected_value, result)

        result, _ = await self.call('get_from_class_without_assigning', [], return_type=list)
        self.assertEqual([], result)

    def test_global_assignment_between_functions_compile(self):
        expected_output = (
            Opcode.PUSH10
            + Opcode.RET
            + Opcode.PUSH5
            + Opcode.RET
        )

        output, _ = self.assertCompile('GlobalAssignmentBetweenFunctions.py')
        self.assertEqual(expected_output, output)

    def test_global_assignment_between_functions_compile_no_optimization(self):
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

        output, _ = self.assertCompile('GlobalAssignmentBetweenFunctions.py', optimize=False)
        self.assertEqual(expected_output, output)

    async def test_global_assignment_between_functions(self):
        await self.set_up_contract('GlobalAssignmentBetweenFunctions.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(10, result)
        result, _ = await self.call('example', [], return_type=int)
        self.assertEqual(5, result)

    async def test_global_variable_in_class_method(self):
        await self.set_up_contract('GlobalVariableInClassMethod.py', compile_if_found=True)

        result, _ = await self.call('use_variable_in_func', [], return_type=int)
        self.assertEqual(42, result)

        result, _ = await self.call('use_variable_in_map', [], return_type=dict[str, int])
        self.assertEqual({'val1': 1, 'val2': 2, 'bar': 42}, result)

    async def test_global_variable_same_id_different_scopes(self):
        await self.set_up_contract('GetGlobalSameIdFromImport.py')

        result, _ = await self.call('value_from_script', [], return_type=int)
        self.assertEqual(42, result)

        result, _ = await self.call('value_from_import', [], return_type=list)
        self.assertEqual([1, 2, 3, 4], result)

    def test_get_global_variable_value_written_after_compile(self):
        expected_output = (
            Opcode.PUSH7
            + Opcode.PUSH6    # [a, b, c, d, e, f, g, h]
            + Opcode.PUSH5
            + Opcode.PUSH4
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH0
            + Opcode.PUSH8
            + Opcode.PACK       # return [a, b, c, d, e, f, g, h]
            + Opcode.RET
        )

        output, _ = self.assertCompile('GetGlobalValueWrittenAfter.py')
        self.assertEqual(expected_output, output)

    def test_get_global_variable_value_written_after_compile_no_optimization(self):
        expected_output_no_optimization = (
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

        output, _ = self.assertCompile('GetGlobalValueWrittenAfter.py', optimize=False)
        self.assertEqual(expected_output_no_optimization, output)

    async def test_get_global_variable_value_written_after(self):
        await self.set_up_contract('GetGlobalValueWrittenAfter.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7], result)

    def test_assign_local_shadowing_global_with_arg_value_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # b = a  // this b is not the global b
            + Opcode.STLOC0
            + Opcode.LDLOC0     # variable address
            + Opcode.RET
        )

        path = self.get_contract_path('AssignLocalWithArgumentShadowingGlobal.py')
        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_assign_local_shadowing_global_with_arg_value_compile_no_optimization(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0  # b = a  // this b is not the global b
            + Opcode.STLOC0
            + Opcode.LDLOC0  # variable address
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH0      # b = 0
            + Opcode.STSFLD0
            + Opcode.RET
        )

        output, _ = self.assertCompile('AssignLocalWithArgumentShadowingGlobal.py', optimize=False)
        self.assertEqual(expected_output, output)

    async def test_assign_local_shadowing_global_with_arg_value(self):
        await self.set_up_contract('AssignLocalWithArgumentShadowingGlobal.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)
        result, _ = await self.call('Main', [-140], return_type=int)
        self.assertEqual(-140, result)

    async def test_assign_global_in_function_with_global_keyword(self):
        await self.set_up_contract('GlobalAssignmentInFunctionWithArgument.py')

        result, _ = await self.call('get_b', [], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('get_b', [], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('Main', [-140], return_type=int)
        self.assertEqual(-140, result)

        result, _ = await self.call('get_b', [], return_type=int)
        self.assertEqual(-140, result)

    def test_assign_void_function_call_compile(self):
        output, _ = self.assertCompile('AssignVoidFunctionCall.py')
        self.assertIn(Opcode.NOP, output)

    async def test_assign_void_function_call(self):
        await self.set_up_contract('AssignVoidFunctionCall.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertEqual(None, result)

    async def test_anonymous_variable(self):
        await self.set_up_contract('AnonymousVariable')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(400, result)

    def test_assign_starred_variable(self):
        path = self.get_contract_path('AssignStarredVariable.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    async def test_variables_in_different_scope_with_same_name(self):
        await self.set_up_contract('DifferentScopesWithSameName.py')

        result, _ = await self.call('test', [], return_type=int)
        self.assertEqual(1_000, result)

    async def test_instance_variable_and_variable_with_same_name(self):
        await self.set_up_contract('InstanceVariableAndVariableWithSameName.py')

        result, _ = await self.call('test', [], return_type=list)
        self.assertEqual([10], result)

    async def test_inner_object_variable_access(self):
        await self.set_up_contract('InnerObjectVariableAccess.py')

        expected_return = 'InnerObjectVariableAccess'
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_return, result)

    async def test_variables_with_same_name_class_variable_and_local(self):
        await self.set_up_contract('VariablesWithSameNameClassVariableAndLocal.py')

        expected_return = 'example'
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_return, result)

    async def test_variables_with_same_name_instance_and_local(self):
        await self.set_up_contract('VariablesWithSameNameInstanceAndLocal.py')

        expected_return = 'example'
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_return, result)

    async def test_variables_with_same_name(self):
        await self.set_up_contract('VariablesWithSameName.py')

        expected_return = 'example'
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_return, result)

    def test_del_variable(self):
        path = self.get_contract_path('DelVariable.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_assign_function(self):
        path = self.get_contract_path('AssignFunction.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    async def test_elvis_operator_any_param(self):
        await self.set_up_contract('ElvisOperatorAnyParam.py')

        result, _ = await self.call('main', ['not empty string'], return_type=str)
        self.assertEqual('not empty string', result)

        result, _ = await self.call('main', [123456], return_type=int)
        self.assertEqual(123456, result)

        result, _ = await self.call('main', [True], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [None], return_type=str)
        self.assertEqual('some default value', result)
        result, _ = await self.call('main', [''], return_type=str)
        self.assertEqual('some default value', result)
        result, _ = await self.call('main', [0], return_type=str)
        self.assertEqual('some default value', result)
        result, _ = await self.call('main', [False], return_type=str)
        self.assertEqual('some default value', result)

    async def test_elvis_operator_bytes_param(self):
        await self.set_up_contract('ElvisOperatorBytesParam.py')

        result, _ = await self.call('main', [b'not empty string'], return_type=bytes)
        self.assertEqual(b'not empty string', result)

        result, _ = await self.call('main', [b''], return_type=bytes)
        self.assertEqual(b'some default value', result)

    async def test_elvis_operator_str_param(self):
        await self.set_up_contract('ElvisOperatorStrParam.py')

        result, _ = await self.call('main', ['not empty string'], return_type=str)
        self.assertEqual('not empty string', result)

        result, _ = await self.call('main', [''], return_type=str)
        self.assertEqual('some default value', result)

    async def test_elvis_operator_int_param(self):
        await self.set_up_contract('ElvisOperatorIntParam.py')

        result, _ = await self.call('main', [100], return_type=int)
        self.assertEqual(100, result)

        result, _ = await self.call('main', [0], return_type=int)
        self.assertEqual(123456, result)

    async def test_elvis_operator_bool_param(self):
        await self.set_up_contract('ElvisOperatorBoolParam.py')

        result, _ = await self.call('main', [True], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [False], return_type=bool)
        self.assertEqual(True, result)

    async def test_elvis_operator_optional_param(self):
        await self.set_up_contract('ElvisOperatorOptionalParam.py')

        result, _ = await self.call('main', ['unit test'], return_type=str)
        self.assertEqual('unit test', result)

        result, _ = await self.call('main', [''], return_type=str)
        self.assertEqual('some default value', result)
        result, _ = await self.call('main', [None], return_type=str)
        self.assertEqual('some default value', result)
