import ast

from boa3_test.tests.boa_test import BoaTest, _COMPILER_LOCK as LOCK  # needs to be the first import to avoid circular imports

from boa3.internal.analyser.analyser import Analyser
from boa3.internal.compiler.codegenerator.codegenerator import CodeGenerator
from boa3.internal.compiler.codegenerator.optimizerhelper import OptimizationLevel
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String


class TestConstant(BoaTest):
    def build_code_generator(self) -> CodeGenerator:
        from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping

        VMCodeMapping.reset()
        return CodeGenerator({})

    def test_small_integer_constant(self):
        input = 7
        expected_output = Opcode.PUSH7

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_integer_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_small_negative_integer_constant(self):
        input = -10
        expected_output = (
            Opcode.PUSH10
            + Opcode.NEGATE
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_integer_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_negative_integer_constant(self):
        input = -100
        byte_input = Integer(input).to_byte_array()
        expected_output = (
            Opcode.PUSHINT8             # push the bytes
            + byte_input
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_integer_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_one_byte_length_integer_constant(self):
        input = 42
        byte_input = Integer(input).to_byte_array()
        expected_output = (
            Opcode.PUSHINT8             # push the bytes
            + byte_input
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_integer_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_two_bytes_length_length_integer_constant(self):
        byte_input = bytes(300) + b'\x01'
        input = Integer.from_bytes(byte_input)
        expected_output = (
            Opcode.PUSHINT256           # push the bytes
            + byte_input[:32]
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_integer_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_big_integer_constant(self):
        byte_input = bytes(100000) + b'\x01'
        input = Integer.from_bytes(byte_input)
        expected_output = (
            Opcode.PUSHINT256           # push the bytes
            + byte_input[:32]
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_integer_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_ambiguous_integer_constant(self):
        byte_input = b'\x00\x80'
        unsigned = Integer.from_bytes(byte_input, signed=False)
        signed = Integer.from_bytes(byte_input, signed=True)
        self.assertNotEqual(unsigned, signed)

        unsigned_byte_input = Integer(unsigned).to_byte_array(signed=True, min_length=4)
        self.assertNotEqual(byte_input, unsigned_byte_input)
        unsigned_expected_output = (
            Opcode.PUSHINT32            # push the bytes
            + unsigned_byte_input
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_integer_literal(unsigned)
            output = generator.bytecode

        self.assertEqual(unsigned_expected_output, output)

        signed_byte_input = Integer(signed).to_byte_array(signed=True, min_length=2)
        self.assertEqual(byte_input, signed_byte_input)
        signed_expected_output = (
            Opcode.PUSHINT16           # push the bytes
            + signed_byte_input
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_integer_literal(signed)
            output = generator.bytecode

        self.assertEqual(signed_expected_output, output)

    def test_string_constant(self):
        input = 'unit_test'
        byte_input = String(input).to_bytes()
        expected_output = (
            Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
        )

        with LOCK:
            generator = self.build_code_generator()
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

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_string_tuple_constant(self):
        input = ('1', '2', '3')
        byte_input0 = String(input[0]).to_bytes()
        byte_input1 = String(input[1]).to_bytes()
        byte_input2 = String(input[2]).to_bytes()

        expected_output = (
            Opcode.INITSSLOT + b'\x01'
            + Opcode.PUSHDATA1  # '3'
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
            + Opcode.DROP
            + Opcode.RET
        )

        analyser = Analyser(ast.parse(str(input)))
        analyser.symbol_table['x'] = Variable(Type.any)
        with LOCK:
            output = CodeGenerator.generate_code(analyser, OptimizationLevel.DEFAULT).bytecode

        self.assertEqual(expected_output, output)

    def test_any_tuple_constant(self):
        input = (1, '2', False)
        byte_input1 = String(input[1]).to_bytes()

        expected_output = (
            Opcode.PUSHF        # False
            + Opcode.PUSHDATA1  # '2'
            + Integer(len(byte_input1)).to_byte_array()
            + byte_input1
            + Opcode.PUSH1      # 1
            + Opcode.PUSH3      # tuple length
            + Opcode.PACK
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

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

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

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

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

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

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_any_list_constant(self):
        input = [1, '2', False]
        byte_input1 = String(input[1]).to_bytes()

        expected_output = (
            Opcode.PUSHF        # False
            + Opcode.PUSHDATA1  # '2'
            + Integer(len(byte_input1)).to_byte_array()
            + byte_input1
            + Opcode.PUSH1      # 1
            + Opcode.PUSH3      # list length
            + Opcode.PACK
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

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

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_integer_dict_constant(self):
        input = {1: 15, 2: 14, 3: 13}
        expected_output = (
            Opcode.NEWMAP     # {1: 15, 2: 14, 3: 13}
            + Opcode.DUP
            + Opcode.PUSH1      # map[1] = 15
            + Opcode.PUSH15
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH2      # map[2] = 14
            + Opcode.PUSH14
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH3      # map[3] = 13
            + Opcode.PUSH13
            + Opcode.SETITEM
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_string_dict_constant(self):
        input = {'one': 1, 'two': 2, 'three': 3}
        one = String('one').to_bytes()
        two = String('two').to_bytes()
        three = String('three').to_bytes()

        expected_output = (
            Opcode.NEWMAP     # {'one': 1, 'two': 2, 'three': 3}
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['one'] = 1
            + Integer(len(one)).to_byte_array(min_length=1)
            + one
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['two'] = 2
            + Integer(len(two)).to_byte_array(min_length=1)
            + two
            + Opcode.PUSH2
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['three'] = 3
            + Integer(len(three)).to_byte_array(min_length=1)
            + three
            + Opcode.PUSH3
            + Opcode.SETITEM
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_any_dict_constant(self):
        input = {1: True, 2: 4, 3: 'nine'}
        nine = String('nine').to_bytes()

        expected_output = (
            Opcode.NEWMAP  # {1: True, 2: 4, 3: 'nine'}
            + Opcode.DUP
            + Opcode.PUSH1  # map[1] = True
            + Opcode.PUSHT
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH2  # map[2] = 4
            + Opcode.PUSH4
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH3  # map[3] = 'nine'
            + Opcode.PUSHDATA1
            + Integer(len(nine)).to_byte_array(min_length=1)
            + nine
            + Opcode.SETITEM
        )

        with LOCK:
            generator = self.build_code_generator()
            generator.convert_literal(input)
            output = generator.bytecode

        self.assertEqual(expected_output, output)

    def test_integer_script_hash(self):
        from boa3.internal.neo import cryptography, to_script_hash

        input = Integer(123).to_byte_array()
        expected_output = cryptography.hash160(input)
        output = to_script_hash(input)

        self.assertEqual(expected_output, output)

    def test_string_script_hash(self):
        import base58
        from boa3.internal.neo import to_script_hash

        input = String('NUnLWXALK2G6gYa7RadPLRiQYunZHnncxg').to_bytes()
        expected_output = base58.b58decode(input)[1:21]
        output = to_script_hash(input)

        self.assertEqual(expected_output, output)

    def test_bytes_script_hash(self):
        from boa3.internal.neo import cryptography, to_script_hash

        input = b'\x01\x02\x03'
        expected_output = cryptography.hash160(input)
        output = to_script_hash(input)

        self.assertEqual(expected_output, output)

    def test_address_script_hash(self):
        from base58 import b58decode
        from boa3.internal.neo import cryptography, to_script_hash

        input = String('Nd7eAuHsKvvzHzSPyuJQALcYCcUrcwvm5W').to_bytes()
        expected_output = b58decode(input)[1:21]
        wrong_output = cryptography.hash160(input)
        output = to_script_hash(input)

        self.assertNotEqual(wrong_output, output)
        self.assertEqual(expected_output, output)
