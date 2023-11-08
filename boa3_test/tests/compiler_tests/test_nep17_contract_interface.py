from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestContractInterface(BoaTest):
    default_folder: str = 'test_sc/nep17_contract_interface_test'

    def test_balance_of(self):
        path, _ = self.get_deploy_file_paths('Nep17BalanceOf.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        from boa3_test.tests.test_drive import neoxp
        genesis = neoxp.utils.get_account_by_name('genesis')

        invoke_balance_of = runner.call_contract(path, 'main', genesis.script_hash.to_array())
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(10 ** 8, invoke_balance_of.result)

    def test_decimals(self):
        path, _ = self.get_deploy_file_paths('Nep17Decimals.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke_decimals = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(0, invoke_decimals.result)

    def test_symbol(self):
        path, _ = self.get_deploy_file_paths('Nep17Symbol.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke_symbol = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual('NEO', invoke_symbol.result)

    def test_total_supply(self):
        path, _ = self.get_deploy_file_paths('Nep17TotalSupply.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke_total_supply = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(10 ** 8, invoke_total_supply.result)

    def test_transfer(self):
        path, _ = self.get_deploy_file_paths('Nep17Transfer.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        from boa3_test.tests.test_drive import neoxp
        genesis = neoxp.utils.get_account_by_name('genesis')

        # TODO: Methods and contract hash are not being added to the contract permissions yet #86a1678cf
        with self.assertRaises(AssertionError):
            invoke_test_transfer = runner.call_contract(path, 'main',
                                                        genesis.script_hash.to_array(), genesis.script_hash.to_array(), -1)
            runner.execute()
            self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
            self.assertEqual(False, invoke_test_transfer.result)
