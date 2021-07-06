from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestPolicyInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/policy'

    def test_get_exec_fee_factor(self):
        path = self.get_contract_path('GetExecFeeFactor.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)

    def test_get_fee_per_byte(self):
        path = self.get_contract_path('GetFeePerByte.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)

    def test_get_storage_price(self):
        path = self.get_contract_path('GetStoragePrice.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)

    def test_is_blocked(self):
        path = self.get_contract_path('IsBlocked.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', bytes(20))
        self.assertEqual(False, result)
