from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest


class TestFor(BoaTest):

    def test_for_tuple_condition(self):
        jmpif_address = Integer(14).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-16).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH15     # for_sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC1
            + Opcode.PUSH0      # for_index = 0
            + Opcode.STLOC2
            + Opcode.JMP        # begin for
            + jmpif_address
                + Opcode.LDLOC1         # x = for_sequence[for_index]
                + Opcode.LDLOC2
                + Opcode.PICKITEM
                + Opcode.STLOC3
                + Opcode.LDLOC0         # a = a + x
                + Opcode.LDLOC3
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.LDLOC2         # for_index = for_index + 1
                + Opcode.PUSH1
                + Opcode.ADD
                + Opcode.STLOC2
            + Opcode.LDLOC2     # if for_index < len(for_sequence)
            + Opcode.LDLOC1
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/for_test/TupleCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_for_string_condition(self):
        path = '%s/boa3_test/example/for_test/StringCondition.py' % self.dirname
        
        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)

    def test_for_variable_condition(self):
        jmpif_address = Integer(14).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-16).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x05'
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
            + Opcode.STLOC2
            + Opcode.PUSH0      # for_index = 0
            + Opcode.STLOC3
            + Opcode.JMP
            + jmpif_address
                + Opcode.LDLOC2         # x = for_sequence[for_index]
                + Opcode.LDLOC3
                + Opcode.PICKITEM
                + Opcode.STLOC4
                + Opcode.LDLOC0         # a = a + x
                + Opcode.LDLOC4
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.LDLOC3         # for_index = for_index + 1
                + Opcode.PUSH1
                + Opcode.ADD
                + Opcode.STLOC3
            + Opcode.LDLOC3     # if for_index < len(for_sequence)
            + Opcode.LDLOC2
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/for_test/VariableCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_for_mismatched_type_condition(self):
        path = '%s/boa3_test/example/for_test/MismatchedTypeCondition.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_for_no_condition(self):
        path = '%s/boa3_test/example/for_test/NoCondition.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_nested_for(self):
        outer_jmpif_address = Integer(38).to_byte_array(min_length=1, signed=True)
        outer_jmp_address = Integer(-40).to_byte_array(min_length=1, signed=True)

        inner_jmpif_address = Integer(18).to_byte_array(min_length=1, signed=True)
        inner_jmp_address = Integer(-20).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x08'
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
            + Opcode.STLOC2
            + Opcode.PUSH0      # outer_for_index = 0
            + Opcode.STLOC3
            + Opcode.JMP
            + outer_jmpif_address
                + Opcode.LDLOC2         # x = outer_for_sequence[outer_for_index]
                + Opcode.LDLOC3
                + Opcode.PICKITEM
                + Opcode.STLOC4
                    + Opcode.LDLOC1     # inner_for_sequence = sequence
                    + Opcode.STLOC5
                    + Opcode.PUSH0      # inner_for_index = 0
                    + Opcode.STLOC6
                + Opcode.JMP
                + inner_jmpif_address
                    + Opcode.LDLOC5         # y = inner_for_sequence[inner_for_index]
                    + Opcode.LDLOC6
                    + Opcode.PICKITEM
                    + Opcode.STLOC
                    + Integer(7).to_byte_array()
                    + Opcode.LDLOC0         # a = a + x * y
                    + Opcode.LDLOC4
                    + Opcode.LDLOC
                    + Integer(7).to_byte_array()
                    + Opcode.MUL
                    + Opcode.ADD
                    + Opcode.STLOC0
                    + Opcode.LDLOC6         # inner_for_index = inner_for_index + 1
                    + Opcode.PUSH1
                    + Opcode.ADD
                    + Opcode.STLOC6
                + Opcode.LDLOC6     # if inner_for_index < len(inner_for_sequence)
                + Opcode.LDLOC5
                + Opcode.SIZE
                + Opcode.LT
                + Opcode.JMPIF      # end inner_for
                + inner_jmp_address
                + Opcode.LDLOC3     # outer_for_index = outer_for_index + 1
                + Opcode.PUSH1
                + Opcode.ADD
                + Opcode.STLOC3
            + Opcode.LDLOC3     # if outer_for_index < len(outer_for_sequence)
            + Opcode.LDLOC2
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end outer_for
            + outer_jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/for_test/NestedFor.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_for_else(self):
        jmpif_address = Integer(14).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-16).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x05'
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
            + Opcode.STLOC2
            + Opcode.PUSH0      # for_index = 0
            + Opcode.STLOC3
            + Opcode.JMP
            + jmpif_address
                + Opcode.LDLOC2         # x = for_sequence[for_index]
                + Opcode.LDLOC3
                + Opcode.PICKITEM
                + Opcode.STLOC4
                + Opcode.LDLOC0         # a = a + x
                + Opcode.LDLOC4
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.LDLOC3         # for_index = for_index + 1
                + Opcode.PUSH1
                + Opcode.ADD
                + Opcode.STLOC3
            + Opcode.LDLOC3     # if for_index < len(for_sequence)
            + Opcode.LDLOC2
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.LDLOC0     # a = a + 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/for_test/ForElse.py' % self.dirname
        output = Boa3.compile(path)

        size = min(len(expected_output), len(output))
        for x in range(0, size - 1):
            if expected_output[x] != output[x]:
                print(x, '\texpected: ', expected_output[x], '\tactual: ', output[x])

        self.assertEqual(expected_output, output)
