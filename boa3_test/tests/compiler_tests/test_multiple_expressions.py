from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestMultipleExpressions(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc'

    def test_multiple_arithmetic_expressions_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x02'
            + Opcode.PUSH1      # d = 1
            + Opcode.STLOC0
            + Opcode.PUSH2      # e = 2
            + Opcode.STLOC1
            + Opcode.LDARG0     # c = a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STLOC2
            + Opcode.LDLOC2     # return c
            + Opcode.RET
        )

        path = self.get_contract_path('arithmetic_test', 'MultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    async def test_multiple_arithmetic_expressions(self):
        await self.set_up_contract('arithmetic_test', 'MultipleExpressionsInLine.py')

        result, _ = await self.call('Main', [1, 2], return_type=int)
        self.assertEqual(3, result)
        result, _ = await self.call('Main', [5, -7], return_type=int)
        self.assertEqual(-2, result)

    def test_multiple_relational_expressions_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x02'
            + Opcode.LDARG0     # is_equal = a == b
            + Opcode.LDARG1
            + Opcode.NUMEQUAL
            + Opcode.STLOC0
            + Opcode.LDARG0     # is_greater = a > b
            + Opcode.LDARG1
            + Opcode.GT
            + Opcode.STLOC1
            + Opcode.LDARG0     # is_less = a < b
            + Opcode.LDARG1
            + Opcode.LT
            + Opcode.STLOC2
            + Opcode.LDLOC0     # return not is_equal
            + Opcode.NOT
            + Opcode.RET
        )

        path = self.get_contract_path('relational_test', 'MultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    async def test_multiple_relational_expressions(self):
        await self.set_up_contract('relational_test', 'MultipleExpressionsInLine.py')

        result, _ = await self.call('Main', [1, 2], return_type=bool)
        self.assertEqual(True, result)
        result, _ = await self.call('Main', [5, -7], return_type=bool)
        self.assertEqual(True, result)
        result, _ = await self.call('Main', [-4, -4], return_type=bool)
        self.assertEqual(False, result)

    def test_multiple_logic_expressions_compile(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x03'
            + Opcode.LDARG0     # a1 = a and b
            + Opcode.LDARG1
            + Opcode.BOOLAND
            + Opcode.STLOC0
            + Opcode.LDARG1     # b1 = b and c
            + Opcode.LDARG2
            + Opcode.BOOLAND
            + Opcode.STLOC1
            + Opcode.LDARG0     # c1 = a or c
            + Opcode.LDARG2
            + Opcode.BOOLOR
            + Opcode.STLOC2
            + Opcode.LDLOC0     # return a1 and not b1 and c1
            + Opcode.LDLOC1
            + Opcode.NOT
            + Opcode.BOOLAND
            + Opcode.LDLOC2
            + Opcode.BOOLAND
            + Opcode.RET
        )

        path = self.get_contract_path('logical_test', 'LogicMultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    async def test_multiple_logic_expressions(self):
        await self.set_up_contract('logical_test', 'LogicMultipleExpressionsInLine.py')

        result, _ = await self.call('Main', [True, False, False], return_type=bool)
        self.assertEqual(False, result)
        result, _ = await self.call('Main', [False, True, False], return_type=bool)
        self.assertEqual(False, result)
        result, _ = await self.call('Main', [False, False, False], return_type=bool)
        self.assertEqual(False, result)
        result, _ = await self.call('Main', [True, True, False], return_type=bool)
        self.assertEqual(True, result)

    def test_multiple_tuple_expressions_compile(self):
        a = String('a').to_bytes()
        b = String('b').to_bytes()
        c = String('c').to_bytes()
        d = String('d').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x01'
            + Opcode.PUSHDATA1  # items2 = ('a', 'b', 'c', 'd')
            + Integer(len(d)).to_byte_array() + d
            + Opcode.PUSHDATA1
            + Integer(len(c)).to_byte_array() + c
            + Opcode.PUSHDATA1
            + Integer(len(b)).to_byte_array() + b
            + Opcode.PUSHDATA1
            + Integer(len(a)).to_byte_array() + a
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.STLOC0     # items2 = array
            + Opcode.LDARG0     # value = items1[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.STLOC1
            + Opcode.LDLOC1     # count = value + len(items2)
            + Opcode.LDLOC0
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.STLOC2
            + Opcode.LDLOC2     # return count
            + Opcode.RET
        )

        path = self.get_contract_path('tuple_test', 'MultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    async def test_multiple_tuple_expressions(self):
        await self.set_up_contract('tuple_test', 'MultipleExpressionsInLine.py')

        result, _ = await self.call('Main', [[1, 2]], return_type=int)
        self.assertEqual(5, result)
        result, _ = await self.call('Main', [[-5, -7]], return_type=int)
        self.assertEqual(-1, result)

    def test_multiple_list_expressions_compile(self):
        one = String('1').to_bytes()
        four = String('4').to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x01'
            + Opcode.PUSHDATA1  # items2 = [False, '1', 2, 3, '4']
            + Integer(len(four)).to_byte_array() + four
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSHDATA1
            + Integer(len(one)).to_byte_array() + one
            + Opcode.PUSHF
            + Opcode.PUSH5
            + Opcode.PACK
            + Opcode.STLOC0     # items2 = array
            + Opcode.LDARG0     # value = items1[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.STLOC1
            + Opcode.LDLOC1     # count = value + len(items2)
            + Opcode.LDLOC0
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.STLOC2
            + Opcode.LDLOC2     # return count
            + Opcode.RET
        )

        path = self.get_contract_path('list_test', 'ListMultipleExpressionsInLine.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    async def test_multiple_list_expressions(self):
        await self.set_up_contract('list_test', 'ListMultipleExpressionsInLine.py')

        result, _ = await self.call('Main', [[2, 1]], return_type=int)
        self.assertEqual(7, result)
        result, _ = await self.call('Main', [[-7, 5]], return_type=int)
        self.assertEqual(-2, result)

