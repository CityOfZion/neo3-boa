from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests import boatestcase


class TestOptional(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/optional_test'

    async def test_optional_return(self):
        await self.set_up_contract('OptionalReturn.py')

        result, _ = await self.call('main', [1], return_type=str)
        self.assertEqual('str', result)

        result, _ = await self.call('main', [2], return_type=int)
        self.assertEqual(123, result)

        result, _ = await self.call('main', [3], return_type=None)
        self.assertIsNone(result)

        result, _ = await self.call('union_test', [1], return_type=str)
        self.assertEqual('str', result)

        result, _ = await self.call('union_test', [2], return_type=int)
        self.assertEqual(123, result)

        result, _ = await self.call('union_test', [3], return_type=None)
        self.assertIsNone(result)

    def test_optional_variable_reassign(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH2  # a = 2
            + Opcode.STLOC0
            + Opcode.PUSH2  # b = a
            + Opcode.STLOC1
            + Opcode.PUSHNULL  # c = None
            + Opcode.STLOC2
            + Opcode.LDLOC2  # b = c
            + Opcode.STLOC1
            + Opcode.RET  # return
        )

        output, _ = self.assertCompile('OptionalVariableReassign')
        self.assertEqual(expected_output, output)

    async def test_optional_variable_argument(self):
        await self.set_up_contract('OptionalVariableArgument.py')

        result, _ = await self.call('main', ['unittest'], return_type=str)
        self.assertEqual('string', result)

        result, _ = await self.call('main', [123], return_type=str)
        self.assertEqual('int', result)

        result, _ = await self.call('main', [None], return_type=str)
        self.assertEqual('None', result)

        result, _ = await self.call('union_test', ['unittest'], return_type=str)
        self.assertEqual('string', result)

        result, _ = await self.call('union_test', [123], return_type=str)
        self.assertEqual('int', result)

        result, _ = await self.call('union_test', [None], return_type=str)
        self.assertEqual('None', result)

    async def test_optional_isinstance_validation(self):
        await self.set_up_contract('OptionalIsInstanceValidation.py')

        result, _ = await self.call('main', ['unittest'], return_type=str)
        self.assertEqual('unittest', result)

        result, _ = await self.call('main', [123], return_type=str)
        self.assertEqual('int', result)

        result, _ = await self.call('main', [None], return_type=str)
        self.assertEqual('None', result)

        result, _ = await self.call('union_test', ['unittest'], return_type=str)
        self.assertEqual('unittest', result)

        result, _ = await self.call('union_test', [123], return_type=str)
        self.assertEqual('int', result)

        result, _ = await self.call('union_test', [None], return_type=str)
        self.assertEqual('None', result)

    def test_optional_inside_dict_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0  # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('OptionalArgumentInsideDict.py')
        self.assertEqual(expected_output, output)

    async def test_optional_inside_dict(self):
        await self.set_up_contract('OptionalArgumentInsideDict.py')

        result, _ = await self.call('main', [{}], return_type=dict)
        self.assertEqual({}, result)
