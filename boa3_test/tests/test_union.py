from boa3.boa3 import Boa3
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestUnion(BoaTest):

    def test_union_return(self):
        integer = Integer(42).to_byte_array()
        string = String('42').to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.JMPIFNOT
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1  # return 42
            + Integer(len(integer)).to_byte_array(min_length=1)
            + integer
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.RET
            + Opcode.PUSHDATA1  # a = b'\x01\x02\x03'
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/union_test/UnionReturn.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'main', True)
        self.assertEqual(42, result)

        result = self.run_smart_contract(engine, path, 'main', False)
        self.assertEqual('42', result)

    def test_union_variable_reassign(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH2      # a = 2
            + Opcode.STLOC0
            + Opcode.PUSH2      # b = a
            + Opcode.STLOC1
            + Opcode.PUSH2      # c = [a, b]
            + Opcode.PUSH2
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.STLOC2
            + Opcode.LDLOC2     # b = c
            + Opcode.STLOC1
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/union_test/UnionVariableReassign.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_union_variable_argument(self):
        path = '%s/boa3_test/test_sc/union_test/UnionVariableArgument.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'main', 'unittest')
        self.assertEqual('string', result)

        result = self.run_smart_contract(engine, path, 'main', False)
        self.assertEqual('boolean', result)

    def test_union_isinstance_validation(self):
        path = '%s/boa3_test/test_sc/union_test/UnionIsInstanceValidation.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'main', 'unittest')
        self.assertEqual('unittest', result)

        result = self.run_smart_contract(engine, path, 'main', False)
        self.assertEqual('boolean', result)

    def test_union_int_none(self):
        path = '%s/boa3_test/test_sc/union_test/UnionIntNone.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(42, result)
