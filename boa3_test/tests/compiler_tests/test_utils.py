import hashlib
from typing import Self

from boaconstructor import storage
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.wallet import account

from boa3.internal.exception import CompilerError
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3_test.tests import boatestcase


class TestUtils(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/utils_test'
    account: account.Account
    ecpoint_init = (
            Opcode.DUP
            + Opcode.ISNULL
            + Opcode.NOT
            + Opcode.JMPIFNOT
            + Integer(11).to_byte_array(min_length=1)
            + Opcode.CONVERT + Type.bytes.stack_item
            + Opcode.DUP
            + Opcode.SIZE
            + Opcode.PUSHINT8 + Integer(33).to_byte_array(signed=True)
            + Opcode.NUMEQUAL
            + Opcode.JMPIF + Integer(3).to_byte_array()
            + Opcode.THROW
    )

    @classmethod
    def setupTestCase(cls):
        cls.account = cls.node.wallet.account_new(label='test')
        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account.script_hash, 100, 8)

    async def test_call_contract(self):
        await self.set_up_contract('CallScriptHash.py')

        invalid_contract = types.UInt160.zero()
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [invalid_contract, 'add', [1, 2]], return_type=int)

        self.assertRegex(str(context.exception), f'called contract {invalid_contract} not found')

        call_hash = await self.compile_and_deploy('test_sc/arithmetic_test', 'Addition.py')
        result, _ = await self.call('add',
                                    [1, 2],
                                    return_type=int,
                                    target_contract=call_hash
                                    )
        self.assertEqual(1 + 2, result)
        expected = result

        result, _ = await self.call('Main', [call_hash, 'add', [1, 2]], return_type=int)
        self.assertEqual(expected, result)

        result, _ = await self.call('Main', [call_hash, 'add', [-42, -24]], return_type=int)
        self.assertEqual(-66, result)

        result, _ = await self.call('Main', [call_hash, 'add', [-42, 24]], return_type=int)
        self.assertEqual(-18, result)

    async def test_call_contract_with_cast(self):
        await self.set_up_contract('CallScriptHashWithCast.py')

        invalid_contract = types.UInt160.zero()
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [invalid_contract, 'add', [1, 2]], return_type=bool)

        self.assertRegex(str(context.exception), f'called contract {invalid_contract} not found')

        call_hash = await self.compile_and_deploy('test_sc/arithmetic_test', 'Addition.py')
        result, _ = await self.call('Main', [call_hash, 'add', [1, 2]], return_type=bool)
        self.assertEqual(True, result)

    async def test_call_contract_without_args(self):
        await self.set_up_contract('CallScriptHashWithoutArgs.py')

        invalid_contract = types.UInt160.zero()
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [invalid_contract, 'Main'], return_type=list[int])

        self.assertRegex(str(context.exception), f'called contract {invalid_contract} not found')

        call_hash = await self.compile_and_deploy('test_sc/list_test', 'IntList.py')
        result, _ = await self.call('Main', [], return_type=list[int], target_contract=call_hash)
        self.assertEqual([1, 2, 3], result)
        expected = result

        result, _ = await self.call('Main', [call_hash, 'Main'], return_type=list[int])
        self.assertEqual(expected, result)

    async def test_call_contract_with_flags(self):
        await self.set_up_contract('CallScriptHashWithFlags.py')
        call_hash = await self.compile_and_deploy('CallFlagsUsage.py')

        from dataclasses import dataclass
        from neo3.api import noderpc
        from neo3.contracts.callflags import CallFlags

        @dataclass
        class NotifyEvent(boatestcase.BoaTestEvent):
            state: str

            @classmethod
            def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
                inner_args_types = tuple(cls.__annotations__.values())
                e = super().from_notification(n, *inner_args_types)
                return cls(e.contract, e.name, e.state[0])

        result, _ = await self.call(
            'Main',
            [call_hash, 'get_value', [b'num'], CallFlags.READ_ONLY],
            return_type=int
        )
        self.assertEqual(0, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [call_hash, 'put_value', [b'num', 10], CallFlags.NONE], return_type=None)
        self.assertRegex(str(context.exception), f'missing call flags: {CallFlags.NONE:05b}')

        expected = 10
        result, _ = await self.call(
            'Main',
            [call_hash, 'put_value', [b'num', expected], CallFlags.STATES],
            return_type=None,
            signing_accounts=[self.genesis]
        )
        self.assertEqual(None, result)

        current_storage = await self.get_storage(target_contract=call_hash,
                                                 values_post_processor=storage.as_int
                                                 )
        self.assertIn(b'num', current_storage)
        self.assertEqual(expected, current_storage[b'num'])

        result, _ = await self.call(
            'Main',
            [call_hash, 'get_value', [b'num'], CallFlags.READ_ONLY],
            return_type=int
        )
        self.assertEqual(expected, result)

        expected = 99
        result, _ = await self.call(
            'Main',
            [call_hash, 'put_value', [b'num', expected], CallFlags.ALL],
            return_type=None,
            signing_accounts=[self.genesis]
        )
        self.assertEqual(None, result)

        current_storage = await self.get_storage(target_contract=call_hash,
                                                 values_post_processor=storage.as_int
                                                 )
        self.assertIn(b'num', current_storage)
        self.assertEqual(expected, current_storage[b'num'])

        result, _ = await self.call(
            'Main',
            [call_hash, 'get_value', [b'num'], CallFlags.READ_ONLY],
            return_type=int
        )
        self.assertEqual(expected, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [call_hash, 'get_value', [b'num'], CallFlags.NONE], return_type=int)
        self.assertRegex(str(context.exception), f'missing call flags: {CallFlags.NONE:05b}')

        result, notifications = await self.call(
            'Main',
            [call_hash, 'notify_user', [], CallFlags.ALL],
            return_type=None
        )
        self.assertEqual(None, result)

        notify = self.filter_events(
            notifications,
            origin=call_hash,
            notification_type=NotifyEvent
        )
        self.assertEqual(1, len(notify))
        self.assertEqual('Notify was called', notify[0].state)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [call_hash, 'notify_user', [], CallFlags.READ_ONLY], return_type=None)
        self.assertRegex(str(context.exception), f'missing call flags: {CallFlags.READ_ONLY:05b}')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [call_hash, 'notify_user', [], CallFlags.STATES], return_type=None)
        self.assertRegex(str(context.exception), f'missing call flags: {CallFlags.STATES:05b}')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [call_hash, 'notify_user', [], CallFlags.NONE], return_type=None)
        self.assertRegex(str(context.exception), f'missing call flags: {CallFlags.NONE:05b}')

        result, _ = await self.call(
            'Main',
            [call_hash, 'call_another_contract', [], CallFlags.ALL],
            return_type=int
        )
        self.assertEqual(0, result)

        result, _ = await self.call(
            'Main',
            [call_hash, 'call_another_contract', [], CallFlags.READ_ONLY],
            return_type=int
        )
        self.assertEqual(0, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [call_hash, 'call_another_contract', [], CallFlags.STATES], return_type=int)
        self.assertRegex(str(context.exception), f'missing call flags: {CallFlags.STATES:05b}')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [call_hash, 'call_another_contract', [], CallFlags.NONE], return_type=int)
        self.assertRegex(str(context.exception), f'missing call flags: {CallFlags.NONE:05b}')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [call_hash, 'Main'], return_type=int)
        self.assertRegex(str(context.exception), 'method not found: {0}/{1}'.format('Main', 2))

    def test_call_contract_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'CallScriptHashTooManyArguments.py')

    def test_call_contract_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'CallScriptHashTooFewArguments.py')

    def test_create_standard_account_compile(self):
        from boa3.internal.neo.vm.type.StackItem import StackItemType
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
                Opcode.INITSLOT
                + b'\x00\x01'
                + Opcode.LDARG0
                + Opcode.DUP
                + Opcode.ISNULL
                + Opcode.NOT
                + Opcode.JMPIFNOT
                + Integer(11).to_byte_array(min_length=1)
                + Opcode.CONVERT
                + StackItemType.ByteString
                + Opcode.DUP
                + Opcode.SIZE
                + Opcode.PUSHINT8
                + Integer(33).to_byte_array(min_length=1)
                + Opcode.NUMEQUAL
                + Opcode.JMPIF
                + Integer(3).to_byte_array(min_length=1)
                + Opcode.THROW
                + Opcode.SYSCALL
                + Interop.CreateStandardAccount.interop_method_hash
                + Opcode.RET
        )
        output, _ = self.assertCompile('CreateStandardAccount.py')
        self.assertEqual(expected_output, output)

    async def test_create_standard_account_run(self):
        await self.set_up_contract('CreateStandardAccount.py')

        public_key = self.account.public_key
        expected = self.account.script_hash
        result, _ = await self.call('main', [public_key], return_type=types.UInt160)
        self.assertEqual(expected, result)

    def test_create_standard_account_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'CreateStandardAccountTooFewArguments.py')

    def test_create_standard_account_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'CreateStandardAccountTooManyArguments.py')

    def test_create_multisig_account_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
                Opcode.INITSLOT
                + b'\x00\x02'
                + Opcode.LDARG1
                + Opcode.LDARG0
                + Opcode.SYSCALL
                + Interop.CreateMultisigAccount.interop_method_hash
                + Opcode.RET
        )
        output, _ = self.assertCompile('CreateMultisigAccount.py')
        self.assertEqual(expected_output, output)

    async def test_create_multisig_account_run(self):
        await self.set_up_contract('CreateMultisigAccount.py')

        minimum_sigs = 2
        account2 = self.node.wallet.account_new(label='test2')
        account3 = self.node.wallet.account_new(label='test3')
        accounts = [
            self.account.public_key,
            account2.public_key,
            account3.public_key
        ]
        multisig_account = self.node.wallet.import_multisig_address(
            minimum_sigs,
            accounts
        )

        expected = multisig_account.script_hash
        result, _ = await self.call('main', [minimum_sigs, accounts], return_type=types.UInt160)
        self.assertEqual(expected, result)

    def test_create_multisig_account_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'CreateMultisigAccountTooFewArguments.py')

    def test_create_multisig_account_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'CreateMultisigAccountTooManyArguments.py')

    async def test_import_contract(self):
        await self.set_up_contract('ImportScUtils.py')
        call_hash = await self.compile_and_deploy('test_sc/arithmetic_test', 'Addition.py')

        expected, _ = await self.call('add', [1, 2], return_type=int, target_contract=call_hash)
        result, _ = await self.call('main', [call_hash, 'add', [1, 2]], return_type=int)
        self.assertEqual(expected, result)

        result, _ = await self.call('call_flags_all', [], return_type=int)
        from neo3.contracts.callflags import CallFlags
        self.assertEqual(CallFlags.ALL, result)

    async def test_hash160_str(self):
        await self.set_up_contract('Hash160Str.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result, _ = await self.call('Main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash160_int(self):
        await self.set_up_contract('Hash160Int.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(Integer(10).to_byte_array()).digest())).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash160_bool(self):
        await self.set_up_contract('Hash160Bool.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(Integer(1).to_byte_array()).digest())).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash160_bytes(self):
        await self.set_up_contract('Hash160Bytes.py')

        expected_result = hashlib.new('ripemd160', (hashlib.sha256(b'unit test').digest())).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash256_str(self):
        await self.set_up_contract('Hash256Str.py')

        expected_result = hashlib.sha256(hashlib.sha256(b'unit test').digest()).digest()
        result, _ = await self.call('Main', ['unit test'], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash256_int(self):
        await self.set_up_contract('Hash256Int.py')

        expected_result = hashlib.sha256(hashlib.sha256(Integer(10).to_byte_array()).digest()).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash256_bool(self):
        await self.set_up_contract('Hash256Bool.py')

        expected_result = hashlib.sha256(hashlib.sha256(Integer(1).to_byte_array()).digest()).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    async def test_hash256_bytes(self):
        await self.set_up_contract('Hash256Bytes.py')

        expected_result = hashlib.sha256(hashlib.sha256(b'unit test').digest()).digest()
        result, _ = await self.call('Main', [], return_type=bytes)
        self.assertEqual(expected_result, result)

    def test_check_sig_compile(self):
        byte_input0 = b'\x03\x5a\x92\x8f\x20\x16\x39\x20\x4e\x06\xb4\x36\x8b\x1a\x93\x36\x54\x62\xa8\xeb\xbf\xf0\xb8\x81\x81\x51\xb7\x4f\xaa\xb3\xa2\xb6\x1a'
        byte_input1 = b'wrongsignature'

        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + self.ecpoint_init
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.STLOC1
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.LDLOC0
                + Opcode.SYSCALL
                + Interop.CheckSig.interop_method_hash
                + Opcode.RET
        )

        output, _ = self.assertCompile('CheckSig.py')
        self.assertEqual(expected_output, output)

    async def test_check_sig_run(self):
        await self.set_up_contract('CheckSig.py')

        result, _ = await self.call('main', [], return_type=bool)
        self.assertEqual(False, result)

    def test_check_multisig_compile(self):
        byte_input0 = b'\x03\xcd\xb0g\xd90\xfdZ\xda\xa6\xc6\x85E\x01`D\xaa\xdd\xecd\xba9\xe5H%\x0e\xae\xa5Q\x17.S\\'
        byte_input1 = b'\x03l\x841\xccx\xb31w\xa6\x0bK\xcc\x02\xba\xf6\r\x05\xfe\xe5\x03\x8es9\xd3\xa6\x88\xe3\x94\xc2\xcb\xd8C'
        byte_input2 = b'wrongsignature1'
        byte_input3 = b'wrongsignature2'

        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + self.ecpoint_init
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + self.ecpoint_init
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input3)).to_byte_array(min_length=1)
                + byte_input3
                + Opcode.PUSHDATA1
                + Integer(len(byte_input2)).to_byte_array(min_length=1)
                + byte_input2
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC1
                + Opcode.LDLOC1
                + Opcode.LDLOC0
                + Opcode.SYSCALL
                + Interop.CheckMultisig.interop_method_hash
                + Opcode.RET
        )

        output, _ = self.assertCompile('CheckMultisig.py')
        self.assertEqual(expected_output, output)

    async def test_check_multisig_run(self):
        await self.set_up_contract('CheckMultisig.py')

        result, _ = await self.call('main', [], return_type=bool)
        self.assertEqual(False, result)
