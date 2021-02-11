from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestWhile(BoaTest):

    default_folder: str = 'test_sc/while_test'

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

        path = self.get_contract_path('ConstantCondition.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(0, result)

    def test_while_variable_condition(self):
        jmpif_address = Integer(12).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-11).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # condition = a < value
            + Opcode.LDARG0
            + Opcode.LT
            + Opcode.STLOC1
            + Opcode.JMP        # begin while
            + jmpif_address
            + Opcode.LDLOC0     # a = a + 2
            + Opcode.PUSH2
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # condition = a < value * 2
            + Opcode.LDARG0
            + Opcode.PUSH2
            + Opcode.MUL
            + Opcode.LT
            + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.JMPIF      # end while arg0
            + jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('VariableCondition.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', -2)
        self.assertEqual(0, result)
        result = self.run_smart_contract(engine, path, 'Main', 5)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', 8)
        self.assertEqual(16, result)

    def test_while_mismatched_type_condition(self):
        path = self.get_contract_path('MismatchedTypeCondition.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_while_no_condition(self):
        path = self.get_contract_path('NoCondition.py')

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_nested_while(self):
        outer_jmpif_address = Integer(23).to_byte_array(min_length=1, signed=True)
        outer_jmp_address = Integer(-26).to_byte_array(min_length=1, signed=True)

        inner_jmpif_address = Integer(6).to_byte_array(min_length=1, signed=True)
        inner_jmp_address = Integer(-9).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH0      # c = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # d = c
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
            + Opcode.LDLOC1     # while d % 10 < 5
            + Opcode.PUSH10
            + Opcode.MOD
            + Opcode.PUSH5
            + Opcode.LT
            + Opcode.JMPIF      # end inner while arg1
            + inner_jmp_address
            + Opcode.LDLOC0     # c = c + d
            + Opcode.LDLOC1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # while c % 3 < 2
            + Opcode.PUSH3
            + Opcode.MOD
            + Opcode.PUSH2
            + Opcode.LT
            + Opcode.JMPIF      # end outer while arg0
            + outer_jmp_address
            + Opcode.LDLOC0     # return c
            + Opcode.RET
        )

        path = self.get_contract_path('NestedWhile.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(8, result)

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

        path = self.get_contract_path('WhileElse.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(1, result)

    def test_while_relational_condition(self):
        jmpif_address = Integer(10).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-11).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
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

        path = self.get_contract_path('RelationalCondition.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(20, result)

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

        path = self.get_contract_path('MultipleRelationalCondition.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', '', 1)
        self.assertEqual(0, result)
        result = self.run_smart_contract(engine, path, 'Main', '', 10)
        self.assertEqual(0, result)
        result = self.run_smart_contract(engine, path, 'Main', '', 100)
        self.assertEqual(20, result)

    def test_while_continue(self):
        jmpif_address = Integer(31).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-33).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # b = 0
            + Opcode.STLOC1
            + Opcode.PUSH15     # sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.JMP        # begin while
            + jmpif_address
            + Opcode.LDLOC2     # x = sequence[a]
            + Opcode.LDLOC0
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
            + Opcode.LDLOC0     # a += 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC3     # if x % 5 != 0
            + Opcode.PUSH5
            + Opcode.MOD
            + Opcode.PUSH0
            + Opcode.NUMNOTEQUAL
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.JMP        # continue
            + Integer(6).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC1     # b += x
            + Opcode.LDLOC3
            + Opcode.ADD
            + Opcode.STLOC1
            + Opcode.LDLOC0
            + Opcode.LDLOC2
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end while a < len(sequence)
            + jmp_address
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )

        path = self.get_contract_path('WhileContinue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(20, result)

    def test_while_break(self):
        jmpif_address = Integer(35).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-37).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # b = 0
            + Opcode.STLOC1
            + Opcode.PUSH15     # sequence = (3, 5, 15)
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.JMP        # begin while
            + jmpif_address
            + Opcode.LDLOC2         # x = sequence[a]
            + Opcode.LDLOC0
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
            + Opcode.LDLOC0         # a += 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC3         # if x % 5 == 0
            + Opcode.PUSH5
            + Opcode.MOD
            + Opcode.PUSH0
            + Opcode.NUMEQUAL
            + Opcode.JMPIFNOT
            + Integer(8).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC1             # b += x
            + Opcode.LDLOC3
            + Opcode.ADD
            + Opcode.STLOC1
            + Opcode.JMP                # break
            + Integer(12).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC1         # b += 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC1
            + Opcode.LDLOC0
            + Opcode.LDLOC2
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF      # end while a < len(sequence)
            + jmp_address
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )

        path = self.get_contract_path('WhileBreak.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(6, result)

    def test_boa2_while_test(self):
        path = self.get_contract_path('WhileBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(24, result)

    def test_boa2_while_test1(self):
        path = self.get_contract_path('WhileBoa2Test1.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(6, result)

    def test_boa2_while_test2(self):
        path = self.get_contract_path('WhileBoa2Test2.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(6, result)
