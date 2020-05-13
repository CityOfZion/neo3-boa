from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest


class TestIf(BoaTest):

    def test_if_constant_condition(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH1
            + Opcode.JMPIFNOT   # if True
            + Integer(6).to_byte_array(min_length=1)
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/if_test/ConstantCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_if_variable_condition(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(6).to_byte_array(min_length=1)
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/if_test/VariableCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_if_mismatched_type_condition(self):
        path = '%s/boa3_test/example/if_test/MismatchedTypeCondition.py' % self.dirname

        with self.assertRaises(MismatchedTypes):
            output = Boa3.compile(path)

    def test_if_no_condition(self):
        path = '%s/boa3_test/example/if_test/NoCondition.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_nested_if(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x02'
            + Opcode.PUSH0      # c = 0
            + Opcode.STLOC0
            + Opcode.LDLOC0     # d = c
            + Opcode.STLOC1
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(17).to_byte_array(min_length=1)
                + Opcode.LDLOC0     # c = c + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.LDARG1
                + Opcode.JMPIFNOT   # if arg1
                + Integer(6).to_byte_array(min_length=1)
                    + Opcode.LDLOC1     # d = d + 3
                    + Opcode.PUSH3
                    + Opcode.ADD
                    + Opcode.STLOC1
                + Opcode.LDLOC0     # c = c + d
                + Opcode.LDLOC1
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.LDLOC0     # return c
            + Opcode.RET
        )

        path = '%s/boa3_test/example/if_test/NestedIf.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_if_else(self):
        path = '%s/boa3_test/example/if_test/IfElse.py' % self.dirname

        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)

    def test_while_relational_condition(self):
        jmp_address = Integer(6).to_byte_array(min_length=1)

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIFNOT   # if c < 10
            + jmp_address
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/example/if_test/RelationalCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)
