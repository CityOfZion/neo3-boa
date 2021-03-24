from boa3.boa3 import Boa3
from boa3.builtin.interop.runtime import TriggerType
from boa3.exception.CompilerError import MismatchedTypes
from boa3.exception.CompilerWarning import NameShadowing
from boa3.model.builtin.interop.interop import Interop
from boa3.model.type.type import Type
from boa3.neo import to_script_hash
from boa3.neo.cryptography import hash160
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestRuntimeInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/runtime'

    def test_check_witness(self):
        path = self.get_contract_path('CheckWitness.py')
        account = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', account)
        self.assertEqual(False, result)

        engine.add_signer_account(account)
        result = self.run_smart_contract(engine, path, 'Main', account)
        self.assertEqual(True, result)

    def test_check_witness_imported_as(self):
        path = self.get_contract_path('CheckWitnessImportedAs.py')
        account = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', account)
        self.assertEqual(False, result)

        engine.add_signer_account(account)
        result = self.run_smart_contract(engine, path, 'Main', account)
        self.assertEqual(True, result)

    def test_check_witness_mismatched_type(self):
        path = self.get_contract_path('CheckWitnessMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_notify_str(self):
        event_name = String('notify').to_bytes()
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

        path = self.get_contract_path('NotifyStr.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((message,), event_notifications[0].arguments)

    def test_notify_int(self):
        event_name = String('notify').to_bytes()
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

        path = self.get_contract_path('NotifyInt.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((15,), event_notifications[0].arguments)

    def test_notify_bool(self):
        event_name = String('notify').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.SWAP
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('NotifyBool.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((1,), event_notifications[0].arguments)

    def test_notify_none(self):
        event_name = String('notify').to_bytes()
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

        path = self.get_contract_path('NotifyNone.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((None,), event_notifications[0].arguments)

    def test_notify_sequence(self):
        event_name = String('notify').to_bytes()
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

        path = self.get_contract_path('NotifySequence.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual(([2, 3, 5, 7],), event_notifications[0].arguments)

    def test_notify_with_name(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.PUSH10
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.SWAP
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('NotifyWithName.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'unit_test')
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name='unit_test')
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((10,), event_notifications[0].arguments)

    def test_log_mismatched_type(self):
        path = self.get_contract_path('LogMismatchedValueInt.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_log_str(self):
        string = String('str').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.Log.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('LogStr.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_get_trigger(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('Trigger.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(TriggerType.APPLICATION, result)

    def test_is_application_trigger(self):
        application = Integer(TriggerType.APPLICATION.value).to_byte_array()
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.PUSHDATA1
            + Integer(len(application)).to_byte_array(min_length=1)
            + application
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.EQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('TriggerApplication.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_is_verification_trigger(self):
        verification = Integer(TriggerType.VERIFICATION.value).to_byte_array()
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.PUSHDATA1
            + Integer(len(verification)).to_byte_array(min_length=1)
            + verification
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.EQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('TriggerVerification.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(False, result)

    def test_get_calling_script_hash(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.CallingScriptHash.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('CallingScriptHash.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_calling_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('CallingScriptHashCantAssign.py')
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_executing_script_hash(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.ExecutingScriptHash.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('ExecutingScriptHash.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_executing_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('ExecutingScriptHashCantAssign.py')
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_block_time(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.BlockTime.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('BlockTime.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        new_block = engine.increase_block()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(new_block.timestamp, result)

    def test_block_time_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('BlockTimeCantAssign.py')
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_gas_left(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.GasLeft.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('GasLeft.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_gas_left_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('GasLeftCantAssign.py')
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_invocation_counter(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.InvocationCounter.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('InvocationCounter.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_invocation_counter_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('InvocationCounterCantAssign.py')
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_notifications(self):
        path = self.get_contract_path('GetNotifications.py')
        output, manifest = self.compile_and_save(path)
        script = hash160(output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'without_param', [])
        self.assertEqual([], result)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'without_param', [1, 2, 3])
        expected_result = []
        for x in [1, 2, 3]:
            expected_result.append([script,
                                    'notify',
                                    [x]])
        self.assertEqual(expected_result, result)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'with_param', [], script)
        self.assertEqual([], result)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'with_param', [1, 2, 3], script)
        expected_result = []
        for x in [1, 2, 3]:
            expected_result.append([script,
                                    'notify',
                                    [x]])
        self.assertEqual(expected_result, result)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'with_param', [1, 2, 3], b'\x01' * 20)
        self.assertEqual([], result)

    def test_get_entry_script_hash(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.EntryScriptHash.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('EntryScriptHash.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_entry_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('EntryScriptHashCantAssign.py')
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_platform(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.Platform.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('GetPlatform.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual('NEO', result)

    def test_get_platform_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('GetPlatformCantAssign.py')
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_boa2_runtime_test(self):
        path = self.get_contract_path('RuntimeBoa2Test.py')
        engine = TestEngine()

        new_block = engine.increase_block()
        result = self.run_smart_contract(engine, path, 'main', 'get_time', 1)
        self.assertEqual(new_block.timestamp, result)

        from boa3.builtin.type import UInt160
        result = self.run_smart_contract(engine, path, 'main', 'check_witness', UInt160(bytes(20)))
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', 'log', 'hello')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', 'notify', 1234)
        self.assertEqual(True, result)
        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((1234,), event_notifications[0].arguments)

        result = self.run_smart_contract(engine, path, 'main', 'get_trigger', 1234)
        self.assertEqual(TriggerType.APPLICATION, result)

    def test_boa2_trigger_type_test(self):
        path = self.get_contract_path('TriggerTypeBoa2Test.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 1)
        self.assertEqual(0x40, result)

        result = self.run_smart_contract(engine, path, 'main', 2)
        self.assertEqual(0x20, result)

        result = self.run_smart_contract(engine, path, 'main', 3)
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(b'\x20', result)

        result = self.run_smart_contract(engine, path, 'main', 0)
        self.assertEqual(-1, result)
