from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestUnion(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/union_test'

    def test_union_return_compile(self):
        integer = Integer(42).to_byte_array()
        string = String('42').to_bytes()
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHINT8 + integer  # return 42
            + Opcode.RET
            + Opcode.PUSHDATA1  # a = b'\x01\x02\x03'
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.RET        # return
        )

        output, _ = self.assertCompile('UnionReturn.py')
        self.assertEqual(expected_output, output)

    async def test_union_return(self):
        await self.set_up_contract('UnionReturn.py')

        result, _ = await self.call('main', [True], return_type=int)
        self.assertEqual(42, result)
        result, _ = await self.call('main', [False], return_type=str)
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

        output, _ = self.assertCompile('UnionVariableReassign.py')
        self.assertEqual(expected_output, output)

    async def test_union_variable_argument(self):
        await self.set_up_contract('UnionVariableArgument.py')

        result, _ = await self.call('main', ['unittest'], return_type=str)
        self.assertEqual('string', result)
        result, _ = await self.call('main', [False], return_type=str)
        self.assertEqual('boolean', result)

    async def test_union_isinstance_validation(self):
        await self.set_up_contract('UnionIsInstanceValidation.py')

        result, _ = await self.call('main', ['unittest'], return_type=str)
        self.assertEqual('unittest', result)
        result, _ = await self.call('main', [False], return_type=str)
        self.assertEqual('boolean', result)

    async def test_union_int_none(self):
        await self.set_up_contract('UnionIntNone.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(42, result)
