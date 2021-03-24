from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, UnfilledArgument
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=event_id)
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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=event_id)
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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((10,), event_notifications[0].arguments)

    def test_event_nep5_transfer(self):
        event_id = 'transfer'
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

        path = self.get_contract_path('EventNep5Transfer.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', b'1', b'2', 10)
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual(('1', '2', 10), event_notifications[0].arguments)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', b'1', b'2', 10)
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=event_id)
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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', b'1', b'2', 10)
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual(('1', '2', 10), event_notifications[0].arguments)

    def test_event_with_return(self):
        path = self.get_contract_path('EventWithoutTypes.py')
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_event_call_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeCallEvent.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_boa2_event_test(self):
        path = self.get_contract_path('EventBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(7, result)

        event_notifications1 = engine.get_events('transfer_test')
        self.assertEqual(1, len(event_notifications1))
        self.assertEqual(3, len(event_notifications1[0].arguments))
        from_address, to_address, amount = event_notifications1[0].arguments
        self.assertEqual(2, from_address)
        self.assertEqual(5, to_address)
        self.assertEqual(7, amount)

        event_notifications2 = engine.get_events('refund')
        self.assertEqual(1, len(event_notifications2))
        self.assertEqual(2, len(event_notifications2[0].arguments))
        to_address, amount = event_notifications2[0].arguments
        self.assertEqual('me', to_address)
        self.assertEqual(52, amount)
