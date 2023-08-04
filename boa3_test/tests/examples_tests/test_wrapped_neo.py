from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestWrappedTokenTemplate(BoaTest):
    default_folder: str = 'examples'

    OWNER = neoxp.utils.get_account_by_name('owner')
    OTHER_ACCOUNT_1 = neoxp.utils.get_account_by_name('testAccount1')
    OTHER_ACCOUNT_2 = neoxp.utils.get_account_by_name('testAccount2')
    OTHER_ACCOUNT_3 = neoxp.utils.get_account_by_name('testAccount3')
    GAS_TO_DEPLOY = 1000 * 10 ** 8

    def test_wrapped_neo_compile(self):
        path = self.get_contract_path('wrapped_neo.py')
        self.compile(path)

    def test_wrapped_neo_symbol(self):
        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'symbol')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual('zNEO', invoke.result)

    def test_wrapped_neo_decimals(self):
        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'decimals')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(0, invoke.result)

    def test_wrapped_neo_total_supply(self):
        total_supply = 10_000_000

        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'totalSupply')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(total_supply, invoke.result)

    def test_wrapped_neo_total_balance_of(self):
        total_supply = 10_000_000

        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        balance_of_owner = runner.call_contract(path, 'balanceOf', self.OWNER.script_hash.to_array())
        balance_of_other_account = runner.call_contract(path, 'balanceOf', self.OTHER_ACCOUNT_1.script_hash.to_array())
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # the owner of the smart contract has all tokens, other accounts should have none
        self.assertEqual(total_supply, balance_of_owner.result)
        self.assertEqual(0, balance_of_other_account.result)

        # should fail when the script length is not 20
        runner.call_contract(path, 'balanceOf', bytes(10))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'balanceOf', bytes(30))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_wrapped_neo_total_transfer(self):
        transferred_amount = 10  # 10 tokens
        owner_script_hash = self.OWNER.script_hash.to_array()
        test_account_1 = self.OTHER_ACCOUNT_1
        test_account_1_script_hash = test_account_1.script_hash.to_array()

        invokes = []
        expected_results = []

        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        wrapped_neo_contract = runner.deploy_contract(path, account=self.OWNER)
        wrapped_neo_address = wrapped_neo_contract.script_hash

        # should fail if the sender doesn't sign
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash, test_account_1_script_hash,
                                            transferred_amount, ""))
        expected_results.append(False)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # should fail if the sender doesn't have enough balance
        invokes.append(runner.call_contract(path, 'transfer', test_account_1_script_hash, owner_script_hash,
                                            transferred_amount, ""))
        expected_results.append(False)
        runner.execute(account=test_account_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # transferring to yourself
        balance_before = runner.call_contract(path, 'balanceOf', owner_script_hash)

        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash, owner_script_hash,
                                            transferred_amount, ""))
        expected_results.append(True)

        balance_after = runner.call_contract(path, 'balanceOf', owner_script_hash)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # transferring to yourself doesn't change the balance
        self.assertEqual(balance_before.result, balance_after.result)

        # fire the transfer event when transferring to yourself
        transfer_events = runner.get_events('Transfer', origin=wrapped_neo_address)
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(owner_script_hash, sender)
        self.assertEqual(owner_script_hash, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring to someone other than yourself
        balance_sender_before = runner.call_contract(path, 'balanceOf', owner_script_hash)
        balance_receiver_before = runner.call_contract(path, 'balanceOf', test_account_1_script_hash)

        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash, test_account_1_script_hash,
                                            transferred_amount, ""))
        expected_results.append(True)

        balance_sender_after = runner.call_contract(path, 'balanceOf', owner_script_hash)
        balance_receiver_after = runner.call_contract(path, 'balanceOf', test_account_1_script_hash)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # fire the transfer event when transferring to someone
        transfer_events = runner.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(owner_script_hash, sender)
        self.assertEqual(test_account_1_script_hash, receiver)
        self.assertEqual(transferred_amount, amount)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # transferring to someone other than yourself does change the balance
        self.assertEqual(balance_sender_before.result - transferred_amount, balance_sender_after.result)
        self.assertEqual(balance_receiver_before.result + transferred_amount, balance_receiver_after.result)

        # should fail when any of the scripts' length is not 20
        runner.call_contract(path, 'transfer', owner_script_hash, bytes(10), transferred_amount, "")
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'transfer', bytes(10), owner_script_hash, transferred_amount, "")
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # should fail when the amount is less than 0
        runner.call_contract(path, 'transfer', test_account_1_script_hash, owner_script_hash, -10, "")
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_wrapped_neo_burn(self):
        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        wrapped_neo_contract = runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)
        wrapped_neo_address = wrapped_neo_contract.script_hash

        total_supply = 10_000_000
        burned_amount = 100

        # adding the same amount of tokens that the wrapped neo smart contract has minted
        runner.add_neo(wrapped_neo_address, total_supply)

        owner_script_hash = self.OWNER.script_hash.to_array()

        # burning zNEO will end up giving NEO to the one who burned it
        neo_wrapped_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_owner_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', owner_script_hash)
        zneo_owner_before = runner.call_contract(path, 'balanceOf', owner_script_hash)
        # in this case, NEO will be given to the Owner
        burn_invoke = runner.call_contract(path, 'burn', owner_script_hash, burned_amount)

        # balance after burning
        neo_wrapped_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_owner_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', owner_script_hash)
        zneo_owner_after = runner.call_contract(path, 'balanceOf', owner_script_hash)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertIsNone(burn_invoke.result)

        transfer_events = runner.get_events('Transfer', origin=wrapped_neo_address)
        self.assertGreaterEqual(len(transfer_events), 1)
        wrapped_token_transfer_event = transfer_events[-1]
        self.assertEqual(3, len(wrapped_token_transfer_event.arguments))

        sender, receiver, amount = wrapped_token_transfer_event.arguments
        self.assertEqual(owner_script_hash, sender)
        self.assertEqual(None, receiver)
        self.assertEqual(burned_amount, amount)

        transfer_events = runner.get_events('Transfer', origin=constants.NEO_SCRIPT)
        self.assertGreaterEqual(len(transfer_events), 1)
        neo_transfer_event = transfer_events[-1]
        self.assertEqual(3, len(neo_transfer_event.arguments))

        sender, receiver, amount = neo_transfer_event.arguments
        self.assertEqual(wrapped_neo_address, sender)
        self.assertEqual(owner_script_hash, receiver)
        self.assertEqual(burned_amount, amount)

        self.assertEqual(neo_wrapped_before.result - burned_amount, neo_wrapped_after.result)
        self.assertEqual(neo_owner_before.result + burned_amount, neo_owner_after.result)
        self.assertEqual(zneo_owner_before.result - burned_amount, zneo_owner_after.result)

        # should fail when the script length is not 20
        runner.call_contract(path, 'burn', bytes(15), burned_amount)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # or amount is less than 0
        runner.call_contract(path, 'burn', owner_script_hash, -1)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_wrapped_neo_approve(self):
        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)

        allowed_amount = 10
        owner_script_hash = self.OWNER.script_hash.to_array()
        test_account_1 = self.OTHER_ACCOUNT_1
        test_account_1_script_hash = test_account_1.script_hash.to_array()
        test_account_2 = self.OTHER_ACCOUNT_2
        test_account_2_script_hash = test_account_2.script_hash.to_array()

        # this approve will fail, because OTHER_ACCOUNT_1 doesn't have enough zNEO
        invokes.append(runner.call_contract(path, 'approve', test_account_1_script_hash, test_account_2_script_hash,
                                            allowed_amount))
        expected_results.append(False)
        runner.execute(account=test_account_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # OWNER will give zNEO to OTHER_ACCOUNT_1 so that it can approve
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash, test_account_1_script_hash,
                                            allowed_amount, None))
        expected_results.append(True)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.run_contract(path, 'transfer', owner_script_hash, test_account_1_script_hash,
                            allowed_amount, None, account=self.OWNER)

        # this approve will succeed, because OTHER_ACCOUNT_1 have enough zNEO
        invokes.append(runner.call_contract(path, 'approve', test_account_1_script_hash, test_account_2_script_hash,
                                            allowed_amount))
        expected_results.append(True)
        runner.execute(account=test_account_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # approved fired an event
        approval_events = runner.get_events('Approval')
        self.assertEqual(1, len(approval_events))

        owner, spender, amount = approval_events[0].arguments
        self.assertEqual(test_account_1_script_hash, owner)
        self.assertEqual(test_account_2_script_hash, spender)
        self.assertEqual(allowed_amount, amount)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_wrapped_neo_allowance(self):
        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        allowed_amount = 10
        owner_script_hash = self.OWNER.script_hash.to_array()
        test_account_1 = self.OTHER_ACCOUNT_1
        test_account_1_script_hash = test_account_1.script_hash.to_array()
        test_account_2 = self.OTHER_ACCOUNT_2
        test_account_2_script_hash = test_account_2.script_hash.to_array()

        # OTHER_ACCOUNT_1 did not approve OTHER_SCRIPT_HASH
        invokes.append(runner.call_contract(path, 'allowance', test_account_1_script_hash, test_account_2_script_hash))
        expected_results.append(0)

        # OWNER will give zNEO to OTHER_ACCOUNT_1 so that it can approve
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash, test_account_1_script_hash,
                                            allowed_amount, None))
        expected_results.append(True)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.run_contract(path, 'transfer', owner_script_hash, test_account_1_script_hash, allowed_amount, None,
                            account=self.OWNER)

        # this approve will succeed, because OTHER_ACCOUNT_1 have enough zNEO
        invokes.append(runner.call_contract(path, 'approve', test_account_1_script_hash, test_account_2_script_hash,
                                            allowed_amount))
        expected_results.append(True)

        # OTHER_ACCOUNT_1 allowed OTHER_ACCOUNT_2 to spend transferred_amount of zNEO
        invokes.append(runner.call_contract(path, 'allowance', test_account_1_script_hash, test_account_2_script_hash))
        expected_results.append(allowed_amount)

        runner.execute(account=test_account_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_wrapped_neo_transfer_from(self):
        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        allowed_amount = 10
        owner_script_hash = self.OWNER.script_hash.to_array()
        test_account_1 = self.OTHER_ACCOUNT_1
        test_account_1_script_hash = test_account_1.script_hash.to_array()
        test_account_2 = self.OTHER_ACCOUNT_2
        test_account_2_script_hash = test_account_2.script_hash.to_array()
        test_account_3 = self.OTHER_ACCOUNT_3
        test_account_3_script_hash = test_account_3.script_hash.to_array()

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_gas(test_account_3.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)

        # OWNER will give zNEO to OTHER_ACCOUNT_3 so that it can approve another contracts
        invokes.append(runner.call_contract(path, 'transfer', owner_script_hash, test_account_3_script_hash,
                                            allowed_amount, None))
        expected_results.append(True)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.run_contract(path, 'transfer', owner_script_hash, test_account_3_script_hash, allowed_amount,
                            None, account=self.OWNER)

        transfer_events = runner.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(owner_script_hash, sender)
        self.assertEqual(test_account_3_script_hash, receiver)
        self.assertEqual(allowed_amount, amount)

        # this approve will succeed, because OTHER_ACCOUNT_3 have enough zNEO
        invokes.append(runner.call_contract(path, 'approve', test_account_3_script_hash, test_account_1_script_hash,
                                            allowed_amount))
        expected_results.append(True)

        runner.execute(account=test_account_3)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.run_contract(path, 'approve', test_account_3_script_hash, test_account_1_script_hash,
                            allowed_amount, account=test_account_3)

        transferred_amount = allowed_amount

        # OTHER_ACCOUNT_3 and OTHER_ACCOUNT_1 allowance is allowed_amount
        invokes.append(runner.call_contract(path, 'allowance', test_account_3_script_hash, test_account_1_script_hash))
        expected_results.append(allowed_amount)

        # this transfer will fail,
        # because OTHER_ACCOUNT_1 is not allowed to transfer more than OTHER_ACCOUNT_3 approved
        invokes.append(runner.call_contract(path, 'transferFrom', test_account_1_script_hash,
                                            test_account_3_script_hash, test_account_2_script_hash,
                                            transferred_amount + 1, None))
        expected_results.append(False)

        # this transfer will succeed and will fire the Transfer event
        balance_spender_before = runner.call_contract(path, 'balanceOf', test_account_1_script_hash)
        balance_sender_before = runner.call_contract(path, 'balanceOf', test_account_3_script_hash)
        balance_receiver_before = runner.call_contract(path, 'balanceOf', test_account_2_script_hash)

        invokes.append(runner.call_contract(path, 'transferFrom', test_account_1_script_hash,
                                            test_account_3_script_hash, test_account_2_script_hash,
                                            transferred_amount, None))
        expected_results.append(True)

        balance_spender_after = runner.call_contract(path, 'balanceOf', test_account_1_script_hash)
        balance_sender_after = runner.call_contract(path, 'balanceOf', test_account_3_script_hash)
        balance_receiver_after = runner.call_contract(path, 'balanceOf', test_account_2_script_hash)

        # OTHER_ACCOUNT_3 and OTHER_ACCOUNT_1 allowance was reduced to 0
        invokes.append(runner.call_contract(path, 'allowance', test_account_3_script_hash, test_account_1_script_hash))
        expected_results.append(0)

        runner.execute(account=test_account_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        transfer_events = runner.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(test_account_3_script_hash, sender)
        self.assertEqual(test_account_2_script_hash, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring changed the balance
        self.assertEqual(balance_spender_before.result, balance_spender_after.result)
        self.assertEqual(balance_sender_before.result - transferred_amount, balance_sender_after.result)
        self.assertEqual(balance_receiver_before.result + transferred_amount, balance_receiver_after.result)

        # this approve will succeed, because OTHER_ACCOUNT_3 have enough zNEO
        invokes.append(runner.call_contract(path, 'approve', test_account_3_script_hash, test_account_1_script_hash,
                                            allowed_amount))
        expected_results.append(True)
        runner.execute(account=test_account_3)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.run_contract(path, 'approve', test_account_3_script_hash, test_account_1_script_hash,
                            allowed_amount, account=test_account_3)

        transferred_amount = allowed_amount - 4

        invokes.append(runner.call_contract(path, 'transferFrom', test_account_1_script_hash,
                                            test_account_3_script_hash, test_account_2_script_hash,
                                            transferred_amount, None))
        expected_results.append(True)

        # OTHER_ACCOUNT_3 and OTHER_ACCOUNT_1 allowance was reduced to allowed_amount - transferred_amount
        invokes.append(runner.call_contract(path, 'allowance', test_account_3_script_hash, test_account_1_script_hash))
        expected_results.append(allowed_amount - transferred_amount)

        runner.execute(account=test_account_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # should fail when any of the scripts' length is not 20
        runner.call_contract(path, 'transferFrom', owner_script_hash, bytes(10), test_account_1_script_hash,
                             allowed_amount, None)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'transferFrom', bytes(10), test_account_1_script_hash, owner_script_hash,
                             allowed_amount, None)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'transferFrom', test_account_1_script_hash, owner_script_hash, bytes(10),
                             allowed_amount, None)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # should fail when the amount is less than 0
        runner.call_contract(path, 'transferFrom', test_account_1_script_hash, owner_script_hash,
                             test_account_2_script_hash, -10, None)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_wrapped_neo_on_nep17_payment(self):
        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        minted_amount = 10
        test_account_1 = self.OTHER_ACCOUNT_1
        test_account_1_script_hash = test_account_1.script_hash.to_array()

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        wrapped_neo_contract = runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)
        wrapped_neo_address = wrapped_neo_contract.script_hash

        runner.add_neo(test_account_1_script_hash, minted_amount)

        neo_wrapped_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_aux_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', test_account_1_script_hash)
        zneo_aux_before = runner.call_contract(path, 'balanceOf', test_account_1_script_hash)

        # transferring NEO to the wrapped_neo_address will mint them
        transfer_invoke = runner.call_contract(constants.NEO_SCRIPT, 'transfer', test_account_1_script_hash,
                                               wrapped_neo_address, minted_amount, None)

        # balance after burning
        neo_wrapped_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_aux_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', test_account_1_script_hash)
        zneo_aux_after = runner.call_contract(path, 'balanceOf', test_account_1_script_hash)

        runner.execute(account=test_account_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(True, transfer_invoke.result)

        transfer_events = runner.get_events('Transfer', origin=constants.NEO_SCRIPT)
        self.assertEqual(1, len(transfer_events))
        neo_transfer_event = transfer_events[0]
        self.assertEqual(3, len(neo_transfer_event.arguments))

        sender, receiver, amount = neo_transfer_event.arguments
        self.assertEqual(test_account_1_script_hash, sender)
        self.assertEqual(wrapped_neo_address, receiver)
        self.assertEqual(minted_amount, amount)

        transfer_events = runner.get_events('Transfer', origin=wrapped_neo_address)
        self.assertEqual(1, len(transfer_events))
        wrapped_token_transfer_event = transfer_events[0]
        self.assertEqual(3, len(wrapped_token_transfer_event.arguments))

        sender, receiver, amount = wrapped_token_transfer_event.arguments
        self.assertEqual(None, sender)
        self.assertEqual(test_account_1_script_hash, receiver)
        self.assertEqual(minted_amount, amount)

        self.assertEqual(neo_wrapped_before.result + minted_amount, neo_wrapped_after.result)
        self.assertEqual(neo_aux_before.result - minted_amount, neo_aux_after.result)
        self.assertEqual(zneo_aux_before.result + minted_amount, zneo_aux_after.result)

        # the smart contract will abort if some address other than NEO calls the onPayment method
        runner.call_contract(path, 'onNEP17Payment', test_account_1_script_hash, minted_amount, None)
        runner.execute(account=test_account_1)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ABORTED_CONTRACT_MSG)

    def test_wrapped_neo_verify(self):
        path, _ = self.get_deploy_file_paths('wrapped_neo.py')
        runner = BoaTestRunner(runner_id=self.method_name())

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
        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'verify'))
        expected_results.append(True)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
