from boa3.exception import CompilerError
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestPolicyContract(BoaTest):

    default_folder: str = 'test_sc/native_test/policy'

    def test_get_exec_fee_factor(self):
        path = self.get_contract_path('GetExecFeeFactor.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)

    def test_get_exec_fee_too_many_parameters(self):
        path = self.get_contract_path('GetExecFeeFactorTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_get_fee_per_byte(self):
        path = self.get_contract_path('GetFeePerByte.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)

    def test_get_fee_per_byte_too_many_parameters(self):
        path = self.get_contract_path('GetFeePerByteTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_get_storage_price(self):
        path = self.get_contract_path('GetStoragePrice.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)

    def test_get_storage_price_too_many_parameters(self):
        path = self.get_contract_path('GetStoragePriceTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_is_blocked(self):
        path = self.get_contract_path('IsBlocked.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', bytes(20))
        self.assertEqual(False, result)

    def test_is_blocked_mismatched_type(self):
        path = self.get_contract_path('IsBlockedMismatchedTypeInt.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

        path = self.get_contract_path('IsBlockedMismatchedTypeStr.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

        path = self.get_contract_path('IsBlockedMismatchedTypeBool.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_is_blocked_too_many_parameters(self):
        path = self.get_contract_path('IsBlockedTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_is_blocked_too_few_parameters(self):
        path = self.get_contract_path('IsBlockedTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)
