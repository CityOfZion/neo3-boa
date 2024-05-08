from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3_test.tests import boatestcase


class TestFunction(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/function_test'

    def test_integer_function_compile(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x00'  # num local variables
            + b'\x01'  # num arguments
            + Opcode.PUSH10  # body
            + Opcode.RET  # return
        )

        output, _ = self.assertCompile('IntegerFunction.py')
        self.assertEqual(expected_output, output)

    async def test_integer_function_run(self):
        await self.set_up_contract('IntegerFunction.py')

        result, _ = await self.call('Main', [1], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('Main', [-1], return_type=int)
        self.assertEqual(10, result)

    def test_string_function_compile(self):
        expected_output = (
            # functions without arguments and local variables don't need initslot
            Opcode.PUSHDATA1  # body
            + bytes([len('42')])
            + bytes('42', constants.ENCODING)
            + Opcode.RET  # return
        )

        output, _ = self.assertCompile('StringFunction.py')
        self.assertEqual(expected_output, output)

    async def test_string_function_run(self):
        await self.set_up_contract('StringFunction.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('42', result)

    def test_bool_function_compile(self):
        expected_output = (
            # functions without arguments and local variables don't need initslot
            Opcode.PUSHT  # body
            + Opcode.RET  # return
        )

        output, _ = self.assertCompile('BoolFunction.py')
        self.assertEqual(expected_output, output)

    async def test_bool_function_run(self):
        await self.set_up_contract('BoolFunction.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    def test_none_function_pass_compile(self):
        output, _ = self.assertCompile('NoneFunctionPass.py')
        self.assertIn(Opcode.NOP, output)

    async def test_none_function_pass_run(self):
        await self.set_up_contract('NoneFunctionPass.py')

        result, _ = await self.call('main', [1], return_type=None)
        self.assertIsNone(result)

    async def test_none_function_return_none(self):
        await self.set_up_contract('NoneFunctionReturnNone.py')

        result, _ = await self.call('main', [], return_type=None)
        self.assertIsNone(result)

    async def test_none_function_changing_values_with_return(self):
        await self.set_up_contract('NoneFunctionChangingValuesWithReturn.py')

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual([2, 4, 6, 8, 10], result)

    async def test_none_function_changing_values_without_return(self):
        await self.set_up_contract('NoneFunctionChangingValuesWithoutReturn.py')

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual([2, 4, 6, 8, 10], result)

    def test_arg_without_type_hint(self):
        self.assertCompilerLogs(CompilerError.TypeHintMissing, 'ArgWithoutTypeHintFunction.py')

    def test_no_return_hint_function_with_empty_return_statement_compile(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x00'  # num local variables
            + b'\x01'  # num arguments
            + Opcode.RET  # return
        )

        output, _ = self.assertCompile('EmptyReturnFunction.py')
        self.assertEqual(expected_output, output)

    async def test_no_return_hint_function_with_empty_return_statement_run(self):
        await self.set_up_contract('EmptyReturnFunction.py')

        result, _ = await self.call('Main', [5], return_type=None)
        self.assertIsNone(result)

    async def test_no_return_hint_function_with_condition_empty_return_statement(self):
        await self.set_up_contract('ConditionEmptyReturnFunction.py')

        result, _ = await self.call('Main', [5], return_type=None)
        self.assertIsNone(result)

        result, _ = await self.call('Main', [50], return_type=None)
        self.assertIsNone(result)

    async def test_empty_return_with_optional_return_type(self):
        await self.set_up_contract('EmptyReturnWithOptionalReturnType.py')

        result, _ = await self.call('Main', [5], return_type=None)
        self.assertIsNone(result)

        result, _ = await self.call('Main', [50], return_type=int)
        self.assertEqual(25, result)

    def test_no_return_hint_function_without_return_statement_compile(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x00'  # num local variables
            + b'\x01'  # num arguments
            + Opcode.NOP  # pass
            + Opcode.RET  # return
        )

        output, _ = self.assertCompile('NoReturnFunction.py')
        self.assertEqual(expected_output, output)

    async def test_no_return_hint_function_without_return_statement_run(self):
        await self.set_up_contract('NoReturnFunction.py')

        result, _ = await self.call('Main', [5], return_type=None)
        self.assertIsNone(result)

    def test_return_type_hint_function_with_empty_return(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ExpectingReturnFunction.py')

    def test_multiple_return_function(self):
        self.assertCompilerLogs(CompilerError.TooManyReturns, 'MultipleReturnFunction.py')

    def test_tuple_function(self):
        self.assertCompilerLogs(CompilerError.TooManyReturns, 'TupleFunction.py')

    def test_default_return(self):
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, 'DefaultReturn.py')

    def test_empty_list_return_compile(self):
        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET
        )

        output, _ = self.assertCompile('EmptyListReturn.py')
        self.assertEqual(expected_output, output)

    async def test_empty_list_return_run(self):
        await self.set_up_contract('EmptyListReturn.py')

        result, _ = await self.call('Main', [], return_type=list)

    def test_mismatched_return_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MismatchedReturnType.py')

    def test_mismatched_return_type_with_if(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MismatchedReturnTypeWithIf.py')

    def test_call_void_function_without_args_compile(self):
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

        output, _ = self.assertCompile('CallVoidFunctionWithoutArgs.py')
        self.assertEqual(expected_output, output)

    async def test_call_void_function_without_args_run(self):
        await self.set_up_contract('CallVoidFunctionWithoutArgs.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    def test_call_function_without_args_compile(self):
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

        output, _ = self.assertCompile('CallReturnFunctionWithoutArgs.py')
        self.assertEqual(expected_output, output)

    async def test_call_function_without_args_run(self):
        await self.set_up_contract('CallReturnFunctionWithoutArgs.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(1, result)

    def test_call_void_function_with_literal_args_compile(self):
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

        output, _ = self.assertCompile('CallVoidFunctionWithLiteralArgs.py')
        self.assertEqual(expected_output, output)

    async def test_call_void_function_with_literal_args_run(self):
        await self.set_up_contract('CallVoidFunctionWithLiteralArgs.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    def test_call_function_with_literal_args_compile(self):
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

        output, _ = self.assertCompile('CallReturnFunctionWithLiteralArgs.py')
        self.assertEqual(expected_output, output)

    async def test_call_function_with_literal_args_run(self):
        await self.set_up_contract('CallReturnFunctionWithLiteralArgs.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(3, result)

    def test_call_void_function_with_variable_args_compile(self):
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

        output, _ = self.assertCompile('CallVoidFunctionWithVariableArgs.py')
        self.assertEqual(expected_output, output)

    async def test_call_void_function_with_variable_args_run(self):
        await self.set_up_contract('CallVoidFunctionWithVariableArgs.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    def test_call_function_with_variable_args_compile(self):
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

        output, _ = self.assertCompile('CallReturnFunctionWithVariableArgs.py')
        self.assertEqual(expected_output, output)

    async def test_call_function_with_variable_args_run(self):
        await self.set_up_contract('CallReturnFunctionWithVariableArgs.py')

        result, _ = await self.call('TestAdd', [1, 2], return_type=int)
        self.assertEqual(3, result)

    def test_call_function_on_return_compile(self):
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

        output, _ = self.assertCompile('CallReturnFunctionOnReturn.py')
        self.assertEqual(expected_output, output)

    async def test_call_function_on_return_run(self):
        await self.set_up_contract('CallReturnFunctionOnReturn.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(3, result)

    def test_call_function_without_variables_compile(self):
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

        output, _ = self.assertCompile('CallFunctionWithoutVariables.py')
        self.assertEqual(expected_output, output)

    async def test_call_function_without_variables_run(self):
        await self.set_up_contract('CallFunctionWithoutVariables.py')

        result, _ = await self.call('Main', [1], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('Main', [2], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('Main', [3], return_type=int)
        self.assertEqual(0, result)

    def test_call_function_written_before_caller_compile(self):
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

        output, _ = self.assertCompile('CallFunctionWrittenBefore.py')
        self.assertEqual(expected_output, output)

    async def test_call_function_written_before_caller_run(self):
        await self.set_up_contract('CallFunctionWrittenBefore.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(3, result)

    def test_return_void_function_compile(self):
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

        output, _ = self.assertCompile('ReturnVoidFunction.py')
        self.assertEqual(expected_output, output)

    async def test_return_void_function_run(self):
        await self.set_up_contract('ReturnVoidFunction.py')

        result, _ = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

    def test_return_void_function_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ReturnVoidFunctionMismatchedType.py')

    async def test_return_inside_if(self):
        await self.set_up_contract('ReturnIf.py')

        result, _ = await self.call('Main', [4], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('Main', [5], return_type=int)
        self.assertEqual(6, result)

        result, _ = await self.call('Main', [6], return_type=int)
        self.assertEqual(6, result)

    def test_missing_return_inside_if(self):
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, 'ReturnIfMissing.py')

    def test_missing_return_inside_elif(self):
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, 'ReturnElifMissing.py')

    def test_missing_return_inside_else(self):
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, 'ReturnElseMissing.py')

    async def test_return_inside_multiple_inner_if(self):
        await self.set_up_contract('ReturnMultipleInnerIf.py')

        result, _ = await self.call('Main', [True], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('Main', [False], return_type=int)
        self.assertEqual(9, result)

    def test_missing_return_inside_multiple_inner_if(self):
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, 'ReturnMultipleInnerIfMissing.py')

    def test_return_if_expression_compiler(self):
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

        output, _ = self.assertCompile('ReturnIfExpression.py')
        self.assertEqual(expected_output, output)

    async def test_return_if_expression_run(self):
        await self.set_up_contract('ReturnIfExpression.py')

        result, _ = await self.call('Main', [True], return_type=int)
        self.assertEqual(5, result)

        result, _ = await self.call('Main', [False], return_type=int)
        self.assertEqual(10, result)

    def test_return_if_expression_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ReturnIfExpressionMismatched.py')

    def test_return_inside_for_compile(self):
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

        output, _ = self.assertCompile('ReturnFor.py')
        self.assertEqual(expected_output, output)

    async def test_return_inside_for_run(self):
        await self.set_up_contract('ReturnFor.py')

        result, _ = await self.call('Main', [[1, 2, 3]], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('Main', [(2, 5, 7)], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('Main', [[]], return_type=int)
        self.assertEqual(5, result)

    def test_missing_return_inside_for_compile(self):
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

        output, _ = self.assertCompile('ReturnForOnlyOnElse.py')
        self.assertEqual(expected_output, output)

    async def test_missing_return_inside_for_run(self):
        await self.set_up_contract('ReturnForOnlyOnElse.py')

        result, _ = await self.call('Main', [[1, 2, 3]], return_type=int)
        self.assertEqual(6, result)

        result, _ = await self.call('Main', [(2, 5, 7)], return_type=int)
        self.assertEqual(14, result)

        result, _ = await self.call('Main', [[]], return_type=int)
        self.assertEqual(0, result)

    def test_missing_return_inside_for_else(self):
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, 'ReturnForElseMissing.py')

    def test_return_inside_while_compile(self):
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

        output, _ = self.assertCompile('ReturnWhile.py')
        self.assertEqual(expected_output, output)

    async def test_return_inside_while_run(self):
        await self.set_up_contract('ReturnWhile.py')

        result, _ = await self.call('Main', [5], return_type=int)
        self.assertEqual(6, result)

        result, _ = await self.call('Main', [3], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('Main', [100], return_type=int)
        self.assertEqual(100, result)

    def test_missing_return_inside_while_compile(self):
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

        output, _ = self.assertCompile('ReturnWhileOnlyOnElse.py')
        self.assertEqual(expected_output, output)

    async def test_missing_return_inside_while_run(self):
        await self.set_up_contract('ReturnWhileOnlyOnElse.py')

        result, _ = await self.call('Main', [5], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('Main', [3], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('Main', [100], return_type=int)
        self.assertEqual(100, result)

    def test_missing_return_inside_while_without_else(self):
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, 'ReturnWhileWithoutElse.py')

    async def test_multiple_function_large_call(self):
        await self.set_up_contract('MultipleFunctionLargeCall.py')

        result, _ = await self.call('main', ['calculate', [1]], return_type=None)
        self.assertIsNone(result)

        result, _ = await self.call('main', ['calc', [1, 2, 3]], return_type=None)
        self.assertIsNone(result)

        result, _ = await self.call('calculate', [1, [10, 3]], return_type=int)
        self.assertEqual(13, result)

        result, _ = await self.call('main', ['calculate', [1, 10, 3]], return_type=int)
        self.assertEqual(13, result)

        result, _ = await self.call('calculate', [2, [10, 3]], return_type=int)
        self.assertEqual(7, result)

        result, _ = await self.call('main', ['calculate', [2, 10, 3]], return_type=int)
        self.assertEqual(7, result)

        result, _ = await self.call('calculate', [3, [10, 3]], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', ['calculate', [3, 10, 3]], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('calculate', [4, [10, 3]], return_type=int)
        self.assertEqual(30, result)

        result, _ = await self.call('main', ['calculate', [4, 10, 3]], return_type=int)
        self.assertEqual(30, result)

        result, _ = await self.call('calculate', [5, [10, 3]], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('main', ['calculate', [5, 10, 3]], return_type=int)
        self.assertEqual(1, result)

    def test_function_with_default_argument_compile(self):
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

        output, _ = self.assertCompile('FunctionWithDefaultArgument.py')
        self.assertEqual(expected_output, output)

    async def test_function_with_default_argument_run(self):
        await self.set_up_contract('FunctionWithDefaultArgument.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([6, 11], result)

    def test_function_with_only_default_arguments_compile(self):
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

        output, _ = self.assertCompile('FunctionWithOnlyDefaultArguments.py')
        self.assertEqual(expected_output, output)

    async def test_function_with_only_default_arguments_run(self):
        await self.set_up_contract('FunctionWithOnlyDefaultArguments.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([6, 9, 11, 0], result)

    def test_function_with_default_argument_between_other_args(self):
        path = self.get_contract_path('FunctionWithDefaultArgumentBetweenArgs.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    async def test_call_function_with_kwarg(self):
        await self.set_up_contract('CallFunctionWithKwarg.py')

        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(-10, result)

    async def test_call_function_with_kwargs(self):
        await self.set_up_contract('CallFunctionWithKwargs.py')

        result, _ = await self.call('positional_order', [], return_type=int)
        self.assertEqual(1234, result)

        result, _ = await self.call('out_of_order', [], return_type=int)
        self.assertEqual(2413, result)

        result, _ = await self.call('mixed_in_order', [], return_type=int)
        self.assertEqual(5612, result)

        result, _ = await self.call('mixed_out_of_order', [], return_type=int)
        self.assertEqual(5621, result)

    async def test_call_function_with_kwargs_with_default_values(self):
        await self.set_up_contract('CallFunctionWithKwargsWithDefaultValues.py')

        result, _ = await self.call('positional_order', [], return_type=int)
        self.assertEqual(1234, result)

        result, _ = await self.call('out_of_order', [], return_type=int)
        self.assertEqual(2413, result)

        result, _ = await self.call('mixed_in_order', [], return_type=int)
        self.assertEqual(5612, result)

        result, _ = await self.call('mixed_out_of_order', [], return_type=int)
        self.assertEqual(5621, result)

        result, _ = await self.call('default_values', [], return_type=int)
        self.assertEqual(1034, result)

        result, _ = await self.call('only_default_values_and_kwargs', [], return_type=int)
        self.assertEqual(204, result)

    def test_call_function_with_kwargs_only(self):
        # TODO: change the test when creating a function that only accepts keywords is implemented #2ewewtz
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'CallFunctionWithKwargsOnly.py')

    def test_call_function_with_kwargs_self(self):
        # TODO: change the test when calling a function using the class is implemented #2ewewtz #2ewexau
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'CallFunctionWithKwargsSelf.py')

    def test_call_function_with_kwargs_wrong_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'CallFunctionWithKwargsWrongType.py')

    def test_call_function_with_kwargs_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'CallFunctionWithKwargsTooFewArguments.py')

    def test_call_function_with_kwargs_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'CallFunctionWithKwargsTooManyArguments.py')

    def test_call_function_with_kwargs_too_many_kw_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'CallFunctionWithKwargsTooManyKwArguments.py')

    async def test_boa2_fibonacci_test(self):
        await self.set_up_contract('FibonacciBoa2Test.py')

        result, _ = await self.call('main', [4], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', [5], return_type=int)
        self.assertEqual(5, result)

        result, _ = await self.call('main', [6], return_type=int)
        self.assertEqual(8, result)

        result, _ = await self.call('main', [7], return_type=int)
        self.assertEqual(13, result)

        result, _ = await self.call('main', [11], return_type=int)
        self.assertEqual(89, result)

    async def test_boa2_method_test(self):
        await self.set_up_contract('MethodBoa2Test.py')

        result, _ = await self.call('main', [1, 2], return_type=int)
        self.assertEqual(7, result)

        result, _ = await self.call('main', [-3, -100], return_type=int)
        self.assertEqual(-99, result)

    async def test_boa2_method_test2(self):
        await self.set_up_contract('MethodBoa2Test2.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(26, result)

    async def test_boa2_method_test3(self):
        await self.set_up_contract('MethodBoa2Test3.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(13, result)

    async def test_boa2_method_test4(self):
        await self.set_up_contract('MethodBoa2Test4.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(63, result)

    async def test_boa2_method_test5(self):
        await self.set_up_contract('MethodBoa2Test5.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(15, result)

    async def test_boa2_module_method_test1(self):
        await self.set_up_contract('ModuleMethodBoa2Test1.py')

        result, _ = await self.call('main', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_boa2_module_method_test2(self):
        await self.set_up_contract('ModuleMethodBoa2Test2.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(3003, result)

    async def test_boa2_module_variable_test(self):
        await self.set_up_contract('ModuleVariableBoa2Test.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(1260, result)

    async def test_boa2_module_variable_test1(self):
        await self.set_up_contract('ModuleVariableBoa2Test1.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(8, result)

    async def test_call_void_function_with_stared_argument(self):
        await self.set_up_contract('CallVoidFunctionWithStarredArgument.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    async def test_call_return_function_with_stared_argument(self):
        await self.set_up_contract('CallReturnFunctionWithStarredArgument.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(sum([1, 2, 3, 4, 5, 6]), result)

    async def test_return_starred_argument(self):
        await self.set_up_contract('ReturnStarredArgumentCount.py')

        result, _ = await self.call('fun_with_starred', [[1, 2, 3, 4, 5]], return_type=int)
        self.assertEqual(5, result)

        result, _ = await self.call('fun_with_starred', [[1, 2, 3]], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', [[1, 2, 3, 4, 5]], return_type=int)
        self.assertEqual(5, result)

        result, _ = await self.call('main', [[1, 2, 3]], return_type=int)
        self.assertEqual(3, result)

    async def test_call_function_with_same_name_in_different_scopes(self):
        await self.set_up_contract('CallFunctionsWithSameNameInDifferentScopes.py')

        result, _ = await self.call('result', [], return_type=list)
        self.assertEqual([10, 20], result)

    def test_function_with_dictionary_unpacking_operator(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'FunctionWithDictionaryUnpackingOperator.py')

    def test_functions_with_duplicated_name(self):
        self.assertCompilerLogs(CompilerError.DuplicatedIdentifier, 'FunctionsWithDuplicatedName.py')

    async def test_function_as_arg(self):
        await self.set_up_contract('FunctionAsArg.py')

        result, _ = await self.call('main', [123], return_type=int)
        self.assertEqual(123, result)

    async def test_function_with_arg_as_arg(self):
        await self.set_up_contract('FunctionWithArgAsArg.py')

        list_int = [123, 456, 789]
        value = 123
        result, _ = await self.call('main', [list_int, value], return_type=int)
        self.assertEqual(list_int.index(value), result)

    async def test_function_with_args_as_arg(self):
        await self.set_up_contract('FunctionWithArgsAsArg.py')

        list_int = [123, 456, 789]
        value = 123
        start = 0
        end = 5
        result, _ = await self.call('main', [list_int, value, start, end], return_type=int)
        self.assertEqual(list_int.index(value, start, end), result)

    async def test_other_contract_call_with_return_none(self):
        called_contract = await self.compile_and_deploy('NoReturnFunction.py')
        await self.set_up_contract('CallExternalContractWithReturnNone.py')

        result, _ = await self.call('main', [], return_type=None)
        self.assertIsNone(result)

    def test_inner_function(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'InnerFunction.py')

    def test_lambda_function(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'LambdaFunction.py')

    def test_function_custom_decorator_with_global_function(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'CustomDecoratorWithGlobalFunction.py')

    def test_function_builtin_function_decorators_with_class(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'BuiltinContractDecoratorWithFunction.py')
