from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3_test.tests import boatestcase


class TestFor(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/for_test'

    def test_for_tuple_condition_compile(self):
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

        output, _ = self.assertCompile('TupleCondition.py')
        self.assertEqual(expected_output, output)

    async def test_for_tuple_condition_run(self):
        await self.set_up_contract('TupleCondition.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(23, result)

    async def test_for_string_condition(self):
        await self.set_up_contract('StringCondition.py')

        result, _ = await self.call('Main', [], return_type=str)
        self.assertEqual('5', result)

    def test_for_iterator_condition_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        call_method_address = Integer(39).to_byte_array(min_length=1, signed=True)
        jmpif_address = Integer(20).to_byte_array(min_length=1, signed=True)
        jmp_address = Integer(-24).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT
            + b'\x03'
            + b'\x00'
            + Opcode.CALL       # value = get_iterator()
            + call_method_address
            + Opcode.STLOC0
            + Opcode.PUSH0      # a = 0
            + Opcode.STLOC1
            + Opcode.LDLOC0
            + Opcode.DUP        # don't iterate with indexes when using iterator
            + Opcode.JMP        # begin for
            + jmpif_address
            + Opcode.DUP           # x = iterator.value
            + Opcode.SYSCALL
            + Interop.IteratorValue.interop_method_hash
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Struct
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.CONVERT + StackItemType.Array
            + Opcode.STLOC2
            + Opcode.LDLOC1         # a = a + x
            + Opcode.LDLOC2
            + Opcode.ADD
            + Opcode.STLOC1
            + Opcode.DUP        # iterator.next
            + Opcode.SYSCALL
            + Interop.IteratorNext.interop_method_hash
            + Opcode.JMPIF      # end for
            + jmp_address
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC1     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('IteratorCondition.py')
        self.assertStartsWith(output, expected_output)

    async def test_for_iterator_condition_run(self):
        await self.set_up_contract('IteratorCondition.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(6, result)

    def test_for_mismatched_type_condition(self):
        path = self.get_contract_path('MismatchedTypeCondition.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_for_no_condition(self):
        path = self.get_contract_path('NoCondition.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    def test_nested_for_compile(self):
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

        output, _ = self.assertCompile('NestedFor.py')
        self.assertEqual(expected_output, output)

    async def test_nested_for_run(self):
        await self.set_up_contract('NestedFor.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(529, result)

    def test_for_else_compile(self):
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

        output, _ = self.assertCompile('ForElse.py')
        self.assertEqual(expected_output, output)

    async def test_for_else_run(self):
        await self.set_up_contract('ForElse.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(24, result)

    async def test_for_continue(self):
        await self.set_up_contract('ForContinue.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(20, result)

    async def test_for_break(self):
        await self.set_up_contract('ForBreak.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(6, result)

    async def test_for_break_else(self):
        await self.set_up_contract('ForBreakElse.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(6, result)

    def test_for_iterate_dict(self):
        path = self.get_contract_path('ForIterateDict.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_boa2_iteration_test(self):
        await self.set_up_contract('IterBoa2Test.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(18, result)

    async def test_boa2_iteration_test2(self):
        await self.set_up_contract('IterBoa2Test2.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(8, result)

    async def test_boa2_iteration_test3(self):
        await self.set_up_contract('IterBoa2Test3.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(7, result)

    def test_boa2_iteration_test4(self):
        path = self.get_contract_path('IterBoa2Test4.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_boa2_iteration_test5(self):
        await self.set_up_contract('IterBoa2Test5.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(51, result)

    async def test_boa2_iteration_test6(self):
        await self.set_up_contract('IterBoa2Test6.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(10, result)

    async def test_boa2_iteration_test7(self):
        await self.set_up_contract('IterBoa2Test7.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(12, result)

    async def test_boa2_iteration_test8(self):
        await self.set_up_contract('IterBoa2Test8.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(6, result)

    async def test_for_pass(self):
        output, _ = self.assertCompile('ForPass.py')
        self.assertIn(Opcode.NOP, output)

        await self.set_up_contract('ForPass.py')

        result, _ = await self.call('main', [], return_type=None)
        self.assertEqual(None, result)

    async def test_for_range(self):
        await self.compile_and_deploy('ForWithContractInterfaceCalled.py')
        await self.set_up_contract('ForWithContractInterface.py')

        result, _ = await self.call('main', [3], return_type=list)
        self.assertEqual([0, 0, 0], result)
