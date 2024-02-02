from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestEvent(boatestcase.BoaTestCase):
    from boa3.internal.model.builtin.interop.interop import Interop

    default_folder: str = 'test_sc/event_test'
    notify_syscall = Interop.Notify.interop_method_hash

    def test_event_without_arguments(self):
        event_id = 'Event'
        event_name = String(event_id).to_bytes(min_length=1)
        expected_output = (
            Opcode.NEWARRAY0    # Main()
            + Opcode.PUSHDATA1      # event()
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + self.notify_syscall
            + Opcode.RET       # return
        )

        output, _ = self.assertCompile('EventWithoutArguments.py')
        self.assertEqual(expected_output, output)

    async def test_event_without_arguments_run(self):
        await self.set_up_contract('EventWithoutArguments.py')

        result, events = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        self.assertEqual(1, len(events))
        event = boatestcase.TestEvent.from_notification(events[0])
        self.assertEqual((), event.state)

    def test_event_with_arguments_compile(self):
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
            + self.notify_syscall
            + Opcode.RET       # return
        )

        output, _ = self.assertCompile('EventWithArgument.py')
        self.assertEqual(expected_output, output)

    async def test_event_with_arguments_run(self):
        await self.set_up_contract('EventWithArgument.py')

        result, events = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)
        self.assertGreater(len(events), 0)

        self.assertEqual(1, len(events))
        event = boatestcase.TestEvent.from_notification(events[0], int)
        self.assertEqual((10,), event.state)

    def test_event_with_name_compile(self):
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
            + self.notify_syscall
            + Opcode.RET      # return
        )

        output, _ = self.assertCompile('EventWithName.py')
        self.assertEqual(expected_output, output)

    async def test_event_with_name_run(self):
        await self.set_up_contract('EventWithName.py')

        result, events = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        self.assertEqual(1, len(events))
        event = boatestcase.TestEvent.from_notification(events[0], int)
        self.assertEqual((10,), event.state)

    def test_event_with_annotation_compile(self):
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
            + self.notify_syscall
            + Opcode.RET      # return
        )

        output, _ = self.assertCompile('EventWithAnnotation.py')
        self.assertEqual(expected_output, output)

    async def test_event_with_annotation(self):
        await self.set_up_contract('EventWithAnnotation.py')

        result, events = await self.call('Main', [], return_type=None)
        self.assertIsNone(result)

        self.assertEqual(1, len(events))
        event = boatestcase.TestEvent.from_notification(events[0], int)
        self.assertEqual((10,), event.state)

    def test_event_nep17_transfer_compile(self):
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
            + self.notify_syscall
            + Opcode.RET       # return
        )

        output, _ = self.assertCompile('EventNep17Transfer.py')
        self.assertEqual(expected_output, output)

    async def test_event_nep17_transfer_run(self):
        await self.set_up_contract('EventNep17Transfer.py')

        transfer_args = b'1', b'2', 10
        result, events = await self.call('Main', [*transfer_args], return_type=None)
        self.assertIsNone(result)

        self.assertEqual(1, len(events))
        event = boatestcase.TestEvent.from_notification(events[0], bytes, bytes, int)
        self.assertEqual(transfer_args, event.state)

    def test_event_nep17_transfer_built_compile(self):
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
            + self.notify_syscall
            + Opcode.RET       # return
        )

        output, _ = self.assertCompile('EventNep17TransferBuilt.py')
        self.assertEqual(expected_output, output)

    async def test_event_nep17_transfer_built_run(self):
        await self.set_up_contract('EventNep17TransferBuilt.py')

        transfer_args = b'1', b'2', 10
        result, events = await self.call('Main', [*transfer_args], return_type=None)
        self.assertIsNone(result)

        self.assertEqual(1, len(events))
        event = boatestcase.TestEvent.from_notification(events[0], bytes, bytes, int)
        self.assertEqual(transfer_args, event.state)

    def test_event_nep11_transfer_compile(self):
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
            + self.notify_syscall
            + Opcode.RET       # return
        )

        output, _ = self.assertCompile('EventNep11Transfer.py')
        self.assertEqual(expected_output, output)

    async def test_event_nep11_transfer_run(self):
        await self.set_up_contract('EventNep11Transfer.py')

        transfer_args = b'1', b'2', 10, b'someToken'
        result, events = await self.call('Main', [*transfer_args], return_type=None)
        self.assertIsNone(result)

        self.assertEqual(1, len(events))
        event = boatestcase.TestEvent.from_notification(events[0], bytes, bytes, int, bytes)
        self.assertEqual(transfer_args, event.state)

    def test_event_without_types(self):
        path = self.get_contract_path('EventWithoutTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_event_with_duplicated_name(self):
        await self.set_up_contract('EventWithDuplicatedName.py')

        arg = 10
        event_id = 'example'
        result, events = await self.call('example', [arg], return_type=None)
        self.assertIsNone(result)

        self.assertEqual(1, len(events))
        event = boatestcase.TestEvent.from_notification(events[0], int)
        self.assertEqual((arg,), event.state)

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

    async def test_event_with_abort(self):
        await self.set_up_contract('EventWithAbort.py')

        result, events = await self.call('send_event', [], return_type=None)
        self.assertIsNone(result)

        self.assertEqual(1, len(events))
        event = boatestcase.TestEvent.from_notification(events[0], int)
        self.assertEqual((10,), event.state)

        with self.assertRaises(boatestcase.AbortException):
            await self.call('send_event_with_abort', [], return_type=None)

    async def test_boa2_event_test(self):
        await self.set_up_contract('EventBoa2Test.py')

        result, events = await self.call('main', [], return_type=int)
        self.assertEqual(7, result)

        self.assertEqual(2, len(events))
        transfer_event = boatestcase.TestEvent.from_notification(events[0], int, int, int)
        refund_event = boatestcase.TestEvent.from_notification(events[1], str, int)

        self.assertEqual('transfer_test', transfer_event.name)
        self.assertEqual((2, 5, 7), transfer_event.state)

        self.assertEqual('refund', refund_event.name)
        self.assertEqual(('me', 52), refund_event.state)
