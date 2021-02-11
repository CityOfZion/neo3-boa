from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.core.types.InteropInterface import InteropInterface
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestIteratorInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/iterator'

    def test_create_iterator_list(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\00'
            + b'\01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.IteratorCreate.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('IteratorCreateList.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'list_iterator', [])
        self.assertEqual(InteropInterface, result)  # returns an interop interface

        result = self.run_smart_contract(engine, path, 'list_iterator', [1, 2, 3])
        self.assertEqual(InteropInterface, result)  # returns an interop interface

    def test_create_iterator_dict(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\00'
            + b'\01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.IteratorCreate.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('IteratorCreateDict.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'dict_iterator', {})
        self.assertEqual(InteropInterface, result)  # returns an interop interface

        result = self.run_smart_contract(engine, path, 'dict_iterator', {1: 2, 2: 4, 3: 6})
        self.assertEqual(InteropInterface, result)  # returns an interop interface

    def test_create_iterator_mismatched_type(self):
        path = self.get_contract_path('IteratorCreateMismatchedTypes.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_iterator_next(self):
        path = self.get_contract_path('IteratorNext.py')
        self.compile_and_save(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'has_next', [1])
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'has_next', [])
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'has_next', {1: 2, 2: 4})
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'has_next', {})
        self.assertEqual(False, result)

    def test_iterator_value(self):
        path = self.get_contract_path('IteratorValue.py')
        self.compile_and_save(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'list_iterator', [1])
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'list_iterator', [])
        self.assertIsNone(result)

        result = self.run_smart_contract(engine, path, 'dict_iterator', {1: 5, 7: 9})
        self.assertEqual([1, 5], result)

        result = self.run_smart_contract(engine, path, 'dict_iterator', {})
        self.assertIsNone(result)

    def test_iterator_value_dict_mismatched_type(self):
        path = self.get_contract_path('IteratorDictValueMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_iterator_value_list_mismatched_type(self):
        path = self.get_contract_path('IteratorListValueMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)
