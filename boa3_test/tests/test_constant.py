import ast
import sys

from boa3.analyser.analyser import Analyser
from boa3.compiler.codegenerator import CodeGenerator
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.StackItemType import StackItemType
from boa3.neo.vm.type.String import String
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
            + Integer(len(byte_input)).to_byte_array()
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
            + Integer(len(byte_input)).to_byte_array(min_length=1)
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
            + Integer(len(byte_input)).to_byte_array(min_length=2)
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
        input = Integer.from_bytes(byte_input)
        expected_output = (
            Opcode.PUSHDATA4            # push the bytes
            + Integer(len(byte_input)).to_byte_array(min_length=4)
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
        byte_input = String(input).to_bytes()
        expected_output = (
            Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
        )

        generator = CodeGenerator({})
        generator.convert_string_literal(input)
        output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_integer_tuple_constant(self):
        input = (1, 2, 3)
        expected_output = (
            Opcode.PUSH3        # 3
            + Opcode.PUSH2      # 2
            + Opcode.PUSH1      # 1
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
        )

        analyser = Analyser(ast.parse(str(input)))
        output = CodeGenerator.generate_code(analyser)

        self.assertEqual(expected_output, output)

    def test_string_tuple_constant(self):
        input = ('1', '2', '3')
        byte_input0 = String(input[0]).to_bytes()
        byte_input1 = String(input[1]).to_bytes()
        byte_input2 = String(input[2]).to_bytes()

        expected_output = (
            Opcode.PUSHDATA1    # '3'
            + Integer(len(byte_input2)).to_byte_array()
            + byte_input2
            + Opcode.PUSHDATA1  # '2'
            + Integer(len(byte_input1)).to_byte_array()
            + byte_input1
            + Opcode.PUSHDATA1  # '1'
            + Integer(len(byte_input0)).to_byte_array()
            + byte_input0
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
        )

        analyser = Analyser(ast.parse(str(input)))
        output = CodeGenerator.generate_code(analyser)

        self.assertEqual(expected_output, output)

    def test_any_tuple_constant(self):
        input = (1, '2', False)
        byte_input1 = String(input[1]).to_bytes()

        expected_output = (
            Opcode.PUSH0        # True
            + Opcode.PUSHDATA1  # '2'
            + Integer(len(byte_input1)).to_byte_array()
            + byte_input1
            + Opcode.PUSH1      # 1
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
        )

        analyser = Analyser(ast.parse(str(input)))
        output = CodeGenerator.generate_code(analyser)

        self.assertEqual(expected_output, output)

    def test_tuple_of_tuple_constant(self):
        input = ((1, 2), (3, 4, 5, 6), (7,))
        expected_output = (
            # tuple[2]
            Opcode.PUSH7    # 7
            + Opcode.PUSH1  # tuple length
            + Opcode.PACK
            # tuple[1]
            + Opcode.PUSH6  # 6
            + Opcode.PUSH5  # 7
            + Opcode.PUSH4  # 4
            + Opcode.PUSH3  # 3
            + Opcode.PUSH4  # tuple length
            + Opcode.PACK
            # tuple[0]
            + Opcode.PUSH2  # 2
            + Opcode.PUSH1  # 1
            + Opcode.PUSH2  # tuple length
            + Opcode.PACK
            + Opcode.PUSH3  # tuple length
            + Opcode.PACK
        )

        analyser = Analyser(ast.parse(str(input)))
        output = CodeGenerator.generate_code(analyser)

        self.assertEqual(expected_output, output)

    def test_integer_list_constant(self):
        input = [1, 2, 3]
        expected_output = (
            Opcode.PUSH3    # 3
            + Opcode.PUSH2  # 2
            + Opcode.PUSH1  # 1
            + Opcode.PUSH3  # list length
            + Opcode.PACK
        )

        analyser = Analyser(ast.parse(str(input)))
        output = CodeGenerator.generate_code(analyser)

        self.assertEqual(expected_output, output)

    def test_string_list_constant(self):
        input = ['1', '2', '3']
        byte_input0 = String(input[0]).to_bytes()
        byte_input1 = String(input[1]).to_bytes()
        byte_input2 = String(input[2]).to_bytes()

        expected_output = (
            Opcode.PUSHDATA1        # '2'
            + Integer(len(byte_input2)).to_byte_array()
            + byte_input2
            + Opcode.PUSHDATA1      # '1'
            + Integer(len(byte_input1)).to_byte_array()
            + byte_input1
            + Opcode.PUSHDATA1      # '0'
            + Integer(len(byte_input0)).to_byte_array()
            + byte_input0
            + Opcode.PUSH3          # list length
            + Opcode.PACK
        )

        analyser = Analyser(ast.parse(str(input)))
        output = CodeGenerator.generate_code(analyser)

        self.assertEqual(expected_output, output)

    def test_any_list_constant(self):
        input = [1, '2', False]
        byte_input1 = String(input[1]).to_bytes()

        expected_output = (
            Opcode.PUSH0        # False
            + Opcode.PUSHDATA1  # '2'
            + Integer(len(byte_input1)).to_byte_array()
            + byte_input1
            + Opcode.PUSH1      # 1
            + Opcode.PUSH3      # list length
            + Opcode.PACK
        )

        analyser = Analyser(ast.parse(str(input)))
        output = CodeGenerator.generate_code(analyser)

        self.assertEqual(expected_output, output)

    def test_list_of_list_constant(self):
        input = [[1, 2], [3, 4, 5, 6], [7]]
        expected_output = (
            # list[2]
            Opcode.PUSH7    # 7
            + Opcode.PUSH1  # list length
            + Opcode.PACK
            # list[1]
            + Opcode.PUSH6  # 6
            + Opcode.PUSH5  # 5
            + Opcode.PUSH4  # 4
            + Opcode.PUSH3  # 3
            + Opcode.PUSH4  # list length
            + Opcode.PACK
            # list[0]
            + Opcode.PUSH2  # 2
            + Opcode.PUSH1  # 1
            + Opcode.PUSH2  # list length
            + Opcode.PACK
            + Opcode.PUSH3  # list length
            + Opcode.PACK
        )

        analyser = Analyser(ast.parse(str(input)))
        output = CodeGenerator.generate_code(analyser)

        self.assertEqual(expected_output, output)
