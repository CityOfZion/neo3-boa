from boa3.exception import CompilerError
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestIteratorInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/iterator'

    def test_iterator_create(self):
        path = self.get_contract_path('IteratorCreate.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_iterator_next(self):
        path = self.get_contract_path('IteratorNext.py')
        self.compile_and_save(path)

        engine = TestEngine()

        prefix = 'test_iterator_next'
        result = self.run_smart_contract(engine, path, 'has_next', prefix)
        self.assertEqual(False, result)

        engine.storage_put(prefix + 'example1', 1, contract_path=path)
        result = self.run_smart_contract(engine, path, 'has_next', prefix)
        self.assertEqual(True, result)

    def test_iterator_value(self):
        path = self.get_contract_path('IteratorValue.py')
        self.compile_and_save(path)

        engine = TestEngine()

        prefix = 'test_iterator_value'
        result = self.run_smart_contract(engine, path, 'test_iterator', prefix)
        self.assertIsNone(result)

        key = prefix + 'example1'
        engine.storage_put(key, 1, contract_path=path)
        result = self.run_smart_contract(engine, path, 'test_iterator', prefix)
        self.assertEqual([key, '\x01'], result)

    def test_iterator_value_dict_mismatched_type(self):
        path = self.get_contract_path('IteratorValueMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
