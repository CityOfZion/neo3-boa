from typing import Dict

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.compiler.compiler import Compiler
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


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

        from boa3_test.tests.boa_test import _COMPILER_LOCK as LOCK
        with LOCK:
            compiler_output = compiler.compile(path)
            main_symbol_table: Dict[str, ISymbol] = self.get_compiler_analyser(compiler).symbol_table

        self.assertEqual(expected_compiler_output, compiler_output)

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
        output = self.compile(path)
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
        output = self.compile(path)
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
        output = self.compile(path)
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

        path = self.get_contract_path('MultipleAssignments.py')
        output = self.compile(path)
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
        output = self.compile(path)
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
        output = self.compile(path)
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

        path = self.get_contract_path('MismatchedTypeMultipleAssignments.py')
        output = self.compile(path)
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
        output = self.compile(path)
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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'Main', -140))
        expected_results.append(-140)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(1)
        invokes.append(runner.call_contract(path, 'Main', -140))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'Main', -140))
        expected_results.append(-140)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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
            + Opcode.PUSHDATA1  # a = '1'
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
            + Opcode.PUSH3  # a = 1 + 2
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
            + Opcode.PUSH5  # a = -5
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
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
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
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_global_declaration_without_assignment(self):
        path = self.get_contract_path('GlobalDeclarationWithoutAssignment.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_global_assignment_with_type(self):
        expected_output = (
            Opcode.PUSH10
            + Opcode.RET
        )
        expected_output_no_optimization = (
            Opcode.LDSFLD0
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH10
            + Opcode.STSFLD0    # a = 10
            + Opcode.RET
        )
        path = self.get_contract_path('GlobalAssignmentWithType.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        output = self.compile(path, optimize=False)
        self.assertEqual(expected_output_no_optimization, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_global_assignment_without_type(self):
        expected_output = (
            Opcode.PUSH10
            + Opcode.RET
        )
        expected_output_no_optimization = (
            Opcode.LDSFLD0
            + Opcode.RET
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH10
            + Opcode.STSFLD0    # a = 10
            + Opcode.RET
        )
        path = self.get_contract_path('GlobalAssignmentWithoutType.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        output = self.compile(path, optimize=False)
        self.assertEqual(expected_output_no_optimization, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_global_tuple_multiple_assignments(self):
        path = self.get_contract_path('GlobalAssignmentWithTuples.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_global_chained_multiple_assignments(self):
        path, _ = self.get_deploy_file_paths('GlobalMultipleAssignments.py', compile_if_found=True)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_a'))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'get_c'))
        expected_results.append(15)

        invokes.append(runner.call_contract(path, 'set_a', 100))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'get_a'))
        expected_results.append(100)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_many_global_assignments(self):
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

        path = self.get_contract_path('ManyGlobalAssignments.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        output = self.compile(path, optimize=False)
        self.assertEqual(expected_output_no_optimization, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1, 2, 3, 4, 5, 6, 7])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_global_assignment(self):
        path, _ = self.get_deploy_file_paths('ListGlobalAssignment.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_value = [1, 2, 3, 4]
        invokes.append(runner.call_contract(path, 'get_from_global'))
        expected_results.append(expected_value)

        invokes.append(runner.call_contract(path, 'get_from_class'))
        expected_results.append(expected_value)

        invokes.append(runner.call_contract(path, 'get_from_class_without_assigning'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_global_assignment_between_functions(self):
        expected_output = (
            Opcode.PUSH10
            + Opcode.RET
            + Opcode.PUSH5
            + Opcode.RET
        )
        expected_output_no_optimization = (
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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        output = self.compile(path, optimize=False)
        self.assertEqual(expected_output_no_optimization, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'example'))
        expected_results.append(5)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_global_variable_in_class_method(self):
        path, _ = self.get_deploy_file_paths('GlobalVariableInClassMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'use_variable_in_func'))
        expected_results.append(42)

        invokes.append(runner.call_contract(path, 'use_variable_in_map'))
        expected_results.append({'val1': 1, 'val2': 2, 'bar': 42})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_global_variable_same_id_different_scopes(self):
        path, _ = self.get_deploy_file_paths('GetGlobalSameIdFromImport.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'value_from_script'))
        expected_results.append(42)

        invokes.append(runner.call_contract(path, 'value_from_import'))
        expected_results.append([1, 2, 3, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_global_variable_value_written_after(self):
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
        path = self.get_contract_path('GetGlobalValueWrittenAfter.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        output = self.compile(path, optimize=False)
        self.assertEqual(expected_output_no_optimization, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([0, 1, 2, 3, 4, 5, 6, 7])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_assign_local_shadowing_global_with_arg_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # b = a  // this b is not the global b
            + Opcode.STLOC0
            + Opcode.LDLOC0     # variable address
            + Opcode.RET
        )
        expected_output_no_optimization = (
            expected_output
            + Opcode.INITSSLOT  # global variables
            + b'\x01'           # number of globals
            + Opcode.PUSH0      # b = 0
            + Opcode.STSFLD0
            + Opcode.RET
        )
        path = self.get_contract_path('AssignLocalWithArgumentShadowingGlobal.py')
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

        output = self.compile(path, optimize=False)
        self.assertEqual(expected_output_no_optimization, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(10)
        invokes.append(runner.call_contract(path, 'Main', -140))
        expected_results.append(-140)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_assign_global_in_function_with_global_keyword(self):
        path, _ = self.get_deploy_file_paths('GlobalAssignmentInFunctionWithArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_b'))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'get_b'))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'Main', -140))
        expected_results.append(-140)

        invokes.append(runner.call_contract(path, 'get_b'))
        expected_results.append(-140)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_assign_void_function_call(self):
        path = self.get_contract_path('AssignVoidFunctionCall.py')
        output = self.compile(path)
        self.assertIn(Opcode.NOP, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_anonymous_variable(self):
        path, _ = self.get_deploy_file_paths('AnonymousVariable')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(400)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_assign_starred_variable(self):
        path = self.get_contract_path('AssignStarredVariable.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_variables_in_different_scope_with_same_name(self):
        path, _ = self.get_deploy_file_paths('DifferentScopesWithSameName.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'test'))
        expected_results.append(1_000)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_instance_variable_and_variable_with_same_name(self):
        path, _ = self.get_deploy_file_paths('InstanceVariableAndVariableWithSameName.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'test'))
        expected_results.append([10])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_inner_object_variable_access(self):
        path, _ = self.get_deploy_file_paths('InnerObjectVariableAccess.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_return = 'InnerObjectVariableAccess'
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_return)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_variables_with_same_name_class_variable_and_local(self):
        path, _ = self.get_deploy_file_paths('VariablesWithSameNameClassVariableAndLocal.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_return = 'example'
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_return)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_variables_with_same_name_instance_and_local(self):
        path, _ = self.get_deploy_file_paths('VariablesWithSameNameInstanceAndLocal.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_return = 'example'
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_return)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_variables_with_same_name(self):
        path, _ = self.get_deploy_file_paths('VariablesWithSameName.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_return = 'example'
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_return)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_del_variable(self):
        path = self.get_contract_path('DelVariable.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_assign_function(self):
        path = self.get_contract_path('AssignFunction.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_elvis_operator_any_param(self):
        path, _ = self.get_deploy_file_paths('ElvisOperatorAnyParam.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'not empty string'))
        expected_results.append('not empty string')

        invokes.append(runner.call_contract(path, 'main', 123456))
        expected_results.append(123456)

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', None))
        expected_results.append('some default value')
        invokes.append(runner.call_contract(path, 'main', ''))
        expected_results.append('some default value')
        invokes.append(runner.call_contract(path, 'main', 0))
        expected_results.append('some default value')
        invokes.append(runner.call_contract(path, 'main', False))
        expected_results.append('some default value')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_elvis_operator_bytes_param(self):
        path, _ = self.get_deploy_file_paths('ElvisOperatorBytesParam.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', b'not empty string', expected_result_type=bytes))
        expected_results.append(b'not empty string')

        invokes.append(runner.call_contract(path, 'main', b'', expected_result_type=bytes))
        expected_results.append(b'some default value')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_elvis_operator_str_param(self):
        path, _ = self.get_deploy_file_paths('ElvisOperatorStrParam.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'not empty string'))
        expected_results.append('not empty string')

        invokes.append(runner.call_contract(path, 'main', ''))
        expected_results.append('some default value')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_elvis_operator_int_param(self):
        path, _ = self.get_deploy_file_paths('ElvisOperatorIntParam.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 100))
        expected_results.append(100)

        invokes.append(runner.call_contract(path, 'main', 0))
        expected_results.append(123456)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_elvis_operator_bool_param(self):
        path, _ = self.get_deploy_file_paths('ElvisOperatorBoolParam.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', True))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', False))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_elvis_operator_optional_param(self):
        path, _ = self.get_deploy_file_paths('ElvisOperatorOptionalParam.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'unit test'))
        expected_results.append('unit test')

        invokes.append(runner.call_contract(path, 'main', ''))
        expected_results.append('some default value')
        invokes.append(runner.call_contract(path, 'main', None))
        expected_results.append('some default value')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
