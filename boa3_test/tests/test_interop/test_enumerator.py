from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.core.types.InteropInterface import InteropInterface
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestEnumeratorInterop(BoaTest):

    def test_create_enumerator_list(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\00'
            + b'\01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.EnumeratorCreate.interop_method_hash
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/interop_test/enumerator/EnumeratorCreateList.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'list_enumerator', [])
        self.assertEqual(InteropInterface, result)  # returns an interop interface

        result = self.run_smart_contract(engine, path, 'list_enumerator', [1, 2, 3])
        self.assertEqual(InteropInterface, result)  # returns an interop interface

    def test_create_enumerator_tuple(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\00'
            + b'\01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.EnumeratorCreate.interop_method_hash
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/interop_test/enumerator/EnumeratorCreateTuple.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'tuple_enumerator', ())
        self.assertEqual(InteropInterface, result)  # returns an interop interface

        result = self.run_smart_contract(engine, path, 'tuple_enumerator', (1, 2, 3))
        self.assertEqual(InteropInterface, result)  # returns an interop interface

    def test_create_enumerator_int(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\00'
            + b'\01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.EnumeratorCreate.interop_method_hash
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/interop_test/enumerator/EnumeratorCreateInt.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'int_enumerator', 42)
        self.assertEqual(InteropInterface, result)  # returns an interop interface

        result = self.run_smart_contract(engine, path, 'int_enumerator', 123456)
        self.assertEqual(InteropInterface, result)  # returns an interop interface

    def test_create_enumerator_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/enumerator/EnumeratorCreateMismatchedTypes.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
