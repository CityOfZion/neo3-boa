from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.type.type import Type
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
            + Integer(6).to_byte_array(min_length=1, signed=True)
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/if_test/ConstantCondition.py' % self.dirname
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
            + Integer(6).to_byte_array(min_length=1, signed=True)
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/if_test/VariableCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_if_mismatched_type_condition(self):
        path = '%s/boa3_test/test_sc/if_test/MismatchedTypeCondition.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_if_no_condition(self):
        path = '%s/boa3_test/test_sc/if_test/IfWithoutCondition.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_if_no_body(self):
        path = '%s/boa3_test/test_sc/if_test/IfWithoutBody.py' % self.dirname

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
            + Integer(17).to_byte_array(min_length=1, signed=True)
                + Opcode.LDLOC0     # c = c + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
                + Opcode.LDARG1
                + Opcode.JMPIFNOT   # if arg1
                + Integer(6).to_byte_array(min_length=1, signed=True)
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

        path = '%s/boa3_test/test_sc/if_test/NestedIf.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_if_else(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(8).to_byte_array(min_length=1, signed=True)
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.JMP        # else
            + Integer(4).to_byte_array(min_length=1, signed=True)
                + Opcode.PUSH10     # a = 10
                + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/if_test/IfElse.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_else_no_body(self):
        path = '%s/boa3_test/test_sc/if_test/ElseWithoutBody.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_if_elif(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(8).to_byte_array(min_length=1)
                + Opcode.LDLOC0     # a = a + 2
                + Opcode.PUSH2
                + Opcode.ADD
                + Opcode.STLOC0
            + Opcode.JMP
            + Integer(7).to_byte_array(min_length=1)
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # elif arg0
            + Integer(4).to_byte_array(min_length=1)
                + Opcode.PUSH10     # a = 10
                + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/if_test/IfElif.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_elif_no_condition(self):
        path = '%s/boa3_test/test_sc/if_test/ElifWithoutCondition.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_elif_no_body(self):
        path = '%s/boa3_test/test_sc/if_test/ElifWithoutBody.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_if_relational_condition(self):
        jmp_address = Integer(6).to_byte_array(min_length=1, signed=True)

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

        path = '%s/boa3_test/test_sc/if_test/RelationalCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_if_multiple_branches(self):
        twenty = Integer(20).to_byte_array()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH0
            + Opcode.LT
            + Opcode.JMPIFNOT       # if arg0 < 0
            + Integer(6).to_byte_array(min_length=1)
                + Opcode.PUSH0          # a = 0
                + Opcode.STLOC0
            + Opcode.JMP
            + Integer(35).to_byte_array(min_length=1)
                + Opcode.LDARG0
                + Opcode.PUSH5
            + Opcode.LT
            + Opcode.JMPIFNOT       # elif arg0 < 5
            + Integer(6).to_byte_array(min_length=1)
                + Opcode.PUSH5          # a = 5
                + Opcode.STLOC0
            + Opcode.JMP
            + Integer(26).to_byte_array(min_length=1)
                + Opcode.LDARG0
                + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIFNOT       # elif arg0 < 10
            + Integer(6).to_byte_array(min_length=1)
                + Opcode.PUSH10         # a = 10
                + Opcode.STLOC0
            + Opcode.JMP
            + Integer(17).to_byte_array(min_length=1)
            + Opcode.LDARG0
            + Opcode.PUSH15
            + Opcode.LT
            + Opcode.JMPIFNOT       # elif arg0 < 15
            + Integer(6).to_byte_array(min_length=1)
                + Opcode.PUSH15         # a = 15
                + Opcode.STLOC0
            + Opcode.JMP            # else
            + Integer(8).to_byte_array(min_length=1)
                + Opcode.PUSHDATA1      # a = 20
                + Integer(len(twenty)).to_byte_array()
                + twenty
                + Opcode.CONVERT
                + Type.int.stack_item
                + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/if_test/MultipleBranches.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_if_expression_variable_condition(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # a = 2 if arg0 else 3
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.PUSH2      # 2
            + Opcode.JMP        # else
            + Integer(3).to_byte_array(min_length=1, signed=True)
                + Opcode.PUSH3      # 3
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/if_test/IfExpVariableCondition.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_if_expression_without_else_branch(self):
        path = '%s/boa3_test/test_sc/if_test/IfExpWithoutElse.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_if_expression_mismatched_types(self):
        path = '%s/boa3_test/test_sc/if_test/MismatchedIfExp.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
