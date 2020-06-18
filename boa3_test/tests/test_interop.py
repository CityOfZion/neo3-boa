from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.builtin.interopmethods.interop import Interop
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest


class TestInterop(BoaTest):

    def test_check_witness(self):
        path = '%s/boa3_test/example/interop_test/CheckWitness.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.CheckWitness.interop_method_hash
            + Opcode.RET
        )

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_witness_imported_as(self):
        path = '%s/boa3_test/example/interop_test/CheckWitnessImportedAs.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.CheckWitness.interop_method_hash
            + Opcode.RET
        )

        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_witness_mismatched_type(self):
        path = '%s/boa3_test/example/interop_test/CheckWitnessMismatchedValue.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
