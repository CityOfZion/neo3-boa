from neo3.api import noderpc
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import utils, types
from neo3.wallet import account

from boa3.internal import constants
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.contracts import TriggerType
from boa3_test.tests import annotation, boatestcase


class TestRuntimeInterop(boatestcase.BoaTestCase):
    from boa3.internal.model.builtin.interop.interop import Interop

    default_folder: str = 'test_sc/interop_test/runtime'
    notify_default_name = Interop.Notify.name

    account: account.Account

    @classmethod
    def setupTestCase(cls):
        cls.account = cls.node.wallet.account_new(label='test', password='123')
        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account.script_hash, 100)

    @classmethod
    async def get_version(cls) -> noderpc.GetVersionResponse:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host) as rpc_client:
            return await rpc_client.get_version()

    async def test_check_witness(self):
        await self.set_up_contract('CheckWitness.py')

        account_hash = self.account.script_hash
        result, _ = await self.call('Main', [account_hash], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [account_hash], return_type=bool, signing_accounts=[self.account])
        self.assertEqual(True, result)

    async def test_contract_with_check_witness(self):
        await self.set_up_contract('CheckWitness.py')
        call_contract = await self.compile_and_deploy('test_sc/interop_test/contract', 'CallScriptHash.py')

        contract_method = 'Main'
        contract_args = [self.account.script_hash]
        result, _ = await self.call(contract_method, contract_args, return_type=bool)
        self.assertEqual(False, result)

        contract_hash = self.contract_hash
        result, _ = await self.call(contract_method,
                                    contract_args,
                                    return_type=bool,
                                    signing_accounts=[self.account]
                                    )
        self.assertEqual(True, result)

        result, _ = await self.call('Main',
                                    [contract_hash, contract_method, contract_args],
                                    return_type=bool,
                                    target_contract=call_contract,
                                    signing_accounts=[self.account]
                                    )
        self.assertEqual(False, result)  # fail because the signer have CalledByEntry scope

    async def test_check_witness_imported_as(self):
        await self.set_up_contract('CheckWitnessImportedAs.py')

        account_hash = self.account.script_hash
        result, _ = await self.call('Main', [account_hash], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('Main', [account_hash], return_type=bool, signing_accounts=[self.account])
        self.assertEqual(True, result)

    def test_check_witness_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'CheckWitnessMismatchedType.py')

    def test_notify_str_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        event_name = String(self.notify_default_name).to_bytes()
        message = 'str'

        string = String(message).to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.SWAP
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('NotifyStr.py')
        self.assertEqual(expected_output, output)

    async def test_notify_str_run(self):
        await self.set_up_contract('NotifyStr.py')
        message = 'str'

        result, notifications = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        event_notifications = self.filter_events(notifications,
                                                 event_name=self.notify_default_name,
                                                 notification_type=boatestcase.BoaTestEvent
                                                 )
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((message,), event_notifications[0].state)

    def test_notify_int_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        event_name = String(self.notify_default_name).to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.PUSH15
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.SWAP
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('NotifyInt.py')
        self.assertEqual(expected_output, output)

    async def test_notify_int_run(self):
        await self.set_up_contract('NotifyInt.py')

        result, notifications = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        event_notifications = self.filter_events(notifications,
                                                 event_name=self.notify_default_name,
                                                 notification_type=boatestcase.BoaTestEvent
                                                 )
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((15,), event_notifications[0].state)

    def test_notify_bool_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        event_name = String(self.notify_default_name).to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.PUSHT
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.SWAP
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('NotifyBool.py')
        self.assertEqual(expected_output, output)

    async def test_notify_bool_run(self):
        await self.set_up_contract('NotifyBool.py')

        result, notifications = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        event_notifications = self.filter_events(notifications,
                                                 event_name=self.notify_default_name,
                                                 notification_type=boatestcase.BoaTestEvent
                                                 )
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((True,), event_notifications[0].state)

    def test_notify_none_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        event_name = String(self.notify_default_name).to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.PUSHNULL
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.SWAP
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('NotifyNone.py')
        self.assertEqual(expected_output, output)

    async def test_notify_none_run(self):
        await self.set_up_contract('NotifyNone.py')

        result, notifications = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        event_notifications = self.filter_events(notifications,
                                                 event_name=self.notify_default_name,
                                                 notification_type=boatestcase.BoaTestEvent
                                                 )
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((None,), event_notifications[0].state)

    def test_notify_sequence_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        event_name = String(self.notify_default_name).to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.PUSH7
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.SWAP
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('NotifySequence.py')
        self.assertEqual(expected_output, output)

    async def test_notify_sequence_run(self):
        await self.set_up_contract('NotifySequence.py')

        result, notifications = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        event_notifications = self.filter_events(notifications,
                                                 event_name=self.notify_default_name,
                                                 notification_type=boatestcase.BoaTestEvent
                                                 )
        self.assertEqual(1, len(event_notifications))
        self.assertEqual(([2, 3, 5, 7],), event_notifications[0].state)

    async def test_notify_with_dynamic_name_run(self):
        self.assertCompilerLogs(CompilerError.InvalidUsage, 'NotifyWithDynamicName.py')

    def test_notify_with_name_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop
        unit_test = String('unit_test').to_bytes()

        expected_output = (
            Opcode.PUSHDATA1  # 'unit_test
            + Integer(len(unit_test)).to_byte_array() + unit_test
            + Opcode.PUSH10
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.SWAP
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('NotifyWithName.py')
        self.assertEqual(expected_output, output)

    async def test_notify_with_name_run(self):
        await self.set_up_contract('NotifyWithName.py')

        event_name = 'unit_test'
        result, notifications = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        event_notifications = self.filter_events(notifications,
                                                 event_name=event_name,
                                                 notification_type=boatestcase.BoaTestEvent
                                                 )
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((10,), event_notifications[0].state)

    def test_log_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'LogMismatchedValueInt.py')

    def test_log_str_commpile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        string = String('str').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.Log.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('LogStr.py')
        self.assertEqual(expected_output, output)

    async def test_log_str_run(self):
        await self.set_up_contract('LogStr.py')

        result, notifications = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)
        self.assertEqual(0, len(notifications))

    def test_get_trigger_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('Trigger.py')
        self.assertEqual(expected_output, output)

    async def test_get_trigger_run(self):
        await self.set_up_contract('Trigger.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(TriggerType.APPLICATION, result)

    def test_is_application_trigger_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        application = Integer(TriggerType.APPLICATION).to_byte_array()
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.PUSHINT8 + application
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('TriggerApplication.py')
        self.assertEqual(expected_output, output)

    async def test_is_application_trigger_run(self):
        await self.set_up_contract('TriggerApplication.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(True, result)

    def test_is_verification_trigger_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        verification = Integer(TriggerType.VERIFICATION).to_byte_array()
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.PUSHINT8 + verification
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        output, _ = self.assertCompile('TriggerVerification.py')
        self.assertEqual(expected_output, output)

    async def test_is_verification_trigger_run(self):
        await self.set_up_contract('TriggerVerification.py')

        result, _ = await self.call('Main', [], return_type=bool)
        self.assertEqual(False, result)

    def test_get_calling_script_hash_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
            Opcode.SYSCALL
            + Interop.CallingScriptHash.getter.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('CallingScriptHash.py')
        self.assertEqual(expected_output, output)

    async def test_get_calling_script_hash_run(self):
        await self.set_up_contract('CallingScriptHash.py')
        call_contract = await self.compile_and_deploy('test_sc/interop_test/contract', 'CallScriptHash.py')

        method_id = 'Main'
        result, _ = await self.call(method_id,
                                    [],
                                    return_type=types.UInt160,
                                    signing_accounts=[self.genesis]
                                    )
        tx = await self.get_last_tx()
        self.assertIsNotNone(tx)

        expected = utils.to_script_hash(tx.script)
        self.assertEqual(expected, result)

        expected = call_contract
        result, _ = await self.call('Main',
                                    [self.contract_hash, method_id, []],
                                    return_type=types.UInt160,
                                    target_contract=call_contract
                                    )
        self.assertEqual(expected, result)

    def test_calling_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, 'CallingScriptHashCantAssign.py')
        self.assertEqual(expected_output, output)

    def test_get_executing_script_hash_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
            Opcode.SYSCALL
            + Interop.ExecutingScriptHash.getter.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('ExecutingScriptHash.py')
        self.assertEqual(expected_output, output)

    async def test_get_executing_script_hash_run(self):
        await self.set_up_contract('ExecutingScriptHash.py')

        result, _ = await self.call('Main', [], return_type=types.UInt160)
        self.assertEqual(self.contract_hash, result)

    def test_executing_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, 'ExecutingScriptHashCantAssign.py')
        self.assertEqual(expected_output, output)

    async def test_get_executing_script_hash_on_deploy(self):
        await self.set_up_contract('ExecutingScriptHashOnDeploy.py')

        result, _ = await self.call('get_script', [], return_type=types.UInt160)
        self.assertEqual(self.contract_hash, result)

    def test_get_block_time_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
            Opcode.SYSCALL
            + Interop.BlockTime.getter.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('BlockTime.py')
        self.assertEqual(expected_output, output)

    async def test_get_block_time_run(self):
        await self.set_up_contract('BlockTime.py')

        result, _ = await self.call('Main',
                                    [],
                                    return_type=int,
                                    signing_accounts=[self.genesis]
                                    )
        last_block = await self.get_latest_block()
        self.assertEqual(last_block.timestamp, result)

    def test_block_time_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, 'BlockTimeCantAssign.py')
        self.assertEqual(expected_output, output)

    def test_get_gas_left_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
            Opcode.SYSCALL
            + Interop.GasLeft.getter.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('GasLeft.py')
        self.assertEqual(expected_output, output)

    async def test_get_gas_left_run(self):
        await self.set_up_contract('GasLeft.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertGreaterEqual(result, 0)

    def test_gas_left_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, 'GasLeftCantAssign.py')
        self.assertEqual(expected_output, output)

    def test_get_invocation_counter_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
            Opcode.SYSCALL
            + Interop.InvocationCounter.getter.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('InvocationCounter.py')
        self.assertEqual(expected_output, output)

    async def test_get_invocation_counter_run(self):
        await self.set_up_contract('InvocationCounter.py')

        method_id = 'Main'
        result, _ = await self.call(method_id, [], return_type=int)
        self.assertEqual(1, result)

    def test_invocation_counter_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, 'InvocationCounterCantAssign.py')
        self.assertEqual(expected_output, output)

    async def test_get_notifications(self):
        await self.set_up_contract('GetNotifications.py')

        script = self.contract_hash
        Notification = annotation.Notification[list[int]]

        arg = []
        expected = []
        result, notifications = await self.call('without_param', [arg], return_type=list[Notification])
        self.assertEqual(expected, result)
        self.assertEqual(len(arg), len(notifications))

        arg = [1, 2, 3]
        expected: list[Notification] = [(script, 'notify', [x]) for x in arg]
        result, notifications = await self.call('without_param', [arg], return_type=list[Notification])
        self.assertEqual(expected, result)
        self.assertEqual(len(arg), len(notifications))

        filtered_notifications = self.filter_events(notifications,
                                                    notification_type=boatestcase.BoaTestEvent
                                                    )
        self.assertEqual(len(expected), len(filtered_notifications))
        for index, x in enumerate(arg):
            self.assertEqual((x,), filtered_notifications[index].state)

        arg = []
        expected = []
        script = types.UInt160(constants.MANAGEMENT_SCRIPT)
        result, notifications = await self.call('with_param',
                                                [arg, script],
                                                return_type=list[Notification]
                                                )
        self.assertEqual(expected, result)
        self.assertEqual(len(arg), len(notifications))

        arg = [4, 5, 6]
        script = self.contract_hash
        expected: list[Notification] = [(script, 'notify', [x]) for x in arg]
        result, notifications = await self.call('with_param', [arg, script], return_type=list[Notification])
        self.assertEqual(expected, result)
        self.assertEqual(len(arg), len(notifications))

        filtered_notifications = self.filter_events(notifications,
                                                    notification_type=boatestcase.BoaTestEvent
                                                    )
        self.assertEqual(len(expected), len(filtered_notifications))
        for index, x in enumerate(arg):
            self.assertEqual((x,), filtered_notifications[index].state)

        arg = [1, 2, 3]
        script = types.UInt160(b'\x01' * 20)
        expected = []
        result, notifications = await self.call('with_param', [arg, script], return_type=list[Notification])
        self.assertEqual(expected, result)
        self.assertEqual(len(arg), len(notifications))

        filtered_notifications = self.filter_events(notifications,
                                                    origin=script,
                                                    notification_type=boatestcase.BoaTestEvent
                                                    )
        self.assertEqual(len(expected), len(filtered_notifications))

    def test_get_entry_script_hash_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
            Opcode.SYSCALL
            + Interop.EntryScriptHash.getter.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('EntryScriptHash.py')
        self.assertEqual(expected_output, output)

    async def test_get_entry_script_hash_run(self):
        await self.set_up_contract('EntryScriptHash.py')
        call_contract = await self.compile_and_deploy('test_sc/interop_test/contract', 'CallScriptHash.py')

        method_id = 'main'
        result, _ = await self.call(method_id,
                                    [],
                                    return_type=types.UInt160,
                                    signing_accounts=[self.genesis]
                                    )
        tx = await self.get_last_tx()
        self.assertIsNotNone(tx)

        expected = utils.to_script_hash(tx.script)
        self.assertEqual(expected, result)

        result, _ = await self.call('Main',
                                    [self.contract_hash, method_id, []],
                                    return_type=types.UInt160,
                                    target_contract=call_contract,
                                    signing_accounts=[self.genesis]
                                    )
        tx = await self.get_last_tx()
        self.assertIsNotNone(tx)

        expected = utils.to_script_hash(tx.script)
        self.assertEqual(expected, result)

    def test_entry_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, 'EntryScriptHashCantAssign.py')
        self.assertEqual(expected_output, output)

    def test_platform_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
            Opcode.SYSCALL
            + Interop.Platform.getter.interop_method_hash
            + Opcode.RET
        )

        output, _ = self.assertCompile('Platform.py')
        self.assertEqual(expected_output, output)

    async def test_platform_run(self):
        await self.set_up_contract('Platform.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('NEO', result)

    def test_platform_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.NameShadowing, 'PlatformCantAssign.py')
        self.assertEqual(expected_output, output)

    async def test_burn_gas(self):
        await self.set_up_contract('BurnGas.py')

        burned_gas_1 = 1 * 10 ** 8  # 1 GAS
        result, _ = await self.call('main', [burned_gas_1], return_type=None)
        self.assertIsNone(result)

        burned_gas_2 = 123 * 10 ** 5  # 0.123 GAS
        result, _ = await self.call('main', [burned_gas_2], return_type=None)
        self.assertIsNone(result)

        error_message = 'GAS must be positive'
        # can not burn negative GAS
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [-10 ** 8], return_type=None)

        self.assertRegex(str(context.exception), error_message)

        # can not burn no GAS
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [0], return_type=None)

        self.assertRegex(str(context.exception), error_message)

    async def test_boa2_runtime_test(self):
        await self.set_up_contract('RuntimeBoa2Test.py')

        result, _ = await self.call('main',
                                    ['time', 1],
                                    return_type=int,
                                    signing_accounts=[self.genesis]
                                    )
        last_block = await self.get_latest_block()
        self.assertEqual(last_block.timestamp, result)

        result, _ = await self.call('main', ['check_witness', self.account.script_hash], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('main', ['log', 'hello'], return_type=bool)
        self.assertEqual(True, result)

        result, notifications = await self.call('main', ['notify', 1234], return_type=bool)
        self.assertEqual(True, result)

        events = self.filter_events(notifications,
                                    event_name=self.notify_default_name,
                                    notification_type=boatestcase.BoaTestEvent
                                    )
        self.assertEqual(1, len(events))
        self.assertEqual((1234,), events[0].state)

        result, _ = await self.call('main', ['get_trigger', 1234], return_type=int)
        self.assertEqual(TriggerType.APPLICATION, result)

    async def test_boa2_trigger_type_test(self):
        await self.set_up_contract('TriggerTypeBoa2Test.py')

        result, _ = await self.call('main', [1], return_type=int)
        self.assertEqual(0x40, result)

        result, _ = await self.call('main', [2], return_type=int)
        self.assertEqual(0x20, result)

        result, _ = await self.call('main', [3], return_type=bytes)
        self.assertEqual(b'\x20', result)

        result, _ = await self.call('main', [0], return_type=int)
        self.assertEqual(-1, result)

    async def test_get_script_container(self):
        await self.set_up_contract('ScriptContainer.py')

        result, _ = await self.call('main',
                                    [],
                                    return_type=annotation.Transaction,
                                    signing_accounts=[self.genesis]
                                    )
        tx = await self.get_last_tx()

        expected = (
            tx.hash(),
            tx.version,
            tx.nonce,
            tx.sender,
            tx.system_fee,
            tx.network_fee,
            tx.valid_until_block,
            tx.script
        )
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    async def test_get_script_container_as_transaction(self):
        await self.set_up_contract('ScriptContainerAsTransaction.py')

        result, _ = await self.call('main',
                                    [],
                                    return_type=annotation.Transaction,
                                    signing_accounts=[self.genesis]
                                    )
        tx = await self.get_last_tx()

        expected = (
            tx.hash(),
            tx.version,
            tx.nonce,
            tx.sender,
            tx.system_fee,
            tx.network_fee,
            tx.valid_until_block,
            tx.script
        )
        self.assertEqual(len(expected), len(result))
        self.assertEqual(expected, result)

    async def test_get_network(self):
        await self.set_up_contract('GetNetwork.py')

        network_protocol = (
            await self.get_version()
        ).protocol

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(network_protocol.network, result)

    def test_get_network_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'GetNetworkTooManyArguments.py')

    async def test_import_runtime(self):
        await self.set_up_contract('ImportRuntime.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertGreater(result, 0)

    async def test_import_interop_runtime(self):
        self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'ImportInteropRuntime.py')
        await self.set_up_contract('ImportInteropRuntime.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertGreater(result, 0)

    async def test_get_random(self):
        await self.set_up_contract('GetRandom.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertGreater(result, 0)

    def test_get_random_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'GetRandomTooManyArguments.py')

    async def test_address_version(self):
        await self.set_up_contract('AddressVersion.py')

        network_protocol = (
            await self.get_version()
        ).protocol

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(network_protocol.address_version, result)

    def test_address_version_cant_assign(self):
        self.assertCompilerLogs(CompilerWarning.NameShadowing, 'AddressVersionCantAssign.py')

    async def test_load_script(self):
        await self.set_up_contract('LoadScriptDynamicCall.py')

        operand_1 = 1
        operand_2 = 2
        expected_result = operand_1 + operand_2
        result, _ = await self.call('dynamic_sum',
                                    [operand_1, operand_2],
                                    return_type=int
                                    )
        self.assertEqual(expected_result, result)

        from boa3.internal.neo3.contracts import CallFlags
        result, _ = await self.call('dynamic_sum_with_flags',
                                    [operand_1, operand_2, CallFlags.READ_ONLY],
                                    return_type=int
                                    )
        self.assertEqual(expected_result, result)

    async def test_script_container_hash(self):
        # test https://github.com/CityOfZion/neo3-boa/issues/1273
        # both import styles must work
        await self.set_up_contract('ScriptContainerHash.py')

        result, _ = await self.call('main', [], return_type=types.UInt256)
        self.assertIsInstance(result, types.UInt256)

        await self.set_up_contract('ScriptContainerHash2.py')
        result, _ = await self.call('main', [], return_type=types.UInt256)
        self.assertIsInstance(result, types.UInt256)

