from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest


class TestWhile(BoaTest):

    def test_while_constant_condition(self):
        jmpif_address = Integer(6).to_byte_array(min_length=1)
        jmp_address = Integer(-5).to_byte_array(min_length=1)

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.JMP        # begin while
            + jmpif_address
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.PUSH0
            + Opcode.JMPIF      # end while False
            + jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/while_test/ConstantCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_while_variable_condition(self):
        jmpif_address = Integer(6).to_byte_array(min_length=1)
        jmp_address = Integer(-5).to_byte_array(min_length=1)

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.JMP        # begin while
            + jmpif_address
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIF      # end while arg0
            + jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/while_test/VariableCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_while_mismatched_type_condition(self):
        path = '%s/boa3_test/example/while_test/MismatchedTypeCondition.py' % self.dirname

        with self.assertRaises(MismatchedTypes):
            output = Boa3.compile(path)

    def test_while_no_condition(self):
        path = '%s/boa3_test/example/while_test/NoCondition.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_nested_while(self):
        outer_jmpif_address = Integer(19).to_byte_array(min_length=1)
        outer_jmp_address = Integer(-18).to_byte_array(min_length=1)

        inner_jmpif_address = Integer(6).to_byte_array(min_length=1)
        inner_jmp_address = Integer(-5).to_byte_array(min_length=1)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x02'
            + Opcode.PUSH0      # c = 0
            + Opcode.STLOC0
            + Opcode.LDLOC0     # d = c
            + Opcode.STLOC1
            + Opcode.JMP        # begin outer while
            + outer_jmpif_address
                + Opcode.LDLOC0     # c = c + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.JMP        # begin inner while
                + inner_jmpif_address
                    + Opcode.LDLOC1     # d = d + 3
                    + Opcode.PUSH3
                    + Opcode.ADD
                    + Opcode.STLOC1
                + Opcode.LDARG1
                + Opcode.JMPIF      # end inner while arg1
                + inner_jmp_address
                + Opcode.LDLOC0     # c = c + d
                + Opcode.LDLOC1
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIF      # end outer while arg0
            + outer_jmp_address
            + Opcode.LDLOC0     # return c
            + Opcode.RET
        )

        path = '%s/boa3_test/example/while_test/NestedWhile.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_while_else(self):
        jmpif_address = Integer(6).to_byte_array(min_length=1)
        jmp_address = Integer(-5).to_byte_array(min_length=1)

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.JMP        # begin while
            + jmpif_address
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.PUSH0
            + Opcode.JMPIF      # end while False
            + jmp_address
            + Opcode.LDLOC0     # else
            + Opcode.PUSH1          # a = a + 1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/while_test/WhileElse.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)
