from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest


class TestAny(BoaTest):

    def test_variable_none(self):
        path = '%s/boa3_test/test_sc/none_test/VariableNone.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHNULL
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_none_tuple(self):
        path = '%s/boa3_test/test_sc/none_test/NoneTuple.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHNULL   # a = (None, None, None)
            + Opcode.PUSHNULL
            + Opcode.PUSHNULL
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_none_identity(self):
        path = '%s/boa3_test/test_sc/none_test/NoneIdentity.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.ISNULL
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_none_not_identity(self):
        path = '%s/boa3_test/test_sc/none_test/NoneNotIdentity.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.ISNULL
            + Opcode.NOT
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_none_equality(self):
        path = '%s/boa3_test/test_sc/none_test/NoneEquality.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_type_int_operation(self):
        path = '%s/boa3_test/test_sc/none_test/MismatchedTypesInOperation.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_type_assign(self):
        path = '%s/boa3_test/test_sc/none_test/MismatchedTypesAssign.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_type_after_reassign(self):
        path = '%s/boa3_test/test_sc/none_test/MismatchedTypesAfterReassign.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
