from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest


class TestWhile(BoaTest):

    def test_while_constant_condition(self):
        jmpif_address = Integer(6).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-5).to_byte_array(min_length=1, signed=True)

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

        path = '%s/boa3_test/test_sc/while_test/ConstantCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_while_variable_condition(self):
        jmpif_address = Integer(6).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-5).to_byte_array(min_length=1, signed=True)

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

        path = '%s/boa3_test/test_sc/while_test/VariableCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_while_mismatched_type_condition(self):
        path = '%s/boa3_test/test_sc/while_test/MismatchedTypeCondition.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_while_no_condition(self):
        path = '%s/boa3_test/test_sc/while_test/NoCondition.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_nested_while(self):
        outer_jmpif_address = Integer(19).to_byte_array(min_length=1, signed=True)
        outer_jmp_address = Integer(-18).to_byte_array(min_length=1, signed=True)

        inner_jmpif_address = Integer(6).to_byte_array(min_length=1, signed=True)
        inner_jmp_address = Integer(-5).to_byte_array(min_length=1, signed=True)

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

        path = '%s/boa3_test/test_sc/while_test/NestedWhile.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_while_else(self):
        jmpif_address = Integer(6).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-5).to_byte_array(min_length=1, signed=True)

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

        path = '%s/boa3_test/test_sc/while_test/WhileElse.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_while_relational_condition(self):
        jmpif_address = Integer(10).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-11).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x02'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # b = 0
            + Opcode.STLOC1
            + Opcode.JMP        # begin while
            + jmpif_address
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.LDLOC1     # b = b + 1
                + Opcode.PUSH1
                + Opcode.ADD
                + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIF      # end while b < 10
            + jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/while_test/RelationalCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_while_multiple_relational_condition(self):
        jmpif_address = Integer(10).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-15).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x02'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # b = 0
            + Opcode.STLOC1
            + Opcode.JMP        # begin while
            + jmpif_address
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.LDLOC1     # b = b + 1
                + Opcode.PUSH1
                + Opcode.ADD
                + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.PUSH10
            + Opcode.LDARG1
            + Opcode.LT
            + Opcode.BOOLAND
            + Opcode.JMPIF      # end while b < 10 < arg1
            + jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/while_test/MultipleRelationalCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_boa2_while_test(self):
        path = '%s/boa3_test/test_sc/while_test/WhileBoa2Test.py' % self.dirname

        # TODO: change test when 'break' are implemented
        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)

    def test_boa2_while_test1(self):
        jmpif_address = Integer(6).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-7).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3          # j = 3
            + Opcode.STLOC0
            + Opcode.JMP            # while
            + jmpif_address
                + Opcode.LDLOC0         # j = j + 1
                + Opcode.PUSH1
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.LDLOC0         # while j < 6
            + Opcode.PUSH6
            + Opcode.LT
            + Opcode.JMPIF
            + jmp_address
            + Opcode.LDLOC0         # return j
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/while_test/WhileBoa2Test1.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_boa2_while_test2(self):
        path = '%s/boa3_test/test_sc/while_test/WhileBoa2Test2.py' % self.dirname

        # TODO: change test when 'break' are implemented
        with self.assertRaises(NotImplementedError):
            output = Boa3.compile(path)
