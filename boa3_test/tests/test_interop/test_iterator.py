from boa3.exception.CompilerError import MismatchedTypes
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.core.types.InteropInterface import InteropInterface
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestIteratorInterop(BoaTest):

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
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorCreateList.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
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
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorCreateDict.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'dict_iterator', {})
        self.assertEqual(InteropInterface, result)  # returns an interop interface

        result = self.run_smart_contract(engine, path, 'dict_iterator', {1: 2, 2: 4, 3: 6})
        self.assertEqual(InteropInterface, result)  # returns an interop interface

    def test_create_iterator_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorCreateMismatchedTypes.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_iterator_next(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorNext.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'has_next', [1])
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'has_next', [])
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'has_next', {1: 2, 2: 4})
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'has_next', {})
        self.assertEqual(False, result)

    def test_iterator_value(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorValue.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'list_iterator', [1])
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'list_iterator', [])
        self.assertIsNone(result)

        result = self.run_smart_contract(engine, path, 'dict_iterator', {1: 5, 7: 9})
        self.assertEqual(5, result)

        result = self.run_smart_contract(engine, path, 'dict_iterator', {})
        self.assertIsNone(result)

    def test_iterator_value_dict_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorDictValueMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_iterator_value_list_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorListValueMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_iterator_key(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorKey.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'list_iterator', [1])
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'list_iterator', [])
        self.assertIsNone(result)

        result = self.run_smart_contract(engine, path, 'dict_iterator', {'1': 5, '7': 9})
        self.assertEqual('1', result)

        result = self.run_smart_contract(engine, path, 'dict_iterator', {})
        self.assertIsNone(result)

    def test_iterator_key_dict_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorDictKeyMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_iterator_key_list_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorListKeyMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_iterator_concat(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorConcat.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'concat_iterators', [1], {'1': 5, '7': 9})
        self.assertEqual(InteropInterface, result)  # returns an interop interface

        result = self.run_smart_contract(engine, path, 'concat_and_get_result', [1], {'1': 5, '7': 9})
        self.assertEqual({0: 1, '1': 5, '7': 9}, result)

    def test_iterator_concat_with_defined_types(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorConcatWithDefinedTypes.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'concat_iterators',
                                         ['1', '2', '3'], {1: False, 10: True})
        self.assertEqual(InteropInterface, result)  # returns an interop interface

        result = self.run_smart_contract(engine, path, 'concat_and_get_result',
                                         ['1', '2', '3'], {1: False, 10: True})
        self.assertEqual({0: '1', 1: '2', 2: '3', 10: True}, result)

        result = self.run_smart_contract(engine, path, 'concat_and_get_result',
                                         ['1', '2', '3'], {5: False, 10: True})
        self.assertEqual({0: '1', 1: '2', 2: '3', 5: False, 10: True}, result)

    def test_iterator_concat_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorConcatMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_iterator_values(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorValues.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'list_iterator', [1])
        self.assertEqual(InteropInterface, result)
        # TODO: validate actual result when Enumerator.next() and Enumerator.value() are implemented

        result = self.run_smart_contract(engine, path, 'list_iterator', [])
        self.assertIsNone(result)

        result = self.run_smart_contract(engine, path, 'dict_iterator', {1: 5, 7: 9})
        self.assertEqual(InteropInterface, result)
        # TODO: validate actual result when Enumerator.next() and Enumerator.value() are implemented

        result = self.run_smart_contract(engine, path, 'dict_iterator', {})
        self.assertIsNone(result)

    def test_iterator_values_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorValuesMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_iterator_keys(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorKeys.py' % self.dirname
        self.compile_and_save(path)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'list_iterator', [1])
        self.assertEqual(InteropInterface, result)
        # TODO: validate actual result when Enumerator.next() and Enumerator.value() are implemented

        result = self.run_smart_contract(engine, path, 'list_iterator', [])
        self.assertIsNone(result)

        result = self.run_smart_contract(engine, path, 'dict_iterator', {1: 5, 7: 9})
        self.assertEqual(InteropInterface, result)
        # TODO: validate actual result when Enumerator.next() and Enumerator.value() are implemented

        result = self.run_smart_contract(engine, path, 'dict_iterator', {})
        self.assertIsNone(result)

    def test_iterator_keys_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/iterator/IteratorKeysMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
