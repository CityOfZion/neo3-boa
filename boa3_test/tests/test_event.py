from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, UnfilledArgument
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestEvent(BoaTest):

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

        path = '%s/boa3_test/test_sc/event_test/EventWithoutArguments.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
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

        path = '%s/boa3_test/test_sc/event_test/EventWithArgument.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
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

        path = '%s/boa3_test/test_sc/event_test/EventWithName.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
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

        path = '%s/boa3_test/test_sc/event_test/EventNep5Transfer.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', b'1', b'2', 10)
        self.assertIsVoid(result)
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=event_id)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual(('1', '2', 10), event_notifications[0].arguments)

    def test_event_with_return(self):
        path = '%s/boa3_test/test_sc/event_test/EventWithoutTypes.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_event_call_mismatched_type(self):
        path = '%s/boa3_test/test_sc/event_test/MismatchedTypeCallEvent.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
