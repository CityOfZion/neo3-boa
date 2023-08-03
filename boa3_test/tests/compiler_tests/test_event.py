from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestEvent(BoaTest):
    default_folder: str = 'test_sc/event_test'

    def test_event_without_arguments(self):
        event_id = 'Event'
        event_name = String(event_id).to_bytes(min_length=1)
        expected_output = (
            Opcode.NEWARRAY0    # Main()
            + Opcode.PUSHDATA1      # event()
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET       # return
        )

        path = self.get_contract_path('EventWithoutArguments.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())
        invoke = runner.call_contract(path, 'Main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNone(invoke.result)
        self.assertGreater(len(runner.notifications), 0)

        event_notifications = runner.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((), event_notifications[0].arguments)

    def test_event_with_arguments(self):
        event_id = 'Event'
        event_name = String(event_id).to_bytes(min_length=1)
        expected_output = (
            Opcode.PUSH10        # Main()
            + Opcode.PUSH1          # event(10)
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET       # return
        )

        path = self.get_contract_path('EventWithArgument.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())
        invoke = runner.call_contract(path, 'Main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNone(invoke.result)
        self.assertGreater(len(runner.notifications), 0)

        event_notifications = runner.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((10,), event_notifications[0].arguments)

    def test_event_with_name(self):
        event_id = 'example'
        event_name = String(event_id).to_bytes(min_length=1)
        expected_output = (
            Opcode.PUSH10       # Main()
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1      # event(10)
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET      # return
        )

        path = self.get_contract_path('EventWithName.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())
        invoke = runner.call_contract(path, 'Main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNone(invoke.result)
        self.assertGreater(len(runner.notifications), 0)

        event_notifications = runner.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((10,), event_notifications[0].arguments)

    def test_event_with_annotation(self):
        event_id = 'example'
        event_name = String(event_id).to_bytes(min_length=1)
        expected_output = (
            Opcode.PUSH10       # Main()
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1      # on_example(10)
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET      # return
        )

        path = self.get_contract_path('EventWithAnnotation.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())
        invoke = runner.call_contract(path, 'Main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNone(invoke.result)
        self.assertGreater(len(runner.notifications), 0)

        event_notifications = runner.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((10,), event_notifications[0].arguments)

    def test_event_nep17_transfer(self):
        event_id = 'Transfer'
        event_name = String(event_id).to_bytes(min_length=1)
        expected_output = (
            Opcode.INITSLOT     # Main()
            + b'\x00\x03'
            + Opcode.LDARG2         # event(from_addr, to_addr, amount)
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET       # return
        )

        path = self.get_contract_path('EventNep17Transfer.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())
        invoke = runner.call_contract(path, 'Main', b'1', b'2', 10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNone(invoke.result)
        self.assertGreater(len(runner.notifications), 0)

        event_notifications = runner.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual(('1', '2', 10), event_notifications[0].arguments)

    def test_event_nep17_transfer_built(self):
        event_id = 'Transfer'
        event_name = String(event_id).to_bytes(min_length=1)
        expected_output = (
            Opcode.INITSLOT     # Main()
            + b'\x00\x03'
            + Opcode.LDARG2         # event(from_addr, to_addr, amount)
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET       # return
        )

        path = self.get_contract_path('EventNep17TransferBuilt.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())
        invoke = runner.call_contract(path, 'Main', b'1', b'2', 10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNone(invoke.result)
        self.assertGreater(len(runner.notifications), 0)

        event_notifications = runner.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual(('1', '2', 10), event_notifications[0].arguments)

    def test_event_nep11_transfer(self):
        event_id = 'Transfer'
        event_name = String(event_id).to_bytes(min_length=1)
        expected_output = (
            Opcode.INITSLOT     # Main()
            + b'\x00\x04'
            + Opcode.LDARG3         # event(from_addr, to_addr, amount, token_id)
            + Opcode.LDARG2
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.RET       # return
        )

        path = self.get_contract_path('EventNep11Transfer.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())
        invoke = runner.call_contract(path, 'Main', b'1', b'2', 10, b'someToken')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNone(invoke.result)
        self.assertGreater(len(runner.notifications), 0)

        event_notifications = runner.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual(('1', '2', 10, 'someToken'), event_notifications[0].arguments)

    def test_event_with_return(self):
        path = self.get_contract_path('EventWithoutTypes.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_event_with_duplicated_name(self):
        path, _ = self.get_deploy_file_paths('EventWithDuplicatedName.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        arg = 10
        event_id = 'example'
        invoke = runner.call_contract(path, 'example', arg)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNone(invoke.result)
        self.assertGreater(len(runner.notifications), 0)

        event_notifications = runner.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((arg,), event_notifications[0].arguments)

    def test_event_call_too_many_arguments(self):
        path = self.get_contract_path('TooManyArgumentsCallEvent.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_event_call_too_few_arguments(self):
        path = self.get_contract_path('TooFewArgumentsCallEvent.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_event_call_mismatched_type_integer(self):
        path = self.get_contract_path('MismatchedTypeCallEventInteger.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_call_mismatched_type_boolean(self):
        path = self.get_contract_path('MismatchedTypeCallEventBoolean.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_call_mismatched_type_hash160(self):
        path = self.get_contract_path('MismatchedTypeCallEventHash160.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_call_mismatched_type_hash256(self):
        path = self.get_contract_path('MismatchedTypeCallEventHash256.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_call_mismatched_type_bytearray(self):
        path = self.get_contract_path('MismatchedTypeCallEventByteArray.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_call_mismatched_type_public_key(self):
        path = self.get_contract_path('MismatchedTypeCallEventPublicKey.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_call_mismatched_type_string(self):
        path = self.get_contract_path('MismatchedTypeCallEventString.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_call_mismatched_type_array(self):
        path = self.get_contract_path('MismatchedTypeCallEventArray.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_call_mismatched_type_map(self):
        path = self.get_contract_path('MismatchedTypeCallEventMap.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_with_interop_interface_argument_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeCreateEventWithInteropInterface.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_event_with_abort(self):
        path = self.get_contract_path('EventWithAbort.py')
        self.compile_and_save(path)
        path, _ = self.get_deploy_file_paths(path)

        runner = BoaTestRunner(runner_id=self.method_name())
        runner.call_contract(path, 'send_event_with_abort')
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ABORTED_CONTRACT_MSG)
        self.assertGreater(len(runner.notifications), 0)

        invoke = runner.call_contract(path, 'send_event')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsNone(invoke.result)
        self.assertGreater(len(runner.notifications), 0)

    def test_boa2_event_test(self):
        path, _ = self.get_deploy_file_paths('EventBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())
        invoke = runner.call_contract(path, 'main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        result = invoke.result
        self.assertIsNotNone(result)
        self.assertEqual(7, result)

        event_notifications1 = runner.get_events('transfer_test')
        self.assertEqual(1, len(event_notifications1))
        self.assertEqual(3, len(event_notifications1[0].arguments))
        from_address, to_address, amount = event_notifications1[0].arguments
        self.assertEqual(2, from_address)
        self.assertEqual(5, to_address)
        self.assertEqual(7, amount)

        event_notifications2 = runner.get_events('refund')
        self.assertEqual(1, len(event_notifications2))
        self.assertEqual(2, len(event_notifications2[0].arguments))
        to_address, amount = event_notifications2[0].arguments
        self.assertEqual('me', to_address)
        self.assertEqual(52, amount)
