from neo3.api import noderpc
from neo3.api.wrappers import PolicyContract
from neo3.core import types

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3_test.tests import boatestcase


class TestPolicyContract(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/native_test/policy'

    @classmethod
    async def get_exec_fee_factor(cls) -> int:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host):
            return await cls.node.facade.test_invoke(PolicyContract().exec_fee_factor())

    @classmethod
    async def get_fee_per_byte(cls) -> int:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host):
            return await cls.node.facade.test_invoke(PolicyContract().fee_per_byte())

    @classmethod
    async def get_storage_price(cls) -> int:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host):
            return await cls.node.facade.test_invoke(PolicyContract().storage_price())

    async def test_get_hash(self):
        await self.set_up_contract('GetHash.py')

        expected = types.UInt160(constants.POLICY_SCRIPT)
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_get_exec_fee_factor(self):
        await self.set_up_contract('GetExecFeeFactor.py')

        expected = await self.get_exec_fee_factor()
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(expected, result)

    def test_get_exec_fee_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'GetExecFeeFactorTooManyArguments.py')

    async def test_get_fee_per_byte(self):
        await self.set_up_contract('GetFeePerByte.py')

        expected = await self.get_fee_per_byte()
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(expected, result)

    def test_get_fee_per_byte_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'GetFeePerByteTooManyArguments.py')

    async def test_get_storage_price(self):
        await self.set_up_contract('GetStoragePrice.py')

        expected = await self.get_storage_price()
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(expected, result)

    def test_get_storage_price_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'GetStoragePriceTooManyArguments.py')

    async def test_is_blocked(self):
        await self.set_up_contract('IsBlocked.py')

        result, _ = await self.call('main', [types.UInt160.zero()], return_type=bool)
        self.assertEqual(False, result)

    def test_is_blocked_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'IsBlockedMismatchedTypeInt.py')

        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'IsBlockedMismatchedTypeStr.py')

        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'IsBlockedMismatchedTypeBool.py')

    def test_is_blocked_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'IsBlockedTooManyArguments.py')

    def test_is_blocked_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'IsBlockedTooFewArguments.py')
