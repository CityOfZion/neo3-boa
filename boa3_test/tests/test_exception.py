from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation
from boa3.exception.CompilerWarning import UsingSpecificException
from boa3.model.builtin.builtin import Builtin
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestException(BoaTest):

    default_folder: str = 'test_sc/exception_test'

    EXCEPTION_EMPTY_MESSAGE = String(Builtin.Exception.default_message).to_bytes()

    def test_raise_exception_empty_message(self):
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

        path = self.get_contract_path('RaiseExceptionEmptyMessage.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        self.run_smart_contract(engine, path, 'test_raise', 10)

        with self.assertRaises(TestExecutionException, msg=self.EXCEPTION_EMPTY_MESSAGE):
            self.run_smart_contract(engine, path, 'test_raise', -10)

    def test_raise_exception_with_message(self):
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

        path = self.get_contract_path('RaiseExceptionWithMessage.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        self.run_smart_contract(engine, path, 'test_raise', 10)

        with self.assertRaises(TestExecutionException, msg=self.EXCEPTION_EMPTY_MESSAGE):
            self.run_smart_contract(engine, path, 'test_raise', -10)

    def test_raise_exception_without_call(self):
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

        path = self.get_contract_path('RaiseExceptionWithoutCall.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        self.run_smart_contract(engine, path, 'test_raise', 10)

        with self.assertRaises(TestExecutionException, msg=self.EXCEPTION_EMPTY_MESSAGE):
            self.run_smart_contract(engine, path, 'test_raise', -10)

    def test_raise_variable_exception(self):
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

        path = self.get_contract_path('RaiseVariableException.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        self.run_smart_contract(engine, path, 'test_raise', 10)

        with self.assertRaises(TestExecutionException, msg=self.EXCEPTION_EMPTY_MESSAGE):
            self.run_smart_contract(engine, path, 'test_raise', -10)

    def test_raise_exception_variable_message(self):
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

        path = self.get_contract_path('RaiseExceptionVariableMessage.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        self.run_smart_contract(engine, path, 'test_raise', 10)

        with self.assertRaises(TestExecutionException, msg=message):
            self.run_smart_contract(engine, path, 'test_raise', -10)

    def test_raise_specific_exception(self):
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

        path = self.get_contract_path('RaiseSpecificException.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        self.run_smart_contract(engine, path, 'test_raise', 10)

        with self.assertRaises(TestExecutionException, msg=self.EXCEPTION_EMPTY_MESSAGE):
            self.run_smart_contract(engine, path, 'test_raise', -10)

    def test_raise_mismatched_type(self):
        path = self.get_contract_path('RaiseMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_try_except_without_exception(self):
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

        path = self.get_contract_path('TryExceptWithoutException.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'test_try_except', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'test_try_except', -110)
        self.assertEqual(-110, result)

    def test_try_except_base_exception(self):
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

        path = self.get_contract_path('TryExceptBaseException.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'test_try_except', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'test_try_except', -110)
        self.assertEqual(-110, result)

    def test_try_except_specific_exception(self):
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

        path = self.get_contract_path('TryExceptSpecificException.py')
        output = self.assertCompilerLogs(UsingSpecificException, path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'test_try_except', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'test_try_except', -110)
        self.assertEqual(-110, result)

    def test_try_except_with_name(self):
        path = self.get_contract_path('TryExceptWithName.py')
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_try_except_finally(self):
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

        path = self.get_contract_path('TryExceptFinally.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'test_try_except', 10)
        self.assertEqual(24, result)
        result = self.run_smart_contract(engine, path, 'test_try_except', -110)
        self.assertEqual(-274, result)
