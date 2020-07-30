from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.exception.CompilerWarning import UnreachableCode
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestEvent(BoaTest):

    def test_event_without_arguments(self):
        event_name = String('Event').to_bytes(min_length=1)
        expected_output = (
            Opcode.NEWARRAY0    # Main()
            + Opcode.PUSHDATA1      # event()
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL       # return
            + Opcode.RET
        )

        path = '%s/boa3_test/example/event_test/EventWithoutArguments.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_event_with_arguments(self):
        event_name = String('Event').to_bytes(min_length=1)
        expected_output = (
            Opcode.PUSH10        # Main()
            + Opcode.PUSH1          # event(10)
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL       # return
            + Opcode.RET
        )

        path = '%s/boa3_test/example/event_test/EventWithArgument.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_event_with_body(self):
        event_name = String('Event').to_bytes(min_length=1)
        expected_output = (
            Opcode.PUSH10       # Main()
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1      # event(10)
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL       # return
            + Opcode.RET
        )

        path = '%s/boa3_test/example/event_test/EventWithBody.py' % self.dirname
        output = self.assertCompilerLogs(UnreachableCode, path)
        self.assertEqual(expected_output, output)

    def test_event_with_return(self):
        path = '%s/boa3_test/example/event_test/EventWithReturnType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_event_call_mismatched_type(self):
        path = '%s/boa3_test/example/event_test/MismatchedTypeCallEvent.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
