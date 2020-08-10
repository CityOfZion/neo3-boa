from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestFor(BoaTest):

    def test_for_tuple_condition(self):
        jmpif_address = Integer(19).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-22).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH15     # for_sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.PUSH0      # for_index = 0
            + Opcode.JMP        # begin for
            + jmpif_address
                + Opcode.OVER           # x = for_sequence[for_index]
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
                + Opcode.LDLOC0         # a = a + x
                + Opcode.LDLOC1
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.INC            # for_index = for_index + 1
            + Opcode.DUP        # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/for_test/TupleCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_for_string_condition(self):
        sequence = String('3515').to_bytes(min_length=1)
        jmpif_address = Integer(24).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-27).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # b = ''
            + Integer(0).to_byte_array(min_length=1)
            + Opcode.STLOC1
            + Opcode.PUSHDATA1  # for_sequence = '3515'
            + Integer(len(sequence)).to_byte_array(min_length=1)
            + sequence
            + Opcode.PUSH0      # for_index = 0
            + Opcode.JMP
                + jmpif_address
                + Opcode.OVER           # x = for_sequence[for_index]
                + Opcode.OVER
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
                + Opcode.STLOC2
                + Opcode.LDLOC0         # a = a + 1
                + Opcode.PUSH1
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.LDLOC2         # b = x
                + Opcode.STLOC1
                + Opcode.INC            # for_index = for_index + 1
            + Opcode.DUP        # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/for_test/StringCondition.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_for_variable_condition(self):
        jmpif_address = Integer(19).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-22).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH15     # sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.LDLOC1     # for_sequence = sequence
            + Opcode.PUSH0      # for_index = 0
            + Opcode.JMP
            + jmpif_address
                + Opcode.OVER         # x = for_sequence[for_index]
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
                + Opcode.STLOC2
                + Opcode.LDLOC0         # a = a + x
                + Opcode.LDLOC2
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.INC            # for_index = for_index + 1
            + Opcode.DUP        # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/for_test/VariableCondition.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_for_mismatched_type_condition(self):
        path = '%s/boa3_test/test_sc/for_test/MismatchedTypeCondition.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_for_no_condition(self):
        path = '%s/boa3_test/test_sc/for_test/NoCondition.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_nested_for(self):
        outer_jmpif_address = Integer(47).to_byte_array(min_length=1, signed=True)
        outer_jmp_address = Integer(-50).to_byte_array(min_length=1, signed=True)

        inner_jmpif_address = Integer(21).to_byte_array(min_length=1, signed=True)
        inner_jmp_address = Integer(-24).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH15     # sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.LDLOC1     # outer_for_sequence = sequence
            + Opcode.PUSH0      # outer_for_index = 0
            + Opcode.JMP
            + outer_jmpif_address
                + Opcode.OVER           # x = outer_for_sequence[outer_for_index]
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
                + Opcode.STLOC2
                    + Opcode.LDLOC1     # inner_for_sequence = sequence
                    + Opcode.PUSH0      # inner_for_index = 0
                + Opcode.JMP
                + inner_jmpif_address
                    + Opcode.OVER         # y = inner_for_sequence[inner_for_index]
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
                    + Opcode.STLOC3
                    + Opcode.LDLOC0         # a = a + x * y
                    + Opcode.LDLOC2
                    + Opcode.LDLOC3
                    + Opcode.MUL
                    + Opcode.ADD
                    + Opcode.STLOC0
                    + Opcode.INC            # inner_for_index = inner_for_index + 1
                + Opcode.DUP        # if inner_for_index < len(inner_for_sequence)
                + Opcode.PUSH2
                + Opcode.PICK
                + Opcode.SIZE
                + Opcode.LT
                + Opcode.JMPIF      # end inner_for
                + inner_jmp_address
                + Opcode.DROP
                + Opcode.DROP
                + Opcode.INC     # outer_for_index = outer_for_index + 1
            + Opcode.DUP        # if outer_for_index < len(outer_for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end outer_for
            + outer_jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/for_test/NestedFor.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_for_else(self):
        jmpif_address = Integer(19).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-22).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH15     # sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.LDLOC1     # for_sequence = sequence
            + Opcode.PUSH0      # for_index = 0
            + Opcode.JMP
            + jmpif_address
                + Opcode.OVER           # x = for_sequence[for_index]
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
                + Opcode.STLOC2
                + Opcode.LDLOC0         # a = a + x
                + Opcode.LDLOC2
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.INC            # for_index = for_index + 1
            + Opcode.DUP        # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0     # a = a + 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/for_test/ForElse.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)
