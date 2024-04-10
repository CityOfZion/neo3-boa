import json

from boaconstructor import storage
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.wallet import account

from boa3.internal import constants
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import annotation, boatestcase, event, stackitem


class TestContractInterop(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/interop_test/contract'
    account: account.Account

    @classmethod
    def setupTestCase(cls):
        cls.account = cls.node.wallet.account_new(label='test', password='123')
        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account.script_hash, 100)

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
            def from_untyped_notification(cls, n: noderpc.Notification):
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

    async def test_create_contract(self):
        await self.set_up_contract('CreateContract.py')
        call_contract_path = self.get_contract_path('test_sc/arithmetic_test', 'Addition.py')

        nef_file, manifest = self.get_serialized_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()
        manifest = stackitem.from_manifest(manifest)

        result, notifications = await self.call(
            'Main',
            [nef_file, arg_manifest, None],
            return_type=annotation.Contract
        )

        deploy_events = self.filter_events(notifications,
                                           event_name='Deploy',
                                           notification_type=event.DeployEvent
                                           )
        self.assertEqual(1, len(deploy_events))

        self.assertEqual(5, len(result))
        self.assertEqual(0, result[1])  # contract update counter must be zero on deploy
        self.assertEqual(nef_file, result[3])
        self.assertEqual(manifest, result[4])

    async def test_create_contract_data_deploy(self):
        await self.set_up_contract('CreateContract.py')
        call_contract_path = self.get_contract_path('NewContract.py')

        self.compile_and_save(call_contract_path)
        nef_file, manifest = self.get_serialized_output(call_contract_path)
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()
        manifest = stackitem.from_manifest(manifest)

        data = 'some sort of data'
        result, notifications = await self.call(
            'Main',
            [nef_file, arg_manifest, data],
            return_type=annotation.Contract
        )

        deploy_events = self.filter_events(notifications,
                                           event_name='Deploy',
                                           notification_type=event.DeployEvent
                                           )
        self.assertEqual(1, len(deploy_events))

        self.assertEqual(5, len(result))
        self.assertEqual(0, result[1])  # contract update counter must be zero on deploy
        self.assertEqual(nef_file, result[3])
        self.assertEqual(manifest, result[4])

        notifies = self.filter_events(notifications,
                                      event_name='notify',
                                      notification_type=boatestcase.BoaTestEvent
                                      )
        self.assertEqual(2, len(notifies))
        self.assertEqual(False, notifies[0].state[0])
        self.assertEqual(data, notifies[1].state[0])

    def test_create_contract_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'CreateContractTooManyArguments.py')

    def test_create_contract_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'CreateContractTooFewArguments.py')

    async def test_update_contract(self):
        await self.set_up_contract('UpdateContract.py')

        updated_method = 'new_method'
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call(updated_method, [], return_type=None)

        self.assertRegex(str(context.exception), fr"method not found: {updated_method}/\d+")

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_serialized_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        result, notifications = await self.call('update',
                                                [new_nef, arg_manifest, None],
                                                return_type=None,
                                                signing_accounts=[self.genesis]
                                                )
        self.assertIsNone(result)
        update_events = self.filter_events(notifications,
                                           event_name='Update',
                                           notification_type=event.UpdateEvent
                                           )
        self.assertEqual(1, len(update_events))
        self.assertEqual(self.contract_hash, update_events[0].updated_contract)

        result, _ = await self.call(updated_method, [], return_type=int)
        self.assertEqual(42, result)

    async def test_update_contract_data_deploy(self):
        await self.set_up_contract('UpdateContract.py', signing_account=self.account)

        updated_method = 'new_method'
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call(updated_method, [], return_type=int)

        self.assertRegex(str(context.exception), fr"method not found: {updated_method}/\d+")

        new_path = self.get_contract_path('test_sc/interop_test', 'UpdateContract.py')
        self.compile_and_save(new_path)
        new_nef, new_manifest = self.get_serialized_output(new_path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        data = 'this function was deployed'
        result, notifications = await self.call('update', [new_nef, arg_manifest, data], return_type=None)
        self.assertIsNone(result)
        update_events = self.filter_events(notifications,
                                           event_name='Update',
                                           notification_type=event.UpdateEvent
                                           )
        self.assertEqual(1, len(update_events))
        self.assertEqual(self.contract_hash, update_events[0].updated_contract)

        notifies = self.filter_events(notifications,
                                      event_name='notify',
                                      notification_type=boatestcase.BoaTestEvent
                                      )
        self.assertEqual(2, len(notifies))
        self.assertEqual(True, notifies[0].state[0])
        self.assertEqual(data, notifies[1].state[0])

    def test_update_contract_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'UpdateContractTooManyArguments.py')

    def test_update_contract_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'UpdateContractTooFewArguments.py')

    async def test_destroy_contract(self):
        await self.set_up_contract('DestroyContract.py')

        contract_hash = self.contract_hash
        result, notifications = await self.call('Main', [], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)
        destroy_events = self.filter_events(notifications,
                                            event_name='Destroy',
                                            notification_type=event.DestroyEvent
                                            )
        self.assertEqual(1, len(destroy_events))
        self.assertEqual(contract_hash, destroy_events[0].destroyed_contract)

        call_contract = await self.compile_and_deploy('boa3_test/test_sc/interop_test/contract', 'CallScriptHash.py')
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main',
                            [contract_hash, 'Main', []],
                            return_type=None,
                            target_contract=call_contract
                            )

        self.assertRegex(str(context.exception), f'called contract {contract_hash} not found')

    def test_destroy_contract_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'DestroyContractTooManyArguments.py')

    def test_get_neo_native_script_hash_compile(self):
        from boa3.internal.neo.vm.type.Integer import Integer

        value = constants.NEO_SCRIPT
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array()
            + value
            + Opcode.RET
        )

        output, _ = self.assertCompile('NeoScriptHash.py')
        self.assertEqual(expected_output, output)

    async def test_get_neo_native_script_hash_run(self):
        await self.set_up_contract('NeoScriptHash.py')

        expected = types.UInt160(constants.NEO_SCRIPT)
        result, _ = await self.call('Main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_neo_native_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, 'NeoScriptHashCantAssign.py')
        self.assertEqual(expected_output, output)

    def test_get_gas_native_script_hash_compile(self):
        from boa3.internal.neo.vm.type.Integer import Integer

        value = constants.GAS_SCRIPT
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array()
            + value
            + Opcode.RET
        )

        output, _ = self.assertCompile('GasScriptHash.py')
        self.assertEqual(expected_output, output)

    async def test_get_gas_native_script_hash_run(self):
        await self.set_up_contract('GasScriptHash.py')

        expected = types.UInt160(constants.GAS_SCRIPT)
        result, _ = await self.call('Main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    def test_gas_native_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, 'GasScriptHashCantAssign.py')
        self.assertEqual(expected_output, output)

    async def test_call_flags_type(self):
        await self.set_up_contract('CallFlagsType.py')

        from neo3.contracts.callflags import CallFlags

        result, _ = await self.call('main', ['ALL'], return_type=int)
        self.assertEqual(CallFlags.ALL, result)

        result, _ = await self.call('main', ['READ_ONLY'], return_type=int)
        self.assertEqual(CallFlags.READ_ONLY, result)

        result, _ = await self.call('main', ['STATES'], return_type=int)
        self.assertEqual(CallFlags.STATES, result)

        result, _ = await self.call('main', ['ALLOW_NOTIFY'], return_type=int)
        self.assertEqual(CallFlags.ALLOW_NOTIFY, result)

        result, _ = await self.call('main', ['ALLOW_CALL'], return_type=int)
        self.assertEqual(CallFlags.ALLOW_CALL, result)

        result, _ = await self.call('main', ['WRITE_STATES'], return_type=int)
        self.assertEqual(CallFlags.WRITE_STATES, result)

        result, _ = await self.call('main', ['READ_STATES'], return_type=int)
        self.assertEqual(CallFlags.READ_STATES, result)

        result, _ = await self.call('main', ['NONE'], return_type=int)
        self.assertEqual(CallFlags.NONE, result)

    async def test_get_call_flags(self):
        await self.set_up_contract('CallScriptHashWithFlags.py')
        call_hash = await self.compile_and_deploy('GetCallFlags.py')

        from neo3.contracts.callflags import CallFlags

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.ALL], return_type=int)
        self.assertEqual(CallFlags.ALL, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.READ_ONLY], return_type=int)
        self.assertEqual(CallFlags.READ_ONLY, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.STATES], return_type=int)
        self.assertEqual(CallFlags.STATES, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.NONE], return_type=int)
        self.assertEqual(CallFlags.NONE, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.READ_STATES], return_type=int)
        self.assertEqual(CallFlags.READ_STATES, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.WRITE_STATES], return_type=int)
        self.assertEqual(CallFlags.WRITE_STATES, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.ALLOW_CALL], return_type=int)
        self.assertEqual(CallFlags.ALLOW_CALL, result)

        result, _ = await self.call('Main', [call_hash, 'main', [], CallFlags.ALLOW_NOTIFY], return_type=int)
        self.assertEqual(CallFlags.ALLOW_NOTIFY, result)

    async def test_import_contract(self):
        await self.set_up_contract('ImportContract.py')
        call_hash = await self.compile_and_deploy('test_sc/arithmetic_test', 'Addition.py')

        expected, _ = await self.call('add', [1, 2], return_type=int, target_contract=call_hash)
        result, _ = await self.call('main', [call_hash, 'add', [1, 2]], return_type=int)
        self.assertEqual(expected, result)

        result, _ = await self.call('call_flags_all', [], return_type=int)
        from neo3.contracts.callflags import CallFlags
        self.assertEqual(CallFlags.ALL, result)

    async def test_import_interop_contract(self):
        await self.set_up_contract('ImportInteropContract.py')
        call_hash = await self.compile_and_deploy('test_sc/arithmetic_test', 'Addition.py')

        expected, _ = await self.call('add', [1, 2], return_type=int, target_contract=call_hash)
        result, _ = await self.call('main', [call_hash, 'add', [1, 2]], return_type=int)
        self.assertEqual(expected, result)

        result, _ = await self.call('call_flags_all', [], return_type=int)
        from neo3.contracts.callflags import CallFlags
        self.assertEqual(CallFlags.ALL, result)

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

    async def test_get_minimum_deployment_fee(self):
        await self.set_up_contract('GetMinimumDeploymentFee.py')

        minimum_cost = 10 * 10 ** 8  # minimum deployment cost is 10 GAS right now
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(minimum_cost, result)

    def test_get_minimum_deployment_fee_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'GetMinimumDeploymentFeeTooManyArguments.py')

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
        account2 = self.node.wallet.account_new(label='test2', password='123')
        account3 = self.node.wallet.account_new(label='test3', password='123')
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
