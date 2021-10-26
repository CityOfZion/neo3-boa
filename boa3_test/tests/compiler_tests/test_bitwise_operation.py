from boa3.builtin.interop.storage.findoptions import FindOptions
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBitwiseOperation(BoaTest):

    default_folder: str = 'test_sc/bitwise_test/'

    def test_bitwise_or(self):
        path = self.get_contract_path('BitwiseOr.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', FindOptions.REMOVE_PREFIX, FindOptions.KEYS_ONLY, expected_result_type=int)
        intValueToCheck = int(FindOptions.REMOVE_PREFIX | FindOptions.KEYS_ONLY)
        self.assertEqual(intValueToCheck, result)

    def test_bitwise_or_FindOptions(self):
        path = self.get_contract_path('BitwiseOr.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', FindOptions.REMOVE_PREFIX, FindOptions.KEYS_ONLY, expected_result_type=FindOptions)
        self.assertEqual(FindOptions.REMOVE_PREFIX | FindOptions.KEYS_ONLY, result)

    def test_bitwise_or_int(self):
        path = self.get_contract_path('BitwiseOr.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 2, 4, expected_result_type=int)
        intValueToCheck = int(2 | 4)
        self.assertEqual(intValueToCheck, result)

    def test_bitwise_or_int_2(self):
        path = self.get_contract_path('BitwiseOr.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 0, 123456789, expected_result_type=int)
        self.assertEqual(123456789, result)

    def test_bitwise_or_int_3(self):
        path = self.get_contract_path('BitwiseOr.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 123456789, 0, expected_result_type=int)
        self.assertEqual(123456789, result)
