from boa3.exception import CompilerError
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestGasClass(BoaTest):

    default_folder: str = 'test_sc/native_test/gas'

    def test_symbol(self):
        path = self.get_contract_path('Symbol.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual('GAS', result)

    def test_symbol_too_many_parameters(self):
        path = self.get_contract_path('SymbolTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_decimals(self):
        path = self.get_contract_path('Decimals.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(8, result)

    def test_decimals_too_many_parameters(self):
        path = self.get_contract_path('DecimalsTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_total_supply(self):
        path = self.get_contract_path('TotalSupply.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)

    def test_total_supply_too_many_parameters(self):
        path = self.get_contract_path('TotalSupplyTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_balance_of(self):
        path = self.get_contract_path('BalanceOf.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', bytes(range(20)))
        self.assertEqual(0, result)

        engine.add_gas(bytes(range(20)), 10)
        result = self.run_smart_contract(engine, path, 'main', bytes(range(20)))
        self.assertEqual(10, result)

    def test_balance_of_too_many_parameters(self):
        path = self.get_contract_path('BalanceOfTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_transfer(self):
        path = self.get_contract_path('Transfer.py')
        engine = TestEngine()

        account_1 = bytes(range(20))
        account_2 = bytes(range(20)[::-1])
        amount = 10000

        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount, ['value', 123, False])
        self.assertEqual(False, result)

        engine.add_gas(account_1, amount)
        # can't transfer if there is no signature, even with enough GAS
        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount, ['value', 123, False])
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount, ['value', 123, False],
                                         signer_accounts=[account_1])
        self.assertEqual(True, result)

    def test_transfer_data_default(self):
        path = self.get_contract_path('TransferDataDefault.py')
        engine = TestEngine()

        account_1 = bytes(range(20))
        account_2 = bytes(range(20)[::-1])
        amount = 100

        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount)
        self.assertEqual(False, result)

        engine.add_gas(account_1, amount)
        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount,
                                         signer_accounts=[account_1])
        self.assertEqual(True, result)

    def test_transfer_too_many_parameters(self):
        path = self.get_contract_path('TransferTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_transfer_too_few__parameters(self):
        path = self.get_contract_path('TransferTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)
