from boa3.internal.exception import CompilerError
from boa3_test.tests import boatestcase


class TestPolicyInterop(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/interop_test/policy'

    async def test_get_exec_fee_factor(self):
        await self.set_up_contract('GetExecFeeFactor.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertIsInstance(result, int)

    def test_get_exec_fee_too_many_parameters(self):
        path = self.get_contract_path('GetExecFeeFactorTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    async def test_get_fee_per_byte(self):
        await self.set_up_contract('GetFeePerByte.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertIsInstance(result, int)

    def test_get_fee_per_byte_too_many_parameters(self):
        path = self.get_contract_path('GetFeePerByteTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    async def test_get_storage_price(self):
        await self.set_up_contract('GetStoragePrice.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertIsInstance(result, int)

    def test_get_storage_price_too_many_parameters(self):
        path = self.get_contract_path('GetStoragePriceTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    async def test_is_blocked(self):
        await self.set_up_contract('IsBlocked.py')

        result, _ = await self.call('main', [bytes(20)], return_type=bool)
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

    async def test_import_policy(self):
        await self.set_up_contract('ImportPolicy.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertIsInstance(result, int)

    async def test_import_interop_policy(self):
        await self.set_up_contract('ImportInteropPolicy.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertIsInstance(result, int)
