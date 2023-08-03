from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestGasClass(BoaTest):
    default_folder: str = 'test_sc/native_test/gas'
    GAS_CONTRACT_NAME = 'GasToken'

    def test_get_hash(self):
        path, _ = self.get_deploy_file_paths('GetHash.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(constants.GAS_SCRIPT)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_symbol(self):
        path, _ = self.get_deploy_file_paths('Symbol.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append('GAS')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_symbol_too_many_parameters(self):
        path = self.get_contract_path('SymbolTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_decimals(self):
        path, _ = self.get_deploy_file_paths('Decimals.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(8)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_decimals_too_many_parameters(self):
        path = self.get_contract_path('DecimalsTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_total_supply(self):
        path, _ = self.get_deploy_file_paths('TotalSupply.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        contract_call = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertIsInstance(contract_call.result, int)

    def test_total_supply_too_many_parameters(self):
        path = self.get_contract_path('TotalSupplyTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_balance_of(self):
        path, _ = self.get_deploy_file_paths('BalanceOf.py')
        test_account_1 = neoxp.utils.get_account_by_name('testAccount1').script_hash.to_array()
        test_account_2 = neoxp.utils.get_account_by_name('testAccount2').script_hash.to_array()
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', test_account_2))
        expected_results.append(0)

        runner.add_gas(test_account_1, 10)
        invokes.append(runner.call_contract(path, 'main', test_account_1))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_balance_of_too_many_parameters(self):
        path = self.get_contract_path('BalanceOfTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_transfer(self):
        path, _ = self.get_deploy_file_paths('Transfer.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        account = neoxp.utils.get_account_by_name('testAccount1')
        account_1 = account.script_hash.to_array()
        account_2 = neoxp.utils.get_account_by_name('testAccount2').script_hash.to_array()
        amount = 10000

        runner.add_gas(account_1, amount)
        invokes.append(runner.call_contract(path, 'main', account_2, account_1, amount, ['value', 123, False]))
        expected_results.append(False)

        # can't transfer if there is no signature, even with enough GAS
        invokes.append(runner.call_contract(path, 'main', account_1, account_2, amount, ['value', 123, False]))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # TestRunner doesn't have WitnessScope modifier
        # signing is not enough to pass check witness calling from test contract
        invokes.append(runner.call_contract(path, 'main', account_1, account_2, amount, ['value', 123, False]))
        expected_results.append(False)

        invokes.append(runner.call_contract(self.GAS_CONTRACT_NAME, 'transfer',
                                            account_1, account_2, amount, ['value', 123, False]))
        expected_results.append(True)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_transfer_data_default(self):
        path, _ = self.get_deploy_file_paths('TransferDataDefault.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        account = neoxp.utils.get_account_by_name('testAccount1')
        account_1 = account.script_hash.to_array()
        account_2 = neoxp.utils.get_account_by_name('testAccount2').script_hash.to_array()
        amount = 100

        runner.add_gas(account_1, amount)
        invokes.append(runner.call_contract(path, 'main', account_2, account_1, amount))
        expected_results.append(False)
        runner.update_contracts(export_checkpoint=True)

        # TestRunner doesn't have WitnessScope modifier
        # signing is not enough to pass check witness calling from test contract
        invokes.append(runner.call_contract(path, 'main', account_1, account_2, amount))
        expected_results.append(False)

        invokes.append(runner.call_contract(self.GAS_CONTRACT_NAME, 'transfer', account_1, account_2, amount, None))
        expected_results.append(True)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_transfer_too_many_parameters(self):
        path = self.get_contract_path('TransferTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_transfer_too_few__parameters(self):
        path = self.get_contract_path('TransferTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_import_with_alias(self):
        path, _ = self.get_deploy_file_paths('ImportWithAlias.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', bytes(20)))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
