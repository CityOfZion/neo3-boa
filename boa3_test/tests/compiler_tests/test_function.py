from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestFunction(BoaTest):
    default_folder: str = 'test_sc/function_test'

    def test_integer_function(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x00'  # num local variables
            + b'\x01'  # num arguments
            + Opcode.PUSH10  # body
            + Opcode.RET  # return
        )

        path = self.get_contract_path('IntegerFunction.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'Main', -1))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_function(self):
        expected_output = (
            # functions without arguments and local variables don't need initslot
            Opcode.PUSHDATA1  # body
            + bytes([len('42')])
            + bytes('42', constants.ENCODING)
            + Opcode.RET  # return
        )

        path = self.get_contract_path('StringFunction.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append('42')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_function(self):
        expected_output = (
            # functions without arguments and local variables don't need initslot
            Opcode.PUSHT  # body
            + Opcode.RET  # return
        )

        path = self.get_contract_path('BoolFunction.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_none_function_pass(self):
        path = self.get_contract_path('NoneFunctionPass.py')
        output = self.compile(path)
        self.assertIn(Opcode.NOP, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_none_function_return_none(self):
        path, _ = self.get_deploy_file_paths('NoneFunctionReturnNone.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_none_function_changing_values_with_return(self):
        path, _ = self.get_deploy_file_paths('NoneFunctionChangingValuesWithReturn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append([2, 4, 6, 8, 10])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_none_function_changing_values_without_return(self):
        path, _ = self.get_deploy_file_paths('NoneFunctionChangingValuesWithoutReturn.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append([2, 4, 6, 8, 10])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_arg_without_type_hint(self):
        path = self.get_contract_path('ArgWithoutTypeHintFunction.py')
        self.assertCompilerLogs(CompilerError.TypeHintMissing, path)

    def test_no_return_hint_function_with_empty_return_statement(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x00'  # num local variables
            + b'\x01'  # num arguments
            + Opcode.RET  # return
        )

        path = self.get_contract_path('EmptyReturnFunction.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_no_return_hint_function_with_condition_empty_return_statement(self):
        path, _ = self.get_deploy_file_paths('ConditionEmptyReturnFunction.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', 50))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_empty_return_with_optional_return_type(self):
        path, _ = self.get_deploy_file_paths('EmptyReturnWithOptionalReturnType.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', 50))
        expected_results.append(25)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_no_return_hint_function_without_return_statement(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x00'  # num local variables
            + b'\x01'  # num arguments
            + Opcode.NOP  # pass
            + Opcode.RET  # return
        )

        path = self.get_contract_path('NoReturnFunction.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_return_type_hint_function_with_empty_return(self):
        path = self.get_contract_path('ExpectingReturnFunction.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_multiple_return_function(self):
        path = self.get_contract_path('MultipleReturnFunction.py')
        self.assertCompilerLogs(CompilerError.TooManyReturns, path)

    def test_tuple_function(self):
        path = self.get_contract_path('TupleFunction.py')
        self.assertCompilerLogs(CompilerError.TooManyReturns, path)

    def test_default_return(self):
        path = self.get_contract_path('DefaultReturn.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

    def test_empty_list_return(self):
        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET
        )

        path = self.get_contract_path('EmptyListReturn.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_mismatched_return_type(self):
        path = self.get_contract_path('MismatchedReturnType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_mismatched_return_type_with_if(self):
        path = self.get_contract_path('MismatchedReturnTypeWithIf.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_call_void_function_without_args(self):
        called_function_address = Integer(4).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.CALL  # TestFunction()
            + called_function_address
            + Opcode.PUSHT  # return True
            + Opcode.RET
            + Opcode.INITSLOT  # TestFunction
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1  # a = 1
            + Opcode.STLOC0
            + Opcode.RET  # return
        )

        path = self.get_contract_path('CallVoidFunctionWithoutArgs.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_without_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x01'
            + b'\x00'
            + Opcode.CALL  # a = TestFunction()
            + called_function_address
            + Opcode.STLOC0
            + Opcode.LDLOC0  # return a
            + Opcode.RET
            + Opcode.PUSH1  # TestFunction
            + Opcode.RET  # return 1
        )

        path = self.get_contract_path('CallReturnFunctionWithoutArgs.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_void_function_with_literal_args(self):
        called_function_address = Integer(4).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.PUSH2  # TestAdd(1, 2)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.PUSHT  # return True
            + Opcode.RET
            + Opcode.INITSLOT  # TestFunction
            + b'\x01'
            + b'\x02'
            + Opcode.LDARG0  # c = a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.RET  # return
        )

        path = self.get_contract_path('CallVoidFunctionWithLiteralArgs.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_with_literal_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH2  # a = TestAdd(1, 2)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.STLOC0
            + Opcode.LDLOC0  # return a
            + Opcode.RET
            + Opcode.INITSLOT  # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0  # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET  # return
        )

        path = self.get_contract_path('CallReturnFunctionWithLiteralArgs.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_void_function_with_variable_args(self):
        called_function_address = Integer(4).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH1  # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2  # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH2  # TestAdd(a, b)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.PUSHT  # return True
            + Opcode.RET
            + Opcode.INITSLOT  # TestFunction
            + b'\x01'
            + b'\x02'
            + Opcode.LDARG0  # c = a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.RET  # return
        )

        path = self.get_contract_path('CallVoidFunctionWithVariableArgs.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_with_variable_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x03'
            + b'\x02'
            + Opcode.PUSH1  # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2  # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH2  # c = TestAdd(a, b)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.STLOC2
            + Opcode.LDLOC2  # return c
            + Opcode.RET
            + Opcode.INITSLOT  # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0  # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET  # return
        )

        path = self.get_contract_path('CallReturnFunctionWithVariableArgs.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'TestAdd', 1, 2))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_on_return(self):
        called_function_address = Integer(3).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH1  # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2  # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH2  # return TestAdd(a, b)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.RET
            + Opcode.INITSLOT  # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0  # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET  # return
        )

        path = self.get_contract_path('CallReturnFunctionOnReturn.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_without_variables(self):
        main_to_one_address = Integer(-10).to_byte_array(min_length=1, signed=True)
        main_to_two_address = Integer(5).to_byte_array(min_length=1, signed=True)
        two_to_one_address = Integer(-24).to_byte_array(min_length=1, signed=True)
        end_if = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.PUSH1  # One
            + Opcode.RET  # return 1
            + Opcode.INITSLOT  # Main
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0  # if arg0 == 1
            + Opcode.PUSH1
            + Opcode.NUMEQUAL
            + Opcode.JMPIFNOT
            + end_if
            + Opcode.CALL  # return One()
            + main_to_one_address
            + Opcode.RET
            + Opcode.LDARG0  # elif arg0 == 2
            + Opcode.PUSH2
            + Opcode.NUMEQUAL
            + Opcode.JMPIFNOT
            + end_if
            + Opcode.CALL  # return Two()
            + main_to_two_address
            + Opcode.RET
            + Opcode.PUSH0  # default return
            + Opcode.RET
            + Opcode.PUSH1  # Two
            + Opcode.CALL  # return 1 + One()
            + two_to_one_address
            + Opcode.ADD
            + Opcode.RET
        )

        path = self.get_contract_path('CallFunctionWithoutVariables.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 1))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'Main', 2))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'Main', 3))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_written_before_caller(self):
        call_address = Integer(-9).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT  # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0  # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET
            + Opcode.PUSH2  # return TestAdd(a, b)
            + Opcode.PUSH1
            + Opcode.CALL
            + call_address
            + Opcode.RET
        )

        path = self.get_contract_path('CallFunctionWrittenBefore.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_return_void_function(self):
        called_function_address = Integer(4).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.CALL  # Main
            + called_function_address  # return TestFunction()
            + Opcode.PUSHNULL
            + Opcode.RET
            + Opcode.INITSLOT  # TestFunction
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1  # a = 1
            + Opcode.STLOC0
            + Opcode.RET  # return
        )

        path = self.get_contract_path('ReturnVoidFunction.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

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

    def test_return_void_function_mismatched_type(self):
        path = self.get_contract_path('ReturnVoidFunctionMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_return_inside_if(self):
        path, _ = self.get_deploy_file_paths('ReturnIf.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 4))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(6)

        invokes.append(runner.call_contract(path, 'Main', 6))
        expected_results.append(6)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_missing_return_inside_if(self):
        path = self.get_contract_path('ReturnIfMissing.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

    def test_missing_return_inside_elif(self):
        path = self.get_contract_path('ReturnElifMissing.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

    def test_missing_return_inside_else(self):
        path = self.get_contract_path('ReturnElseMissing.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

    def test_return_inside_multiple_inner_if(self):
        path, _ = self.get_deploy_file_paths('ReturnMultipleInnerIf.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(9)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_missing_return_inside_multiple_inner_if(self):
        path = self.get_contract_path('ReturnMultipleInnerIfMissing.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

    def test_return_if_expression(self):
        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0  # return 5 if condition else 10
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH5  # 5
            + Opcode.JMP  # else
            + Integer(3).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH10  # 10
            + Opcode.RET  # return
        )

        path = self.get_contract_path('ReturnIfExpression.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', True))
        expected_results.append(5)

        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_return_if_expression_mismatched_type(self):
        path = self.get_contract_path('ReturnIfExpressionMismatched.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_return_inside_for(self):
        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0  # for_sequence = arg0
            + Opcode.PUSH0  # for_index = 0
            + Opcode.JMP  # begin for
            + Integer(19).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER  # value = for_sequence[for_index]
            + Opcode.OVER
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
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0  # return value
            + Opcode.RET
            + Opcode.INC  # for_index = for_index + 1
            + Opcode.DUP  # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-22).to_byte_array(min_length=1, signed=True)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.PUSH5  # else
            + Opcode.RET  # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('ReturnFor.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [1, 2, 3]))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'Main', (2, 5, 7)))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'Main', []))
        expected_results.append(5)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_missing_return_inside_for(self):
        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x02'
            + b'\x01'
            + Opcode.PUSH0  # x = 0
            + Opcode.STLOC0
            + Opcode.LDARG0  # for_sequence = arg0
            + Opcode.PUSH0  # for_index = 0
            + Opcode.JMP  # begin for
            + Integer(19).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER  # value = for_sequence[for_index]
            + Opcode.OVER
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.STLOC1
            + Opcode.LDLOC0  # x += value
            + Opcode.LDLOC1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.INC  # for_index = for_index + 1
            + Opcode.DUP  # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-22).to_byte_array(min_length=1, signed=True)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0  # else
            + Opcode.RET  # return x
            + Opcode.RET
        )

        path = self.get_contract_path('ReturnForOnlyOnElse.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', [1, 2, 3]))
        expected_results.append(6)

        invokes.append(runner.call_contract(path, 'Main', (2, 5, 7)))
        expected_results.append(14)

        invokes.append(runner.call_contract(path, 'Main', []))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_missing_return_inside_for_else(self):
        path = self.get_contract_path('ReturnForElseMissing.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

    def test_return_inside_while(self):
        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0  # x = arg0
            + Opcode.STLOC0
            + Opcode.JMP  # begin while
            + Integer(8).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0  # x += 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0  # return x
            + Opcode.RET
            + Opcode.LDLOC0
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIF  # end while x < 10
            + Integer(-9).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0  # else
            + Opcode.RET  # return x
            + Opcode.RET
        )

        path = self.get_contract_path('ReturnWhile.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(6)

        invokes.append(runner.call_contract(path, 'Main', 3))
        expected_results.append(4)

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'Main', 100))
        expected_results.append(100)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_missing_return_inside_while(self):
        expected_output = (
            Opcode.INITSLOT  # Main
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0  # x = arg0
            + Opcode.STLOC0
            + Opcode.JMP  # begin while
            + Integer(6).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0  # x += 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIF  # end while x < 10
            + Integer(-7).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0  # else
            + Opcode.RET  # return x
            + Opcode.RET
        )

        path = self.get_contract_path('ReturnWhileOnlyOnElse.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 5))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'Main', 3))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'Main', 100))
        expected_results.append(100)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_missing_return_inside_while_without_else(self):
        path = self.get_contract_path('ReturnWhileWithoutElse.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

    def test_multiple_function_large_call(self):
        path, _ = self.get_deploy_file_paths('MultipleFunctionLargeCall.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'calculate', [1]))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'main', 'calc', [1, 2, 3]))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'calculate', 1, [10, 3]))
        expected_results.append(13)

        invokes.append(runner.call_contract(path, 'main', 'calculate', [1, 10, 3]))
        expected_results.append(13)

        invokes.append(runner.call_contract(path, 'calculate', 2, [10, 3]))
        expected_results.append(7)

        invokes.append(runner.call_contract(path, 'main', 'calculate', [2, 10, 3]))
        expected_results.append(7)

        invokes.append(runner.call_contract(path, 'calculate', 3, [10, 3]))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', 'calculate', [3, 10, 3]))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'calculate', 4, [10, 3]))
        expected_results.append(30)

        invokes.append(runner.call_contract(path, 'main', 'calculate', [4, 10, 3]))
        expected_results.append(30)

        invokes.append(runner.call_contract(path, 'calculate', 5, [10, 3]))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'main', 'calculate', [5, 10, 3]))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_function_with_default_argument(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH3  # x = add(1, 2, 3)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.CALL
            + Integer(14).to_byte_array(signed=True, min_length=1)
            + Opcode.STLOC0
            + Opcode.PUSH0
            + Opcode.PUSH6  # y = add(5, 6)
            + Opcode.PUSH5
            + Opcode.CALL
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.LDLOC0
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.RET
            + Opcode.INITSLOT  # def add(a: int, b: int, c: int = 0)
            + b'\x00\x03'
            + Opcode.LDARG0  # return a + b + c
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.LDARG2
            + Opcode.ADD
            + Opcode.RET
        )

        path = self.get_contract_path('FunctionWithDefaultArgument.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([6, 11])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_function_with_only_default_arguments(self):
        expected_output = (
            Opcode.PUSH0  # defaults
            + Opcode.PUSH0
            + Opcode.PUSH0
            + Opcode.CALL  # add()
            + Integer(20).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH0  # defaults
            + Opcode.PUSH6  # add(5, 6)
            + Opcode.PUSH5
            + Opcode.CALL
            + Integer(15).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH0  # defaults
            + Opcode.PUSH0
            + Opcode.PUSH9  # add(9)
            + Opcode.CALL
            + Integer(10).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3  # add(1, 2, 3)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.CALL
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.RET
            + Opcode.INITSLOT  # def add(a: int, b: int, c: int)
            + b'\x00\x03'
            + Opcode.LDARG0  # return a + b + c
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.LDARG2
            + Opcode.ADD
            + Opcode.RET
        )

        path = self.get_contract_path('FunctionWithOnlyDefaultArguments.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([6, 9, 11, 0])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_function_with_default_argument_between_other_args(self):
        path = self.get_contract_path('FunctionWithDefaultArgumentBetweenArgs.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    def test_call_function_with_kwarg(self):
        path, _ = self.get_deploy_file_paths('CallFunctionWithKwarg.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(-10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_with_kwargs(self):
        path, _ = self.get_deploy_file_paths('CallFunctionWithKwargs.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'positional_order'))
        expected_results.append(1234)

        invokes.append(runner.call_contract(path, 'out_of_order'))
        expected_results.append(2413)

        invokes.append(runner.call_contract(path, 'mixed_in_order'))
        expected_results.append(5612)

        invokes.append(runner.call_contract(path, 'mixed_out_of_order'))
        expected_results.append(5621)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_with_kwargs_with_default_values(self):
        path, _ = self.get_deploy_file_paths('CallFunctionWithKwargsWithDefaultValues.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'positional_order'))
        expected_results.append(1234)

        invokes.append(runner.call_contract(path, 'out_of_order'))
        expected_results.append(2413)

        invokes.append(runner.call_contract(path, 'mixed_in_order'))
        expected_results.append(5612)

        invokes.append(runner.call_contract(path, 'mixed_out_of_order'))
        expected_results.append(5621)

        invokes.append(runner.call_contract(path, 'default_values'))
        expected_results.append(1034)

        invokes.append(runner.call_contract(path, 'only_default_values_and_kwargs'))
        expected_results.append(204)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_with_kwargs_only(self):
        path = self.get_contract_path('CallFunctionWithKwargsOnly.py')
        # TODO: change the test when creating a function that only accepts keywords is implemented #2ewewtz
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_call_function_with_kwargs_self(self):
        path = self.get_contract_path('CallFunctionWithKwargsSelf.py')
        # TODO: change the test when calling a function using the class is implemented #2ewewtz #2ewexau
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_call_function_with_kwargs_wrong_type(self):
        path = self.get_contract_path('CallFunctionWithKwargsWrongType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_call_function_with_kwargs_too_few_parameters(self):
        path = self.get_contract_path('CallFunctionWithKwargsTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_call_function_with_kwargs_too_many_parameters(self):
        path = self.get_contract_path('CallFunctionWithKwargsTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_call_function_with_kwargs_too_many_kw_parameters(self):
        path = self.get_contract_path('CallFunctionWithKwargsTooManyKwArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_boa2_fibonacci_test(self):
        path, _ = self.get_deploy_file_paths('FibonacciBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 4))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', 5))
        expected_results.append(5)

        invokes.append(runner.call_contract(path, 'main', 6))
        expected_results.append(8)

        invokes.append(runner.call_contract(path, 'main', 7))
        expected_results.append(13)

        invokes.append(runner.call_contract(path, 'main', 11))
        expected_results.append(89)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_method_test(self):
        path, _ = self.get_deploy_file_paths('MethodBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1, 2))
        expected_results.append(7)

        invokes.append(runner.call_contract(path, 'main', -3, -100))
        expected_results.append(-99)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_method_test2(self):
        path, _ = self.get_deploy_file_paths('MethodBoa2Test2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(26)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_method_test3(self):
        path, _ = self.get_deploy_file_paths('MethodBoa2Test3.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(13)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_method_test4(self):
        path, _ = self.get_deploy_file_paths('MethodBoa2Test4.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(63)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_method_test5(self):
        path, _ = self.get_deploy_file_paths('MethodBoa2Test5.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(15)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_module_method_test1(self):
        path, _ = self.get_deploy_file_paths('ModuleMethodBoa2Test1.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_module_method_test2(self):
        path, _ = self.get_deploy_file_paths('ModuleMethodBoa2Test2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(3003)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_module_variable_test(self):
        path, _ = self.get_deploy_file_paths('ModuleVariableBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(1260)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_module_variable_test1(self):
        path, _ = self.get_deploy_file_paths('ModuleVariableBoa2Test1.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(8)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_void_function_with_stared_argument(self):
        path, _ = self.get_deploy_file_paths('CallVoidFunctionWithStarredArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_return_function_with_stared_argument(self):
        path, _ = self.get_deploy_file_paths('CallReturnFunctionWithStarredArgument.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(sum([1, 2, 3, 4, 5, 6]))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_return_starred_argument(self):
        path, _ = self.get_deploy_file_paths('ReturnStarredArgumentCount.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'fun_with_starred', [1, 2, 3, 4, 5]))
        expected_results.append(5)

        invokes.append(runner.call_contract(path, 'fun_with_starred', [1, 2, 3]))
        expected_results.append(3)

        invokes.append(runner.call_contract(path, 'main', [1, 2, 3, 4, 5]))
        expected_results.append(5)

        invokes.append(runner.call_contract(path, 'main', [1, 2, 3]))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_function_with_same_name_in_different_scopes(self):
        path, _ = self.get_deploy_file_paths('CallFunctionsWithSameNameInDifferentScopes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'result'))
        expected_results.append([10, 20])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_function_with_dictionary_unpacking_operator(self):
        path = self.get_contract_path('FunctionWithDictionaryUnpackingOperator.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_functions_with_duplicated_name(self):
        path = self.get_contract_path('FunctionsWithDuplicatedName.py')
        self.assertCompilerLogs(CompilerError.DuplicatedIdentifier, path)

    def test_function_as_arg(self):
        path, _ = self.get_deploy_file_paths('FunctionAsArg.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 123))
        expected_results.append(123)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_function_with_arg_as_arg(self):
        path, _ = self.get_deploy_file_paths('FunctionWithArgAsArg.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_int = [123, 456, 789]
        value = 123
        invokes.append(runner.call_contract(path, 'main', list_int, value))
        expected_results.append(list_int.index(value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_function_with_args_as_arg(self):
        path, _ = self.get_deploy_file_paths('FunctionWithArgsAsArg.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_int = [123, 456, 789]
        value = 123
        start = 0
        end = 5
        invokes.append(runner.call_contract(path, 'main', list_int, value, start, end))
        expected_results.append(list_int.index(value, start, end))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_call_external_contract_with_return_none(self):
        path, _ = self.get_deploy_file_paths('CallExternalContractWithReturnNone.py')
        no_return_path, _ = self.get_deploy_file_paths('NoReturnFunction.py')

        runner = BoaTestRunner(runner_id=self.method_name())
        runner.deploy_contract(no_return_path)

        invoke = runner.call_contract(path, 'main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(invoke.result, None)

    def test_inner_function(self):
        path = self.get_contract_path('InnerFunction.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_lambda_function(self):
        path = self.get_contract_path('LambdaFunction.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_function_custom_decorator_with_global_function(self):
        path = self.get_contract_path('CustomDecoratorWithGlobalFunction.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_function_builtin_function_decorators_with_class(self):
        path = self.get_contract_path('BuiltinContractDecoratorWithFunction.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)
