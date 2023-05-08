from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive import neoxp
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner


class TestNEP5Template(BoaTest):
    default_folder: str = 'examples'

    OWNER = neoxp.utils.get_account_by_name('owner')
    OTHER_ACCOUNT = neoxp.utils.get_account_by_name('testAccount1')
    GAS_TO_DEPLOY = 1000 * 10 ** 8

    def test_nep5_compile(self):
        path = self.get_contract_path('nep5.py')
        self.compile(path)

    def test_nep5_symbol(self):
        path, _ = self.get_deploy_file_paths('nep5.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'symbol')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual('NEP5', invoke.result)

    def test_nep5_decimals(self):
        path, _ = self.get_deploy_file_paths('nep5.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'decimals')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(8, invoke.result)

    def test_nep5_total_supply(self):
        total_supply = 10_000_000 * 10 ** 8

        path, _ = self.get_deploy_file_paths('nep5.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'totalSupply')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(total_supply, invoke.result)

    def test_nep5_total_balance_of(self):
        total_supply = 10_000_000 * 10 ** 8

        path, _ = self.get_deploy_file_paths('nep5.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)

        invoke = runner.call_contract(path, 'balanceOf', self.OWNER.script_hash.to_array())
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(total_supply, invoke.result)

        # should fail when the script length is not 20
        runner.call_contract(path, 'balanceOf', bytes(10))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'balanceOf', bytes(30))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_nep5_total_transfer(self):
        transferred_amount = 10 * 10 ** 8  # 10 tokens
        test_account = self.OTHER_ACCOUNT
        test_account_script_hash = test_account.script_hash.to_array()
        owner_script_hash = self.OWNER.script_hash.to_array()

        path, _ = self.get_deploy_file_paths('nep5.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        nep5_contract = runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)

        nep5_address = nep5_contract.script_hash

        # should fail if the sender doesn't sign
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash,
                                            test_account_script_hash, transferred_amount))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # other account doesn't have enough balance
        invokes.append(runner.call_contract(path, 'transfer', test_account_script_hash,
                                            owner_script_hash, transferred_amount))
        expected_results.append(False)

        runner.execute(account=test_account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # doesn't fire the transfer event when transferring to yourself
        balance_before = runner.call_contract(path, 'balanceOf', owner_script_hash)
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash,
                                            owner_script_hash, transferred_amount))
        expected_results.append(True)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        transfer_events = runner.get_events('transfer', origin=nep5_address)
        self.assertEqual(0, len(transfer_events))

        balance_after = runner.call_contract(path, 'balanceOf', owner_script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # transferring to yourself doesn't change the balance
        self.assertEqual(balance_before.result, balance_after.result)

        balance_sender_before = runner.call_contract(path, 'balanceOf', owner_script_hash)
        balance_receiver_before = runner.call_contract(path, 'balanceOf', test_account_script_hash)
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash,
                                            test_account_script_hash, transferred_amount))
        expected_results.append(True)
        balance_sender_after = runner.call_contract(path, 'balanceOf', owner_script_hash)
        balance_receiver_after = runner.call_contract(path, 'balanceOf', test_account_script_hash)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(balance_sender_before.result - transferred_amount, balance_sender_after.result)
        self.assertEqual(balance_receiver_before.result + transferred_amount, balance_receiver_after.result)

        transfer_events = runner.get_events('transfer', origin=nep5_address)
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(sender).to_bytes()
        self.assertEqual(owner_script_hash, sender)
        self.assertEqual(test_account_script_hash, receiver)
        self.assertEqual(transferred_amount, amount)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # should fail when any of the scripts' length is not 20
        runner.call_contract(path, 'transfer', owner_script_hash, bytes(10), transferred_amount)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'transfer', bytes(10), owner_script_hash, transferred_amount)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # should fail when the amount is less than 0
        runner.call_contract(path, 'transfer', test_account_script_hash,
                             owner_script_hash, -10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_nep5_name(self):
        path, _ = self.get_deploy_file_paths('nep5.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'name')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual('NEP5 Standard', invoke.result)

    def test_nep5_verify(self):
        path, _ = self.get_deploy_file_paths('nep5.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invokes = []
        expected_results = []

        # should fail without signature
        invokes.append(runner.call_contract(path, 'verify'))
        expected_results.append(False)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # should fail if not signed by the owner
        invokes.append(runner.call_contract(path, 'verify'))
        expected_results.append(False)
        runner.execute(account=self.OTHER_ACCOUNT)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'verify'))
        expected_results.append(True)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
