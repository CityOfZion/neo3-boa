from neo3.api import noderpc
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3_test.tests import boatestcase


class TestWhile(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/while_test'

    def test_while_constant_condition_compile(self):
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
            + Opcode.PUSHF
            + Opcode.JMPIF      # end while False
            + jmp_address
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('WhileConstantCondition.py')
        self.assertEqual(expected_output, output)

    async def test_while_constant_condition_run(self):
        await self.set_up_contract('WhileConstantCondition.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(0, result)

    def test_while_variable_condition_compile(self):
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

        output, _ = self.assertCompile('WhileVariableCondition.py')
        self.assertEqual(expected_output, output)

    async def test_while_variable_condition_run(self):
        await self.set_up_contract('WhileVariableCondition.py')

        result, _ = await self.call('Main', [-2], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('Main', [5], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('Main', [8], return_type=int)
        self.assertEqual(16, result)

    def test_while_mismatched_type_condition(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'WhileMismatchedTypeCondition.py')

    def test_while_no_condition(self):
        path = self.get_contract_path('WhileNoCondition.py')
        with self.assertRaises(SyntaxError):
            self.compile(path)

    async def test_nested_while(self):
        await self.set_up_contract('NestedWhile.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(8, result)

    def test_while_else_compile(self):
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
            + Opcode.PUSHF
            + Opcode.JMPIF      # end while False
            + jmp_address
            + Opcode.LDLOC0     # else
            + Opcode.PUSH1          # a = a + 1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )

        output, _ = self.assertCompile('WhileElse.py')
        self.assertEqual(expected_output, output)

    async def test_while_else_run(self):
        await self.set_up_contract('WhileElse.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(1, result)

    def test_while_relational_condition_compile(self):
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

        output, _ = self.assertCompile('WhileRelationalCondition.py')
        self.assertEqual(expected_output, output)

    async def test_while_relational_condition_run(self):
        await self.set_up_contract('WhileRelationalCondition.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(20, result)

    def test_while_multiple_relational_condition_compile(self):
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

        output, _ = self.assertCompile('WhileMultipleRelationalCondition.py')
        self.assertEqual(expected_output, output)

    async def test_while_multiple_relational_condition_run(self):
        await self.set_up_contract('WhileMultipleRelationalCondition.py')

        result, _ = await self.call('Main', ['', 1], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('Main', ['', 10], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('Main', ['', 100], return_type=int)
        self.assertEqual(20, result)

    async def test_while_continue(self):
        await self.set_up_contract('WhileContinue.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(20, result)

    async def test_while_break(self):
        await self.set_up_contract('WhileBreak.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(6, result)

    async def test_boa2_while_test(self):
        await self.set_up_contract('WhileBoa2Test.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(24, result)

    async def test_boa2_while_test1(self):
        await self.set_up_contract('WhileBoa2Test1.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(6, result)

    async def test_boa2_while_test2(self):
        await self.set_up_contract('WhileBoa2Test2.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(6, result)

    async def test_while_interop_condition(self):
        from dataclasses import dataclass

        @dataclass
        class NotifyTestEvent(boatestcase.BoaTestEvent):
            token: types.UInt160
            executing: types.UInt160
            fee_receiver: types.UInt160
            fee_amount: int

            @classmethod
            def from_untyped_notification(cls, n: noderpc.Notification):
                inner_args_types = tuple(cls.__annotations__.values())
                e = super().from_notification(n, tuple[inner_args_types])
                stack = e.state[0]
                return cls(e.contract, e.name, e.state, *stack)

        await self.set_up_contract('WhileWithInteropCondition.py', compile_if_found=True)

        result, events = await self.call('test_end_while_jump', [], return_type=bool)
        self.assertEqual(True, result)

        # test notifications inserted into the code for validating if the code flow is correct
        notifications = self.filter_events(events, notification_type=NotifyTestEvent)
        self.assertEqual(2, len(notifications))

        event = notifications[0]
        self.assertEqual(CONTRACT_HASHES.GAS_TOKEN, event.token)
        self.assertEqual(self.contract_hash, event.executing)
        self.assertEqual(types.UInt160.zero(), event.fee_receiver)
        self.assertEqual(10, event.fee_amount)

        event = notifications[1]
        self.assertEqual(CONTRACT_HASHES.NEO_TOKEN, event.token)
        self.assertEqual(self.contract_hash, event.executing)
        self.assertEqual(types.UInt160.zero(), event.fee_receiver)
        self.assertEqual(20, event.fee_amount)
