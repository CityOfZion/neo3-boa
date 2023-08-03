from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestSimpleNEP17Template(BoaTest):
    default_folder: str = 'examples'

    DECIMALS = 2
    TOTAL_SUPPLY = 100_000_000 * 10 ** DECIMALS

    OWNER = neoxp.utils.get_account_by_name('owner')
    OTHER_ACCOUNT = neoxp.utils.get_account_by_name('testAccount1')
    GAS_TO_DEPLOY = 1000 * 10 ** 8

    def test_simple_nep17_compile(self):
        path = self.get_contract_path('simple_nep17.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-17', manifest['supportedstandards'])

    def test_simple_nep17_symbol(self):
        path, _ = self.get_deploy_file_paths('simple_nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'symbol')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual('COIN', invoke.result)

    def test_simple_nep17_decimals(self):
        path, _ = self.get_deploy_file_paths('simple_nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'decimals')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(self.DECIMALS, invoke.result)

    def test_simple_nep17_total_supply(self):
        path, _ = self.get_deploy_file_paths('simple_nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'totalSupply')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(self.TOTAL_SUPPLY, invoke.result)

    def test_simple_nep17_total_balance_of(self):
        path, _ = self.get_deploy_file_paths('simple_nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invoke = runner.call_contract(path, 'balanceOf', self.OWNER.script_hash.to_array())
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(self.TOTAL_SUPPLY, invoke.result)

        # should fail when the script length is not 20
        runner.call_contract(path, 'balanceOf', bytes(10))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'balanceOf', bytes(30))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_simple_nep17_total_transfer(self):
        transferred_amount = 10 * 10 ** self.DECIMALS  # 10 tokens
        invokes = []
        expected_results = []
        owner_script_hash = self.OWNER.script_hash.to_array()
        test_account = self.OTHER_ACCOUNT
        test_account_script_hash = self.OTHER_ACCOUNT.script_hash.to_array()

        path, _ = self.get_deploy_file_paths('simple_nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # should fail if the sender doesn't sign
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash, test_account_script_hash,
                                            transferred_amount, None))
        expected_results.append(False)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # should fail if the sender doesn't have enough balance
        invokes.append(runner.call_contract(path, 'transfer', test_account_script_hash, owner_script_hash,
                                            transferred_amount, None))
        expected_results.append(False)
        runner.execute(account=test_account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # transferring tokens to yourself
        balance_before = runner.call_contract(path, 'balanceOf', owner_script_hash)
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash, owner_script_hash,
                                            transferred_amount, None))
        expected_results.append(True)
        balance_after = runner.call_contract(path, 'balanceOf', owner_script_hash)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # fire the transfer event when transferring to yourself
        transfer_events = runner.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(owner_script_hash, sender)
        self.assertEqual(owner_script_hash, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring to yourself doesn't change the balance
        self.assertEqual(balance_before.result, balance_after.result)

        # transferring tokens to another account
        balance_sender_before = runner.call_contract(path, 'balanceOf', owner_script_hash)
        balance_receiver_before = runner.call_contract(path, 'balanceOf', test_account_script_hash)
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash, test_account_script_hash,
                                            transferred_amount, None))
        expected_results.append(True)
        balance_sender_after = runner.call_contract(path, 'balanceOf', owner_script_hash)
        balance_receiver_after = runner.call_contract(path, 'balanceOf', test_account_script_hash)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        transfer_events = runner.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(owner_script_hash, sender)
        self.assertEqual(test_account_script_hash, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring to someone other than yourself does change the balance
        self.assertEqual(balance_sender_before.result - transferred_amount, balance_sender_after.result)
        self.assertEqual(balance_receiver_before.result + transferred_amount, balance_receiver_after.result)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # should fail when any of the scripts' length is not 20
        runner.call_contract(path, 'transfer', owner_script_hash, bytes(10), transferred_amount, "")
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'transfer', bytes(10), test_account_script_hash, transferred_amount, "")
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # should fail when the amount is less than 0
        runner.call_contract(path, 'transfer', owner_script_hash, test_account_script_hash, -10, None)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_simple_nep17_on_nep17_payment(self):
        path, _ = self.get_deploy_file_paths('simple_nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.update_contracts(export_checkpoint=True)

        # trying to call onNEP17Payment() will result all result in an abort
        runner.call_contract(path, 'onNEP17Payment', self.OWNER.script_hash.to_array(), 0, None)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ABORTED_CONTRACT_MSG)
