from boa3.boa3 import Boa3
from boa3.exception.CompilerError import UnresolvedOperation
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestString(BoaTest):

    def test_string_get_value(self):
        path = '%s/boa3_test/test_sc/string_test/GetValue.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.PUSH1
            + Opcode.SUBSTR
            + Opcode.CONVERT
            + Type.str.stack_item
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_string_set_value(self):
        path = '%s/boa3_test/test_sc/string_test/SetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_string_slicing(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[2:3]
            + Opcode.PUSH2
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.PUSH3      # size = 3 - 2
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.OVER
            + Opcode.SUB
            + Opcode.SUBSTR
            + Opcode.CONVERT
            + Type.str.stack_item
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingLiteralValues.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_string_slicing_with_variables(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH2      # a1 = 2
            + Opcode.STLOC0
            + Opcode.PUSH3      # a2 = 3
            + Opcode.STLOC1
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC2
            + Opcode.LDLOC2     # return a[a1:a2]
            + Opcode.LDLOC0
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.LDLOC1     # size = a2 - a1
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.OVER
            + Opcode.SUB
            + Opcode.SUBSTR
            + Opcode.CONVERT
            + Type.str.stack_item
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingVariableValues.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_string_slicing_negative_start(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:-4]
            + Opcode.PUSH4            # size of the substring: len(a) - 4
            + Opcode.NEGATE
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.LEFT
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingNegativeStart.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_string_slicing_negative_end(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[-4:]
            + Opcode.DUP            # size of the substring: len(a) - (len(a) - 4) = 4
            + Opcode.SIZE
            + Opcode.PUSH4
            + Opcode.NEGATE
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.SUB
            + Opcode.RIGHT
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingNegativeEnd.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_string_slicing_start_omitted(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:3]
            + Opcode.PUSH3            # size of the substring: 3
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.LEFT
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingStartOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_string_slicing_omitted(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:3]
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_string_slicing_end_omitted(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[2:]
            + Opcode.DUP            # size of the substring: len(a) - 2
            + Opcode.SIZE
            + Opcode.PUSH2
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.SUB
            + Opcode.RIGHT
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/string_test/StringSlicingEndOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_string_slicing_omitted_stride(self):
        path = '%s/boa3_test/test_sc/string_test/StringSlicingWithStride.py' % self.dirname
        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)

    def test_string_slicing_omitted_with_stride(self):
        path = '%s/boa3_test/test_sc/string_test/StringSlicingOmittedWithStride.py' % self.dirname
        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)
