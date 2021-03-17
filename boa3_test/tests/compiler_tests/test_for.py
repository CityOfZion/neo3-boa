from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestFor(BoaTest):

    default_folder: str = 'test_sc/for_test'

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

        path = self.get_contract_path('TupleCondition.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(23, result)

    def test_for_string_condition(self):
        path = self.get_contract_path('StringCondition.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('5', result)

    def test_for_mismatched_type_condition(self):
        path = self.get_contract_path('MismatchedTypeCondition.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_for_no_condition(self):
        path = self.get_contract_path('NoCondition.py')

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

        path = self.get_contract_path('NestedFor.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(529, result)

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

        path = self.get_contract_path('ForElse.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(24, result)

    def test_for_continue(self):
        jmpif_address = Integer(28).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-31).to_byte_array(min_length=1, signed=True)

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
            + Opcode.LDLOC2         # if x % 5 != 0
            + Opcode.PUSH5
            + Opcode.MOD
            + Opcode.PUSH0
            + Opcode.NUMNOTEQUAL
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.JMP                # continue
            + Integer(6).to_byte_array(min_length=1, signed=True)
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

        path = self.get_contract_path('ForContinue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(20, result)

    def test_for_break(self):
        jmpif_address = Integer(32).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-35).to_byte_array(min_length=1, signed=True)

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
            + Opcode.LDLOC2         # if x % 5 != 0
            + Opcode.PUSH5
            + Opcode.MOD
            + Opcode.PUSH0
            + Opcode.NUMEQUAL
            + Opcode.JMPIFNOT
            + Integer(8).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0             # a += x
            + Opcode.LDLOC2
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.JMP                # break
            + Integer(14).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0         # a += 1
            + Opcode.PUSH1
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
        path = self.get_contract_path('ForBreak.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(6, result)

    def test_for_break_else(self):
        jmpif_address = Integer(33).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-36).to_byte_array(min_length=1, signed=True)

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
            + Opcode.LDLOC2         # if x % 5 == 0
            + Opcode.PUSH5
            + Opcode.MOD
            + Opcode.PUSH0
            + Opcode.NUMEQUAL
            + Opcode.JMPIFNOT
            + Integer(9).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0             # a += x
            + Opcode.LDLOC2
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.PUSH1
            + Opcode.JMP                # break
            + Integer(15).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0         # a += 1
            + Opcode.PUSH1
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
            + Opcode.PUSH0
            + Opcode.REVERSE3
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.JMPIF
            + Integer(4).to_byte_array(signed=True)
            + Opcode.PUSHM1         # a = -1
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        path = self.get_contract_path('ForBreakElse.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(6, result)

    def test_for_iterate_dict(self):
        path = self.get_contract_path('ForIterateDict.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_boa2_iteration_test(self):
        path = self.get_contract_path('IterBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(18, result)

    def test_boa2_iteration_test2(self):
        path = self.get_contract_path('IterBoa2Test2.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(8, result)

    def test_boa2_iteration_test3(self):
        path = self.get_contract_path('IterBoa2Test3.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(7, result)

    def test_boa2_iteration_test4(self):
        path = self.get_contract_path('IterBoa2Test4.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_boa2_iteration_test5(self):
        path = self.get_contract_path('IterBoa2Test5.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(51, result)

    def test_boa2_iteration_test6(self):
        path = self.get_contract_path('IterBoa2Test6.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(10, result)

    def test_boa2_iteration_test7(self):
        path = self.get_contract_path('IterBoa2Test7.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(12, result)

    def test_boa2_iteration_test8(self):
        path = self.get_contract_path('IterBoa2Test8.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(6, result)
