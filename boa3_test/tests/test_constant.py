import sys

from boa3.compiler.codegenerator import CodeGenerator
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.StackItemType import StackItemType
from boa3_test.tests.boa_test import BoaTest


class TestConstant(BoaTest):

    def test_small_integer_constant(self):
        input = 7
        expected_output = Opcode.PUSH7

        generator = CodeGenerator({})
        generator.convert_integer_literal(input)
        output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_negative_integer_constant(self):
        input = -10
        byte_input = Integer(input).to_byte_array()
        expected_output = (
            Opcode.PUSHDATA1            # push the bytes
            + len(byte_input).to_bytes(1, sys.byteorder)
            + byte_input
            + Opcode.CONVERT            # convert to integer
            + StackItemType.Integer
        )

        generator = CodeGenerator({})
        generator.convert_integer_literal(input)
        output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_one_byte_integer_constant(self):
        input = 42
        byte_input = Integer(input).to_byte_array()
        expected_output = (
            Opcode.PUSHDATA1            # push the bytes
            + len(byte_input).to_bytes(1, sys.byteorder)
            + byte_input
            + Opcode.CONVERT            # convert to integer
            + StackItemType.Integer
        )

        generator = CodeGenerator({})
        generator.convert_integer_literal(input)
        output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_two_bytes_length_integer_constant(self):
        byte_input = bytes(300) + b'\x01'
        input = int.from_bytes(byte_input, sys.byteorder)
        expected_output = (
            Opcode.PUSHDATA2            # push the bytes
            + len(byte_input).to_bytes(2, sys.byteorder)
            + byte_input
            + Opcode.CONVERT            # convert to integer
            + StackItemType.Integer
        )

        generator = CodeGenerator({})
        generator.convert_integer_literal(input)
        output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_big_integer_constant(self):
        byte_input = bytes(100000) + b'\x01'
        input = int.from_bytes(byte_input, sys.byteorder)
        expected_output = (
            Opcode.PUSHDATA4            # push the bytes
            + len(byte_input).to_bytes(4, sys.byteorder)
            + byte_input
            + Opcode.CONVERT            # convert to integer
            + StackItemType.Integer
        )

        generator = CodeGenerator({})
        generator.convert_integer_literal(input)
        output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_string_constant(self):
        input = 'unit_test'
        byte_input = bytes(input, sys.getdefaultencoding())
        expected_output = (
            Opcode.PUSHDATA1            # push the bytes
            + len(byte_input).to_bytes(1, sys.byteorder)
            + byte_input
        )

        generator = CodeGenerator({})
        generator.convert_string_literal(input)
        output = generator.bytecode

        self.assertEqual(expected_output, output)
