from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3_test.tests import boatestcase


class TestIf(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/if_test'

    def test_if_constant_condition_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.PUSHT
            + Opcode.JMPIFNOT   # if True
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2     # a = a + 2
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        output, _ = self.assertCompile('IfConstantCondition.py')
        self.assertEqual(expected_output, output)

    async def test_if_constant_condition(self):
        await self.set_up_contract('IfConstantCondition.py')

        result, _ = await self.call('Main', return_type=int)
        self.assertEqual(2, result)

    def test_if_variable_condition_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2      # a = a + 2
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        output, _ = self.assertCompile('IfVariableCondition.py')
        self.assertEqual(expected_output, output)

    async def test_if_variable_condition(self):
        await self.set_up_contract('IfVariableCondition.py')

        result, _ = await self.call('Main', [True], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('Main', [False], return_type=int)
        self.assertEqual(0, result)

    def test_if_no_condition(self):
        path = self.get_contract_path('IfWithoutCondition.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    def test_if_no_body(self):
        path = self.get_contract_path('IfWithoutBody.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    def test_nested_if_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x02'
            + Opcode.PUSH0      # c = 0
            + Opcode.STLOC0
            + Opcode.PUSH0      # d = c
            + Opcode.STLOC1
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(13).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2      # c = c + 2
            + Opcode.STLOC0
            + Opcode.LDARG1
            + Opcode.JMPIFNOT   # if arg1
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH3      # d = d + 3
            + Opcode.STLOC1
            + Opcode.PUSH2      # c = c + d
            + Opcode.LDLOC1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return c
            + Opcode.RET
        )
        output, _ = self.assertCompile('NestedIf.py')
        self.assertEqual(expected_output, output)

    async def test_nested_if(self):
        await self.set_up_contract('NestedIf.py')

        result, _ = await self.call('Main', [True, True], return_type=int)
        self.assertEqual(5, result)
        result, _ = await self.call('Main', [True, False], return_type=int)
        self.assertEqual(2, result)
        result, _ = await self.call('Main', [False, True], return_type=int)
        self.assertEqual(0, result)
        result, _ = await self.call('Main', [False, False], return_type=int)
        self.assertEqual(0, result)

    def test_if_else_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(6).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2      # a = a + 2
            + Opcode.STLOC0
            + Opcode.JMP        # else
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH10     # a = 10
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('IfElse.py')
        self.assertEqual(expected_output, output)

    async def test_if_else(self):
        await self.set_up_contract('IfElse.py')

        result, _ = await self.call('Main', [True], return_type=int)
        self.assertEqual(2, result)
        result, _ = await self.call('Main', [False], return_type=int)
        self.assertEqual(10, result)

    def test_else_no_body(self):
        path = self.get_contract_path('ElseWithoutBody.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    def test_if_elif_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC0
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if arg0
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.PUSH2      # a = a + 2
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
        output, _ = self.assertCompile('IfElif.py')
        self.assertEqual(expected_output, output)

    async def test_if_elif(self):
        await self.set_up_contract('IfElif.py')

        result, _ = await self.call('Main', [True], return_type=int)
        self.assertEqual(2, result)
        result, _ = await self.call('Main', [False], return_type=int)
        self.assertEqual(0, result)

    def test_elif_no_condition(self):
        path = self.get_contract_path('ElifWithoutCondition.py')
        with self.assertRaises(SyntaxError):
            output = self.compile(path)

    def test_elif_no_body(self):
        path = self.get_contract_path('ElifWithoutBody.py')
        with self.assertRaises(SyntaxError):
            output = self.compile(path)

    def test_if_relational_condition_compile(self):
        jmp_address = Integer(4).to_byte_array(min_length=1, signed=True)

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
            + Opcode.PUSH2      # a = a + 2
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('IfRelationalCondition.py')
        self.assertEqual(expected_output, output)

    async def test_if_relational_condition(self):
        await self.set_up_contract('IfRelationalCondition.py')

        result, _ = await self.call('Main', [5], return_type=int)
        self.assertEqual(2, result)
        result, _ = await self.call('Main', [10], return_type=int)
        self.assertEqual(0, result)

    def test_if_multiple_branches_compile(self):
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
            + Opcode.PUSH0              # a = 0
            + Opcode.STLOC0
            + Opcode.JMP
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.LDARG0
            + Opcode.PUSH5
            + Opcode.LT
            + Opcode.JMPIFNOT       # elif arg0 < 5
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.PUSH5              # a = 5
            + Opcode.STLOC0
            + Opcode.JMP
            + Integer(23).to_byte_array(min_length=1)
            + Opcode.LDARG0
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIFNOT       # elif arg0 < 10
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.PUSH10             # a = 10
            + Opcode.STLOC0
            + Opcode.JMP
            + Integer(14).to_byte_array(min_length=1)
            + Opcode.LDARG0
            + Opcode.PUSH15
            + Opcode.LT
            + Opcode.JMPIFNOT       # elif arg0 < 15
            + Integer(6).to_byte_array(min_length=1)
            + Opcode.PUSH15             # a = 15
            + Opcode.STLOC0
            + Opcode.JMP            # else
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.PUSHINT8 + twenty  # a = 20
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('IfMultipleBranches.py')
        self.assertEqual(expected_output, output)

    async def test_if_multiple_branches(self):
        await self.set_up_contract('IfMultipleBranches.py')

        result, _ = await self.call('Main', [-10], return_type=int)
        self.assertEqual(0, result)
        result, _ = await self.call('Main', [2], return_type=int)
        self.assertEqual(5, result)
        result, _ = await self.call('Main', [7], return_type=int)
        self.assertEqual(10, result)
        result, _ = await self.call('Main', [13], return_type=int)
        self.assertEqual(15, result)
        result, _ = await self.call('Main', [17], return_type=int)
        self.assertEqual(20, result)
        result, _ = await self.call('Main', [23], return_type=int)
        self.assertEqual(20, result)

    def test_if_expression_variable_condition_compile(self):
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

        output, _ = self.assertCompile('IfExpVariableCondition.py')
        self.assertEqual(expected_output, output)

    async def test_if_expression_variable_condition(self):
        await self.set_up_contract('IfExpVariableCondition.py')

        result, _ = await self.call('Main', [True], return_type=int)
        self.assertEqual(2, result)
        result, _ = await self.call('Main', [False], return_type=int)
        self.assertEqual(3, result)

    def test_if_expression_without_else_branch(self):
        path = self.get_contract_path('IfExpWithoutElse.py')
        with self.assertRaises(SyntaxError):
            output = self.compile(path)

    def test_if_expression_mismatched_types_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # a = 2 if condition else None
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2      # 2
            + Opcode.JMP        # else
            + Integer(3).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSHNULL   # None
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('IfMismatchedIfExp.py')
        self.assertEqual(expected_output, output)

    async def test_if_expression_mismatched_types(self):
        await self.set_up_contract('IfMismatchedIfExp.py')

        result, _ = await self.call('Main', [True], return_type=int)
        self.assertEqual(2, result)
        result, _ = await self.call('Main', [False], return_type=None)
        self.assertEqual(None, result)

    async def test_inner_if_else(self):
        await self.set_up_contract('InnerIfElse.py')

        result, _ = await self.call('main', [4, 3, 2, 1], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', [4, 3, 1, 2], return_type=int)
        self.assertEqual(8, result)

        result, _ = await self.call('main', [4, 1, 2, 3], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('main', [1, 2, 4, 3], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('main', [1, 2, 3, 4], return_type=int)
        self.assertEqual(11, result)

        result, _ = await self.call('main', [1, 3, 2, 4], return_type=int)
        self.assertEqual(22, result)

    async def test_if_is_instance_condition(self):
        await self.set_up_contract('IfIsInstanceCondition.py')

        result, _ = await self.call('example', [4], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('example', ['123'], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('example', [-70], return_type=int)
        self.assertEqual(-70, result)

        result, _ = await self.call('example', [True], return_type=int)
        self.assertEqual(-1, result)

    async def test_if_else_is_instance_condition(self):
        await self.set_up_contract('IfElseIsInstanceCondition.py')

        result, _ = await self.call('example', [4], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('example', ['123'], return_type=int)
        self.assertEqual(-1, result)

        result, _ = await self.call('example', [-70], return_type=int)
        self.assertEqual(-70, result)

        result, _ = await self.call('example', [True], return_type=int)
        self.assertEqual(-1, result)

    async def test_if_else_is_instance_condition_with_union_variable(self):
        await self.set_up_contract('IfElseIsInstanceConditionWithUnionVariable.py')

        result, _ = await self.call('example', [4], return_type=bytes)
        self.assertEqual(b'\x04', result)

        result, _ = await self.call('example', ['123'], return_type=bytes)
        self.assertEqual(b'123', result)

        result, _ = await self.call('example', [70], return_type=bytes)
        self.assertEqual(Integer(70).to_byte_array(), result)

        result, _ = await self.call('example', [True], return_type=bytes)
        self.assertEqual(b'\x01', result)

    async def test_if_else_multiple_is_instance_condition_with_union_variable(self):
        await self.set_up_contract('IfElseMultipleIsInstanceConditionWithUnionVariable.py')

        result, _ = await self.call('example', [4], return_type=int)
        self.assertEqual(16, result)

        result, _ = await self.call('example', [[b'123456', b'789']], return_type=int)
        self.assertEqual(6, result)

        result, _ = await self.call('example', [-70], return_type=int)
        self.assertEqual(4900, result)

        result, _ = await self.call('example', [[]], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('example', [b'True'], return_type=int)
        self.assertEqual(4, result)

    async def test_variable_in_if_scopes(self):
        await self.set_up_contract('IfVariablesInIfScopes.py')

        result, _ = await self.call('main', [1], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [2], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [3], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [4], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [5], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [6], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [7], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [8], return_type=bool)
        self.assertEqual(False, result)

    async def test_boa2_compare_test0int(self):
        await self.set_up_contract('IfCompareBoa2Test0int.py')

        result, _ = await self.call('main', [2, 4], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [4, 2], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', [2, 2], return_type=int)
        self.assertEqual(2, result)

    async def test_boa2_compare_test0str(self):
        await self.set_up_contract('IfCompareBoa2Test0str.py')

        result, _ = await self.call('main', ['b', 'a'], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', ['a', 'b'], return_type=int)
        self.assertEqual(2, result)

    async def test_boa2_compare_test1(self):
        await self.set_up_contract('IfCompareBoa2Test1.py')

        result, _ = await self.call('main', [1, 2, 3, 4], return_type=int)
        self.assertEqual(11, result)

        result, _ = await self.call('main', [1, 2, 4, 3], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('main', [1, 4, 3, 5], return_type=int)
        self.assertEqual(22, result)

        result, _ = await self.call('main', [4, 1, 5, 3], return_type=int)
        self.assertEqual(3, result)

        result, _ = await self.call('main', [9, 1, 3, 5], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('main', [9, 5, 3, 5], return_type=int)
        self.assertEqual(8, result)

    async def test_boa2_compare_test2(self):
        await self.set_up_contract('IfCompareBoa2Test2.py')

        result, _ = await self.call('main', [2, 2], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [2, 3], return_type=bool)
        self.assertEqual(False, result)

    async def test_boa2_op_call_test(self):
        await self.set_up_contract('IfOpCallBoa2Test.py')

        result, _ = await self.call('main', ['omin', 4, 4], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', ['omin', -4, 4], return_type=int)
        self.assertEqual(-4, result)

        result, _ = await self.call('main', ['omin', 16, 0], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', ['omax', 4, 4], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', ['omax', -4, 4], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', ['omax', 16, 0], return_type=int)
        self.assertEqual(16, result)

        from boa3.internal.neo.cryptography import sha256, hash160
        from boa3.internal.neo.vm.type.String import String
        result, _ = await self.call('main', ['sha256', b'abc', 4], return_type=bytes)
        self.assertEqual(sha256(String('abc').to_bytes()), result)

        result, _ = await self.call('main', ['hash160', b'abc', 4], return_type=bytes)
        self.assertEqual(hash160(String('abc').to_bytes()), result)

    async def test_boa2_test_many_elif(self):
        await self.set_up_contract('IfTestManyElifBoa2.py')

        result, _ = await self.call('main', [1], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('main', [3], return_type=int)
        self.assertEqual(4, result)

        result, _ = await self.call('main', [16], return_type=int)
        self.assertEqual(17, result)

        result, _ = await self.call('main', [22], return_type=int)
        self.assertEqual(-1, result)

    async def test_if_with_inner_while(self):
        await self.set_up_contract('IfWithInnerWhile.py')

        result, _ = await self.call('Main', [True], return_type=str)
        self.assertEqual('{[]}', result)

        result, _ = await self.call('Main', [False], return_type=str)
        self.assertEqual('{[value1,value2,value3]}', result)

    async def test_if_with_inner_for(self):
        await self.set_up_contract('IfWithInnerFor.py')

        result, _ = await self.call('Main', [True], return_type=str)
        self.assertEqual('{[]}', result)

        result, _ = await self.call('Main', [False], return_type=str)
        self.assertEqual('{[value1,value2,value3]}', result)

    async def test_if_implicit_boolean(self):
        await self.set_up_contract('IfImplicitBoolean.py')

        result, _ = await self.call('main', [1], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [0], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', ['unit_test'], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [''], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [b'unit test'], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [b''], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [[1, 2, 3, 4]], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [[]], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', [{'a': 1, 'b': 2}], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('main', [{}], return_type=bool)
        self.assertEqual(False, result)

    async def test_if_implicit_boolean_literal(self):
        await self.set_up_contract('IfImplicitBooleanLiteral.py')

        result, _ = await self.call('main', return_type=int)
        self.assertEqual(4, result)

    def test_if_pass_compile(self):
        expected_output = Opcode.NOP

        output, _ = self.assertCompile('IfPass.py')
        self.assertIn(expected_output, output)

    async def test_if_pass(self):
        await self.set_up_contract('IfPass.py')

        result, _ = await self.call('main', [True], return_type=int)
        self.assertEqual(0, result)

    def test_else_pass_compile(self):
        expected_output = Opcode.NOP

        output, _ = self.assertCompile('ElsePass.py')
        self.assertIn(expected_output, output)

    async def test_else_pass(self):
        await self.set_up_contract('ElsePass.py')

        result, _ = await self.call('main', [True], return_type=int)
        self.assertEqual(5, result)
        result, _ = await self.call('main', [False], return_type=int)
        self.assertEqual(0, result)

    def test_if_else_pass_compile(self):
        output, _ = self.assertCompile('IfElsePass.py')
        n_nop = 0
        for byte_value in output:
            if byte_value == int.from_bytes(Opcode.NOP.value, 'little'):
                n_nop += 1
        self.assertEqual(n_nop, 2)

    async def test_if_else_pass(self):
        await self.set_up_contract('IfElsePass.py')

        result, _ = await self.call('main', [True], return_type=int)
        self.assertEqual(0, result)

    async def test_if_is_none(self):
        await self.set_up_contract('IfIsNone.py')

        result, _ = await self.call('main', [123], return_type=bool)
        self.assertEqual(False, result)
        result, _ = await self.call('main', [None], return_type=bool)
        self.assertEqual(True, result)

    async def test_if_is_not_none(self):
        await self.set_up_contract('IfIsNotNone.py')

        result, _ = await self.call('main', [123], return_type=bool)
        self.assertEqual(True, result)
        result, _ = await self.call('main', [None], return_type=bool)
        self.assertEqual(False, result)

    async def test_if_is_none_type_check(self):
        await self.set_up_contract('IfIsNoneTypeCheck.py')

        test_input = bytes(20)
        result, _ = await self.call('main', [test_input], return_type=bytes)
        self.assertEqual(test_input, result)

        result, _ = await self.call('main', [None], return_type=None)
        self.assertEqual(None, result)
