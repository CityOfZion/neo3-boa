from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.network.payloads import verification
from neo3.wallet import account

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3_test.tests import boatestcase


class TestGasClass(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/native_test/gas'
    GAS_DECIMALS = 8

    account1: account.Account
    account2: account.Account
    balance_test: account.Account

    @classmethod
    def setupTestCase(cls):
        cls.account1 = cls.node.wallet.account_new(label='test1', password='123')
        cls.account2 = cls.node.wallet.account_new(label='test2', password='123')
        cls.balance_test = cls.node.wallet.account_new(label='balanceTestAccount', password='123')

        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 100)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.balance_test.script_hash, 10)

    async def test_get_hash(self):
        await self.set_up_contract('GetHash.py')

        expected = types.UInt160(constants.GAS_SCRIPT)
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_symbol(self):
        await self.set_up_contract('Symbol.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('GAS', result)

    def test_symbol_too_many_parameters(self):
        path = self.get_contract_path('SymbolTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    async def test_decimals(self):
        await self.set_up_contract('Decimals.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(self.GAS_DECIMALS, result)

    def test_decimals_too_many_parameters(self):
        path = self.get_contract_path('DecimalsTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    async def test_total_supply(self):
        await self.set_up_contract('TotalSupply.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertGreater(result, 0)

    def test_total_supply_too_many_parameters(self):
        path = self.get_contract_path('TotalSupplyTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    async def test_balance_of(self):
        await self.set_up_contract('BalanceOf.py')

        no_balance = types.UInt160.zero()
        result, _ = await self.call('main', [no_balance], return_type=int)
        self.assertEqual(0, result)

        expected = 10 * 10 ** self.GAS_DECIMALS
        result, _ = await self.call('main', [self.balance_test.script_hash], return_type=int)
        self.assertEqual(expected, result)

    def test_balance_of_too_many_parameters(self):
        path = self.get_contract_path('BalanceOfTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    async def test_transfer(self):
        await self.set_up_contract('Transfer.py')

        no_balance = types.UInt160.zero()
        account_1 = self.account1.script_hash
        account_2 = self.account2.script_hash
        amount = 10000
        data = ['value', 123, False]

        result, _ = await self.call('main', [no_balance, account_1, amount, data], return_type=bool)
        self.assertEqual(False, result)

        # can't transfer if there is no signature, even with enough GAS
        result, _ = await self.call('main', [account_1, account_2, amount, data], return_type=bool)
        self.assertEqual(False, result)

        # signing_accounts doesn't modify WitnessScope
        # it is not enough to pass check witness calling from test contract
        result, _ = await self.call('main',
                                    [account_1, account_2, amount, data],
                                    return_type=bool,
                                    signing_accounts=[self.account1]
                                    )
        self.assertEqual(False, result)

        signer = verification.Signer(
            account_1,
            verification.WitnessScope.GLOBAL
        )
        result, notifications = await self.call('main',
                                                [account_1, account_2, amount, data],
                                                return_type=bool,
                                                signers=[signer]
                                                )
        self.assertEqual(True, result)

        transfers = self.filter_events(notifications,
                                       origin=CONTRACT_HASHES.GAS_TOKEN,
                                       event_name='Transfer',
                                       notification_type=boatestcase.Nep17TransferEvent
                                       )
        self.assertEqual(1, len(transfers))
        self.assertEqual(account_1, transfers[0].source)
        self.assertEqual(account_2, transfers[0].destination)
        self.assertEqual(amount, transfers[0].amount)

    async def test_transfer_data_default(self):
        await self.set_up_contract('TransferDataDefault.py')

        no_balance = types.UInt160.zero()
        account_1 = self.account1.script_hash
        account_2 = self.account2.script_hash
        amount = 100

        result, _ = await self.call('main', [no_balance, account_1, amount], return_type=bool)
        self.assertEqual(False, result)

        # signing_accounts doesn't modify WitnessScope
        # it is not enough to pass check witness calling from test contract
        result, _ = await self.call('main',
                                    [account_1, account_2, amount],
                                    return_type=bool,
                                    signing_accounts=[self.account1]
                                    )
        self.assertEqual(False, result)

        signer = verification.Signer(
            account_1,
            verification.WitnessScope.GLOBAL
        )
        result, notifications = await self.call('main',
                                                [account_1, account_2, amount],
                                                return_type=bool,
                                                signers=[signer]
                                                )
        self.assertEqual(True, result)

        transfers = self.filter_events(notifications,
                                       origin=CONTRACT_HASHES.GAS_TOKEN,
                                       event_name='Transfer',
                                       notification_type=boatestcase.Nep17TransferEvent
                                       )
        self.assertEqual(1, len(transfers))
        self.assertEqual(account_1, transfers[0].source)
        self.assertEqual(account_2, transfers[0].destination)
        self.assertEqual(amount, transfers[0].amount)

    def test_transfer_too_many_parameters(self):
        path = self.get_contract_path('TransferTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_transfer_too_few__parameters(self):
        path = self.get_contract_path('TransferTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    async def test_import_with_alias(self):
        await self.set_up_contract('ImportWithAlias.py')

        no_balance = types.UInt160.zero()
        result, _ = await self.call('main', [no_balance], return_type=int)
        self.assertEqual(0, result)
