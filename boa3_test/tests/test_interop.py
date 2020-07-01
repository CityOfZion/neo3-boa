from boa3.boa3 import Boa3
from boa3.builtin.interop.runtime import TriggerType
from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.builtin.interop.interop import Interop
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestInterop(BoaTest):

    def test_check_witness(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.CheckWitness.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/example/interop_test/CheckWitness.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_witness_imported_as(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.CheckWitness.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/example/interop_test/CheckWitnessImportedAs.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_witness_mismatched_type(self):
        path = '%s/boa3_test/example/interop_test/CheckWitnessMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_notify_str(self):
        string = String('str').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/example/interop_test/NotifyStr.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_notify_int(self):
        expected_output = (
            Opcode.PUSH15
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/example/interop_test/NotifyInt.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_notify_bool(self):
        expected_output = (
            Opcode.PUSH1
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/example/interop_test/NotifyBool.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_notify_none(self):
        expected_output = (
            Opcode.PUSHNULL
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/example/interop_test/NotifyNone.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_notify_sequence(self):
        expected_output = (
            Opcode.PUSH7
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/example/interop_test/NotifySequence.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_log_mismatched_type(self):
        path = '%s/boa3_test/example/interop_test/LogMismatchedValueInt.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_log_str(self):
        string = String('str').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.Log.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/example/interop_test/LogStr.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_get_trigger(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/example/interop_test/Trigger.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/example/interop_test/TriggerApplication.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

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

        path = '%s/boa3_test/example/interop_test/TriggerVerification.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)
