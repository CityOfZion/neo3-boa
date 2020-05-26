from boa3.boa3 import Boa3
from boa3.exception.CompilerError import UnresolvedOperation, MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestTuple(BoaTest):

    def test_tuple_int_values(self):
        path = '%s/boa3_test/example/tuple_test/IntTuple.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # tuple length
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
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_string_values(self):
        path = '%s/boa3_test/example/tuple_test/StrTuple.py' % self.dirname
        byte_input0 = String('1').to_bytes()
        byte_input1 = String('2').to_bytes()
        byte_input2 = String('3').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # tuple length
            + Opcode.NEWARRAY
            + Opcode.DUP        # array[0] = '1'
            + Opcode.PUSH0
            + Opcode.PUSHDATA1
            + Integer(len(byte_input0)).to_byte_array()
            + byte_input0
            + Opcode.SETITEM
            + Opcode.DUP        # array[1] = '2'
            + Opcode.PUSH1
            + Opcode.PUSHDATA1
            + Integer(len(byte_input1)).to_byte_array()
            + byte_input1
            + Opcode.SETITEM
            + Opcode.DUP        # array[2] = '3'
            + Opcode.PUSH2
            + Opcode.PUSHDATA1
            + Integer(len(byte_input2)).to_byte_array()
            + byte_input2
            + Opcode.SETITEM
            + Opcode.STLOC0     # a = array
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_bool_values(self):
        path = '%s/boa3_test/example/tuple_test/BoolTuple.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # tuple length
            + Opcode.NEWARRAY
            + Opcode.DUP        # array[0] = True
            + Opcode.PUSH0
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP        # array[1] = True
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP        # array[2] = False
            + Opcode.PUSH2
            + Opcode.PUSH0
            + Opcode.SETITEM
            + Opcode.STLOC0     # a = array
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_variable_values(self):
        path = '%s/boa3_test/example/tuple_test/VariableTuple.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH1      # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2      # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH3      # c = 3
            + Opcode.STLOC2
            + Opcode.PUSH3      # tuple length
            + Opcode.NEWARRAY
            + Opcode.DUP        # array[0] = a
            + Opcode.PUSH0
            + Opcode.LDLOC0
            + Opcode.SETITEM
            + Opcode.DUP        # array[1] = b
            + Opcode.PUSH1
            + Opcode.LDLOC1
            + Opcode.SETITEM
            + Opcode.DUP        # array[2] = c
            + Opcode.PUSH2
            + Opcode.LDLOC2
            + Opcode.SETITEM
            + Opcode.STLOC3     # d = array
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_tuple_get_value(self):
        path = '%s/boa3_test/example/tuple_test/GetValue.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_non_sequence_get_value(self):
        path = '%s/boa3_test/example/tuple_test/MismatchedTypeGetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_tuple_set_value(self):
        path = '%s/boa3_test/example/tuple_test/SetValue.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0] = 1
            + Opcode.PUSH0
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.PUSH1      # return 1
            + Opcode.RET
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_non_sequence_set_value(self):
        path = '%s/boa3_test/example/tuple_test/MismatchedTypeSetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_tuple_index_mismatched_type(self):
        path = '%s/boa3_test/example/tuple_test/MismatchedTypeTupleIndex.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_tuple_of_tuple(self):
        path = '%s/boa3_test/example/tuple_test/TupleOfTuple.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0][0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_nep5_main(self):
        path = '%s/boa3_test/example/tuple_test/Nep5Main.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG1     # args[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)
