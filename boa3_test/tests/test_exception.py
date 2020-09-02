from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.builtin.builtin import Builtin
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestException(BoaTest):

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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/exception_test/RaiseExceptionEmptyMessage.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/exception_test/RaiseExceptionWithMessage.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/exception_test/RaiseExceptionWithoutCall.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/exception_test/RaiseVariableException.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_raise_exception_variable_message(self):
        exception_message = String('raised an exception').to_bytes()
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
            + Integer(4).to_byte_array(signed=True, min_length=1)
            + Opcode.LDLOC0         # raise Exception(x)
            + Opcode.THROW
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/exception_test/RaiseExceptionVariableMessage.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/exception_test/RaiseSpecificException.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_raise_mismatched_type(self):
        path = '%s/boa3_test/test_sc/exception_test/RaiseMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
