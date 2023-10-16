from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.contracts import TriggerType
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestRuntimeInterop(BoaTest):
    default_folder: str = 'test_sc/interop_test/runtime'

    def test_check_witness(self):
        path, _ = self.get_deploy_file_paths('CheckWitness.py')
        account = neoxp.utils.get_account_by_name('testAccount1')
        account_hash = account.script_hash.to_array()
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', account_hash))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'Main', account_hash))
        expected_results.append(True)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_contract_with_check_witness(self):
        path, _ = self.get_deploy_file_paths('test_sc/interop_test/contract', 'CallScriptHash.py')
        call_contract_path, _ = self.get_deploy_file_paths('CheckWitness.py')
        account = neoxp.utils.get_account_by_name('testAccount1')
        account_hash = account.script_hash.to_array()
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        contract_method = 'Main'
        contract_args = [account_hash]
        first_call = runner.call_contract(call_contract_path, contract_method, *contract_args)
        invokes.append(first_call)
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        contract_hash = first_call.invoke.contract.script_hash

        invokes.append(runner.call_contract(call_contract_path, contract_method, *contract_args))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main',
                                            contract_hash, contract_method, contract_args))
        expected_results.append(False)  # fail because the signer have CalledByEntry scope

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_check_witness_imported_as(self):
        path, _ = self.get_deploy_file_paths('CheckWitnessImportedAs.py')
        account = neoxp.utils.get_account_by_name('testAccount1')
        account_hash = account.script_hash.to_array()
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', account_hash))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'Main', account_hash))
        expected_results.append(True)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_check_witness_mismatched_type(self):
        path = self.get_contract_path('CheckWitnessMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        event_notifications = runner.get_events(event_name=Interop.Notify.name)
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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        event_notifications = runner.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((15,), event_notifications[0].arguments)

    def test_notify_bool(self):
        event_name = String('notify').to_bytes()
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

        path = self.get_contract_path('NotifyBool.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        event_notifications = runner.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((True,), event_notifications[0].arguments)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        event_notifications = runner.get_events(event_name=Interop.Notify.name)
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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        event_notifications = runner.get_events(event_name=Interop.Notify.name)
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

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'unit_test'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        event_notifications = runner.get_events(event_name='unit_test')
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((10,), event_notifications[0].arguments)

    def test_log_mismatched_type(self):
        path = self.get_contract_path('LogMismatchedValueInt.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_trigger(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('Trigger.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(TriggerType.APPLICATION)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_is_application_trigger(self):
        application = Integer(TriggerType.APPLICATION.value).to_byte_array()
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.PUSHINT8 + application
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('TriggerApplication.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_is_verification_trigger(self):
        verification = Integer(TriggerType.VERIFICATION.value).to_byte_array()
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.PUSHINT8 + verification
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        path = self.get_contract_path('TriggerVerification.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_calling_script_hash(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.CallingScriptHash.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('CallingScriptHash.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        contract_call = runner.call_contract(path, 'Main',
                                             expected_result_type=bytes)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # cannot get calling script hash directly from test runner to check the value
        result = contract_call.result
        self.assertIsInstance(result, bytes)
        self.assertEqual(constants.SIZE_OF_INT160, len(result))

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
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_executing_script_hash(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.ExecutingScriptHash.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('ExecutingScriptHash.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        contract = runner.deploy_contract(path)
        invoke = runner.call_contract(path, 'Main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(contract.script_hash, invoke.result)

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
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_executing_script_hash_on_deploy(self):
        path, _ = self.get_deploy_file_paths('ExecutingScriptHashOnDeploy.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        call = runner.call_contract(path, 'get_script')
        runner.update_contracts(export_checkpoint=True)
        invokes.append(call)
        expected_results.append(call.invoke.contract.script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_block_time(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.BlockTime.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('BlockTime.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke_1 = runner.run_contract(path, 'Main')
        invoke_2 = runner.call_contract(path, 'Main')
        runner.execute()

        # Test Runner has an error when returning block time
        # it returns None instead of the actual timestamp and raises NullPointerException
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.NULL_POINTER_MSG)

        self.assertIsNotNone(invoke_1.tx_id)
        invoke_tx = runner.get_transaction_result(invoke_1.tx_id)
        self.assertEqual(1, len(invoke_tx.executions))

        tx_result = invoke_tx.executions[0]
        self.assertEqual(VMState.HALT, tx_result.vm_state)
        self.assertEqual(1, len(tx_result.result_stack))
        self.assertGreater(tx_result.result_stack[0], 0)

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
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_gas_left(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.GasLeft.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('GasLeft.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'Main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsInstance(invoke.result, int)

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
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_invocation_counter(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.InvocationCounter.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('InvocationCounter.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'Main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(1, invoke.result)

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
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_notifications(self):
        path, _ = self.get_deploy_file_paths('GetNotifications.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        notify_call = runner.call_contract(path, 'without_param', [])
        runner.update_contracts(export_checkpoint=True)

        script = notify_call.invoke.contract.script_hash
        invokes.append(notify_call)
        expected_results.append([])

        invokes.append(runner.call_contract(path, 'without_param', [1, 2, 3]))
        expected_result_1 = []
        for x in [1, 2, 3]:
            expected_result_1.append([script, 'notify', [x]])
        expected_results.append(expected_result_1)

        invokes.append(runner.call_contract(path, 'with_param', [], constants.MANAGEMENT_SCRIPT))
        expected_results.append([])

        invokes.append(runner.call_contract(path, 'with_param', [1, 2, 3], script))
        expected_result_2 = []
        for x in [1, 2, 3]:
            expected_result_2.append([script, 'notify', [x]])
        expected_results.append(expected_result_1 + expected_result_2)

        invokes.append(runner.call_contract(path, 'with_param', [1, 2, 3], b'\x01' * 20))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_entry_script_hash(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.EntryScriptHash.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('EntryScriptHash.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        result = invoke.result
        self.assertIsInstance(result, bytes)
        self.assertEqual(len(result), constants.SIZE_OF_INT160)

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
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_platform(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.Platform.getter.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('Platform.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append('NEO')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_platform_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('PlatformCantAssign.py')
        output = self.assertCompilerLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_burn_gas(self):
        path, _ = self.get_deploy_file_paths('BurnGas.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        burned_gas_1 = 1 * 10 ** 8  # 1 GAS
        invokes.append(runner.call_contract(path, 'main', burned_gas_1))
        expected_results.append(None)

        burned_gas_2 = 123 * 10 ** 5  # 0.123 GAS
        invokes.append(runner.call_contract(path, 'main', burned_gas_2))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # can not burn negative GAS
        runner.call_contract(path, 'main', -10 ** 8)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.GAS_MUST_BE_POSITIVE_MSG)

        # can not burn no GAS
        runner.call_contract(path, 'main', 0)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.GAS_MUST_BE_POSITIVE_MSG)

    def test_boa2_runtime_test(self):
        path, _ = self.get_deploy_file_paths('RuntimeBoa2Test.py')
        account = neoxp.utils.get_account_by_name('testAccount1').script_hash.to_array()
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        # Test Runner has an error when returning block time
        # it returns None instead of the actual timestamp and raises NullPointerException
        invoke = runner.call_contract(path, 'main', 'time', 1)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.NULL_POINTER_MSG)

        invokes.append(runner.call_contract(path, 'main', 'check_witness', account))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 'log', 'hello'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 'notify', 1234))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 'get_trigger', 1234))
        expected_results.append(TriggerType.APPLICATION)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        event_notifications = runner.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((1234,), event_notifications[0].arguments)

    def test_boa2_trigger_type_test(self):
        path, _ = self.get_deploy_file_paths('TriggerTypeBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(0x40)

        invokes.append(runner.call_contract(path, 'main', 2))
        expected_results.append(0x20)

        invokes.append(runner.call_contract(path, 'main', 3,
                                            expected_result_type=bytes))
        expected_results.append(b'\x20')

        invokes.append(runner.call_contract(path, 'main', 0))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_script_container(self):
        path, _ = self.get_deploy_file_paths('ScriptContainer.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNotNone(invoke.result)

    def test_get_script_container_as_transaction(self):
        path, _ = self.get_deploy_file_paths('ScriptContainerAsTransaction.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        result = invoke.result

        self.assertEqual(8, len(result))
        if isinstance(result[0], str):
            result[0] = String(result[0]).to_bytes()
        self.assertIsInstance(result[0], bytes)
        self.assertIsInstance(result[1], int)
        self.assertIsInstance(result[2], int)
        if isinstance(result[3], str):
            result[3] = String(result[3]).to_bytes()
        self.assertIsInstance(result[3], bytes)
        self.assertIsInstance(result[4], int)
        self.assertIsInstance(result[5], int)
        self.assertIsInstance(result[6], int)
        if isinstance(result[7], str):
            result[7] = String(result[7]).to_bytes()
        self.assertIsInstance(result[7], bytes)

    def test_get_network(self):
        path, _ = self.get_deploy_file_paths('GetNetwork.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(neoxp.utils.get_magic())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_network_too_many_parameters(self):
        path = self.get_contract_path('GetNetworkTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_import_runtime(self):
        path, _ = self.get_deploy_file_paths('ImportRuntime.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsInstance(invoke.result, int)

    def test_import_interop_runtime(self):
        path, _ = self.get_deploy_file_paths('ImportInteropRuntime.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsInstance(invoke.result, int)

    def test_get_random(self):
        path, _ = self.get_deploy_file_paths('GetRandom.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsInstance(invoke.result, int)

    def test_get_random_too_many_parameters(self):
        path = self.get_contract_path('GetRandomTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_address_version(self):
        path, _ = self.get_deploy_file_paths('AddressVersion.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(53)    # current Neo protocol version is 53

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_address_version_cant_assign(self):
        path = self.get_contract_path('AddressVersionCantAssign.py')
        self.assertCompilerLogs(CompilerWarning.NameShadowing, path)

    def test_load_script(self):
        path, _ = self.get_deploy_file_paths('LoadScriptDynamicCall.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        operand_1 = 1
        operand_2 = 2
        expected_result = operand_1 + operand_2
        invokes.append(runner.call_contract(path, 'dynamic_sum',
                                            operand_1, operand_2))
        expected_results.append(expected_result)

        from boa3.internal.neo3.contracts import CallFlags
        invokes.append(runner.call_contract(path, 'dynamic_sum_with_flags',
                                            operand_1, operand_2, CallFlags.READ_ONLY))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
