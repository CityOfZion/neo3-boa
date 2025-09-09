from neo3.api import noderpc
from neo3.api.wrappers import PolicyContract
from neo3.core import types
from neo3.network.payloads import verification

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo3.network.payloads.transactionattributetype import TransactionAttributeType
from boa3_test.tests import boatestcase


class TestPolicyContract(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/native_test/policy'

    @classmethod
    async def get_exec_fee_factor(cls) -> int:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host):
            receipt = await cls.node.facade.test_invoke(PolicyContract().exec_fee_factor())
            return receipt.result

    @classmethod
    async def get_fee_per_byte(cls) -> int:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host):
            receipt = await cls.node.facade.test_invoke(PolicyContract().fee_per_byte())
            return receipt.result

    @classmethod
    async def get_storage_price(cls) -> int:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host):
            receipt = await cls.node.facade.test_invoke(PolicyContract().storage_price())
            return receipt.result

    async def test_get_hash(self):
        await self.set_up_contract('GetHash.py')

        expected = types.UInt160(constants.POLICY_SCRIPT)
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_get_attribute_fee(self):
        await self.set_up_contract('GetAttributeFee.py')

        result, _ = await self.call('main', [TransactionAttributeType.HIGH_PRIORITY], return_type=int)
        self.assertIsInstance(result, int)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [19999999], return_type=int)
        self.assertRegex(str(context.exception), 'bigint does not fit into uint8')

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [20], return_type=int)
        self.assertRegex(str(context.exception), 'invalid attribute type: 20')

    async def test_set_attribute_fee(self):
        await self.set_up_contract('SetAttributeFee.py')

        signer = verification.Signer(
            self.genesis.script_hash,
            verification.WitnessScope.GLOBAL
        )
        result, _ = await self.call('main', [TransactionAttributeType.HIGH_PRIORITY, 100],
                                    return_type=None, signers=[signer], signing_accounts=[self.genesis])

        result, _ = await self.call('get_tx_attr', [TransactionAttributeType.HIGH_PRIORITY], return_type=int)
        self.assertEqual(result, 100)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [TransactionAttributeType.HIGH_PRIORITY, 100], return_type=int)
        self.assertRegex(str(context.exception), 'invalid committee signature')

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

    async def test_transaction_attribute_instantiate(self):
        await self.set_up_contract('TransactionAttributeTypeInstantiate.py')

        result, _ = await self.call('main', [TransactionAttributeType.HIGH_PRIORITY], return_type=int)
        self.assertEqual(TransactionAttributeType.HIGH_PRIORITY, result)

        result, _ = await self.call('main', [TransactionAttributeType.ORACLE_RESPONSE], return_type=int)
        self.assertEqual(TransactionAttributeType.ORACLE_RESPONSE, result)

        result, _ = await self.call('main', [TransactionAttributeType.NOT_VALID_BEFORE], return_type=int)
        self.assertEqual(TransactionAttributeType.NOT_VALID_BEFORE, result)

        result, _ = await self.call('main', [TransactionAttributeType.CONFLICTS], return_type=int)
        self.assertEqual(TransactionAttributeType.CONFLICTS, result)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [0x00], return_type=int)

        self.assertRegex(str(context.exception), "Invalid TransactionAttributeType parameter value")

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('main', [0xFF], return_type=int)

        self.assertRegex(str(context.exception), "Invalid TransactionAttributeType parameter value")

    async def test_transaction_attribute_not(self):
        await self.set_up_contract('TransactionAttributeTypeNot.py')

        for transaction_attribute_type in TransactionAttributeType:
            result, _ = await self.call('main', [transaction_attribute_type], return_type=int)
            self.assertEqual(~transaction_attribute_type, result)

    async def test_import_contracts_policy_contract(self):
        await self.set_up_contract('ImportContractsPolicyContract.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertIsInstance(result, int)

    async def test_import_interop_policy(self):
        await self.set_up_contract('ImportScContractsPolicyContract.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertIsInstance(result, int)
