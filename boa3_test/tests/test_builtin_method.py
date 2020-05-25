from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, UnexpectedArgument, UnfilledArgument
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestVariable(BoaTest):

    def test_len_of_tuple(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH3      # a = (1, 2, 3)
            + Opcode.NEWARRAY
            + Opcode.DUP        # array[0] = 1
            + Opcode.PUSH0
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP        # array[1] = 2
            + Opcode.PUSH1
            + Opcode.PUSH2
            + Opcode.SETITEM
            + Opcode.DUP        # array[2] = 3
            + Opcode.PUSH2
            + Opcode.PUSH3
            + Opcode.SETITEM
            + Opcode.STLOC0     # a = array
            + Opcode.LDLOC0     # b = len(a)
            + Opcode.SIZE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = '%s/boa3_test/example/built_in_methods_test/LenTuple.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_len_of_str(self):
        input = 'just a test'
        byte_input = String(input).to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.SIZE
            + Opcode.RET
        )
        path = '%s/boa3_test/example/built_in_methods_test/LenString.py' % self.dirname

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_len_of_no_collection(self):
        path = '%s/boa3_test/example/built_in_methods_test/LenMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_len_too_many_parameters(self):
        path = '%s/boa3_test/example/built_in_methods_test/LenTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_len_too_few_parameters(self):
        path = '%s/boa3_test/example/built_in_methods_test/LenTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)
