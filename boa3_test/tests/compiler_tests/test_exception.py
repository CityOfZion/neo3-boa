from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestException(boatestcase.BoaTestCase):
    from boa3.internal.model.builtin.builtin import Builtin

    default_folder: str = 'test_sc/exception_test'

    default_message = Builtin.Exception.default_message
    EXCEPTION_EMPTY_MESSAGE = String(default_message).to_bytes()
    UNHANDLED_ERROR_MESSAGE = r'unhandled exception: "{0}"'

    def test_raise_exception_empty_message_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(14).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise Exception
            + Integer(len(self.EXCEPTION_EMPTY_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.EXCEPTION_EMPTY_MESSAGE
            + Opcode.THROW
            + Opcode.RET
        )

        output, _ = self.assertCompile('RaiseExceptionEmptyMessage.py')
        self.assertEqual(expected_output, output)

    async def test_raise_exception_empty_message_run(self):
        await self.set_up_contract('RaiseExceptionEmptyMessage.py')
        
        result, _ = await self.call('test_raise', [10], return_type=None)
        self.assertIsNone(result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('test_raise', [-10], return_type=None)

        self.assertRegex(str(context.exception), self.UNHANDLED_ERROR_MESSAGE.format(self.default_message))

    def test_raise_exception_with_message_compile(self):
        exception_message = String('raised an exception').to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(24).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise Exception('raised an exception')
            + Integer(len(exception_message)).to_byte_array(signed=True, min_length=1)
            + exception_message
            + Opcode.THROW
            + Opcode.RET
        )

        output, _ = self.assertCompile('RaiseExceptionWithMessage.py')
        self.assertEqual(expected_output, output)

    async def test_raise_exception_with_message_run(self):
        await self.set_up_contract('RaiseExceptionWithMessage.py')

        exception_message = 'raised an exception'
        result, _ = await self.call('test_raise', [10], return_type=None)
        self.assertIsNone(result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('test_raise', [-10], return_type=None)

        self.assertRegex(str(context.exception), self.UNHANDLED_ERROR_MESSAGE.format(exception_message))

    def test_raise_exception_without_call_contract(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(14).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise Exception
            + Integer(len(self.EXCEPTION_EMPTY_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.EXCEPTION_EMPTY_MESSAGE
            + Opcode.THROW
            + Opcode.RET
        )

        output, _ = self.assertCompile('RaiseExceptionWithoutCall.py')
        self.assertEqual(expected_output, output)

    async def test_raise_exception_without_call_run(self):
        await self.set_up_contract('RaiseExceptionWithoutCall.py')

        result, _ = await self.call('test_raise', [10], return_type=None)
        self.assertIsNone(result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('test_raise', [-10], return_type=None)

        self.assertRegex(str(context.exception), self.UNHANDLED_ERROR_MESSAGE.format(self.default_message))

    def test_raise_variable_exception_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHDATA1  # x = Exception
            + Integer(len(self.EXCEPTION_EMPTY_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.EXCEPTION_EMPTY_MESSAGE
            + Opcode.STLOC0
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0         # raise x
            + Opcode.THROW
            + Opcode.RET
        )

        output, _ = self.assertCompile('RaiseVariableException.py')
        self.assertEqual(expected_output, output)

    async def test_raise_variable_exception_run(self):
        await self.set_up_contract('RaiseVariableException.py')

        result, _ = await self.call('test_raise', [10], return_type=None)
        self.assertIsNone(result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('test_raise', [-10], return_type=None)

        self.assertRegex(str(context.exception), self.UNHANDLED_ERROR_MESSAGE.format(self.default_message))

    def test_raise_exception_variable_message_compile(self):
        message = 'raised an exception'
        exception_message = String(message).to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHDATA1  # x = 'raised an exception'
            + Integer(len(exception_message)).to_byte_array(signed=True, min_length=1)
            + exception_message
            + Opcode.STLOC0
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(24).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise Exception(x)
            + Integer(len(exception_message)).to_byte_array(signed=True, min_length=1)
            + exception_message
            + Opcode.THROW
            + Opcode.RET
        )

        output, _ = self.assertCompile('RaiseExceptionVariableMessage.py')
        self.assertEqual(expected_output, output)

    async def test_raise_exception_variable_message_run(self):
        await self.set_up_contract('RaiseExceptionVariableMessage.py')

        exception_message = 'raised an exception'
        result, _ = await self.call('test_raise', [10], return_type=None)
        self.assertIsNone(result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('test_raise', [-10], return_type=None)

        self.assertRegex(str(context.exception), self.UNHANDLED_ERROR_MESSAGE.format(exception_message))

    def test_raise_specific_exception_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if arg0 < 0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT
            + Integer(14).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1      # raise ValueError
            + Integer(len(self.EXCEPTION_EMPTY_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.EXCEPTION_EMPTY_MESSAGE
            + Opcode.THROW
            + Opcode.RET
        )

        output, _ = self.assertCompile('RaiseSpecificException.py')
        self.assertEqual(expected_output, output)

    async def test_raise_specific_exception_run(self):
        await self.set_up_contract('RaiseSpecificException.py')

        result, _ = await self.call('test_raise', [10], return_type=None)
        self.assertIsNone(result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('test_raise', [-10], return_type=None)

        self.assertRegex(str(context.exception), self.UNHANDLED_ERROR_MESSAGE.format(self.default_message))

    def test_raise_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'RaiseMismatchedType.py')

    def test_try_except_without_exception_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.TRY        # try:
            + Integer(7).to_byte_array(signed=True, min_length=1)  # jmp to exception
            + Integer(0).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDARG0         # x = arg
            + Opcode.STLOC0
            + Opcode.JMP        # except:
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0          # x = 0
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(2).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        output, _ = self.assertCompile('TryExceptWithoutException.py')
        self.assertEqual(expected_output, output)

    async def test_try_except_without_exception_run(self):
        await self.set_up_contract('TryExceptWithoutException.py')

        result, _ = await self.call('test_try_except', [10], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('test_try_except', [-110], return_type=int)
        self.assertEqual(-110, result)

    def test_try_except_base_exception_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.TRY        # try:
            + Integer(7).to_byte_array(signed=True, min_length=1)  # jmp to exception
            + Integer(0).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDARG0         # x = arg
            + Opcode.STLOC0
            + Opcode.JMP        # except BaseException:
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0          # x = 0
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(2).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        output, _ = self.assertCompile('TryExceptBaseException.py')
        self.assertEqual(expected_output, output)

    async def test_try_except_base_exception_run(self):
        await self.set_up_contract('TryExceptBaseException.py')

        result, _ = await self.call('test_try_except', [10], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('test_try_except', [-110], return_type=int)
        self.assertEqual(-110, result)

    def test_try_except_specific_exception_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.TRY        # try:
            + Integer(7).to_byte_array(signed=True, min_length=1)  # jmp to exception
            + Integer(0).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDARG0         # x = arg
            + Opcode.STLOC0
            + Opcode.JMP        # except ValueError:
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0          # x = 0
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(2).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.UsingSpecificException, 'TryExceptSpecificException.py')
        self.assertEqual(expected_output, output)

    async def test_try_except_specific_exception_run(self):
        await self.set_up_contract('TryExceptSpecificException.py')

        result, _ = await self.call('test_try_except', [10], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('test_try_except', [-110], return_type=int)
        self.assertEqual(-110, result)

    def test_try_except_with_name(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'TryExceptWithName.py')

    def test_try_except_finally_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH4
            + Opcode.DIV
            + Opcode.STLOC0
            + Opcode.TRY        # try:
            + Integer(9).to_byte_array(signed=True, min_length=1)   # jmp to exception
            + Integer(15).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDLOC0         # x += arg
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.JMP        # except ValueError:
            + Integer(6).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.LDLOC0         # x = -x
            + Opcode.NEGATE
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # finally
            + Opcode.PUSH2          # x *= 2
            + Opcode.MUL
            + Opcode.STLOC0
            + Opcode.ENDFINALLY
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        output, _ = self.assertCompile('TryExceptFinally.py')
        self.assertEqual(expected_output, output)

    async def test_try_except_finally_run(self):
        await self.set_up_contract('TryExceptFinally.py')

        result, _ = await self.call('test_try_except', [10], return_type=int)
        self.assertEqual(24, result)

        result, _ = await self.call('test_try_except', [-110], return_type=int)
        self.assertEqual(-274, result)

    def test_try_except_else_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.TRY        # try:
            + Integer(7).to_byte_array(signed=True, min_length=1)  # jmp to exception
            + Integer(0).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDARG0         # x = arg
            + Opcode.STLOC0
            + Opcode.JMP        # except BaseException:
            + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSH0          # x = 0
            + Opcode.STLOC0
            + Opcode.JMP        # else:
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.LDARG0         # x = -arg
            + Opcode.NEGATE
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(2).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        output, _ = self.assertCompile('TryExceptElse.py')
        self.assertEqual(expected_output, output)

    async def test_try_except_else_run(self):
        await self.set_up_contract('TryExceptElse.py')

        result, _ = await self.call('test_try_except', [10], return_type=int)
        self.assertEqual(-10, result)

        result, _ = await self.call('test_try_except', [-110], return_type=int)
        self.assertEqual(110, result)

    def test_try_except_else_finally_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH4
            + Opcode.DIV
            + Opcode.STLOC0
            + Opcode.TRY        # try:
            + Integer(9).to_byte_array(signed=True, min_length=1)   # jmp to exception
            + Integer(21).to_byte_array(signed=True, min_length=1)  # jmp to finally if exists
            + Opcode.LDLOC0         # x += arg
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.JMP        # except ValueError:
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.LDLOC0         # x = -x
            + Opcode.NEGATE
            + Opcode.STLOC0
            + Opcode.JMP        # else:
            + Integer(6).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0         # x += arg
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.ENDTRY
            + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0     # finally
            + Opcode.PUSH2          # x *= 2
            + Opcode.MUL
            + Opcode.STLOC0
            + Opcode.ENDFINALLY
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        output, _ = self.assertCompile('TryExceptElseFinally.py')
        self.assertEqual(expected_output, output)

    async def test_try_except_else_finally_run(self):
        await self.set_up_contract('TryExceptElseFinally.py')

        result, _ = await self.call('test_try_except', [10], return_type=int)
        self.assertEqual(44, result)

        result, _ = await self.call('test_try_except', [-110], return_type=int)
        self.assertEqual(-494, result)
