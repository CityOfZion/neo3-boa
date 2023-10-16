import json

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestUpdateContractTemplate(BoaTest):
    default_folder: str = 'examples'

    OWNER = neoxp.utils.get_account_by_name('owner')
    OTHER_ACCOUNT = neoxp.utils.get_account_by_name('testAccount1')
    GAS_TO_DEPLOY = 1000 * 10 ** 8

    def test_update_contract_compile(self):
        path = self.get_contract_path('update_contract.py')
        path_new = self.get_contract_path('examples/auxiliary_contracts', 'update_contract.py')
        self.compile(path)
        self.compile(path_new)

    def test_update_contract(self):
        path, _ = self.get_deploy_file_paths('update_contract.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_account = self.OTHER_ACCOUNT
        test_account_script_hash = test_account.script_hash.to_array()

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        update_contract = runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)

        tx_deploy_notifications = runner.get_transaction_result(update_contract.tx_id).executions[0].notifications
        # Transfer emitted when deploying the smart contract
        self.assertEqual(2, len(tx_deploy_notifications))
        self.assertEqual(1, len([notification
                                 for notification in tx_deploy_notifications if notification.name == 'Transfer']))
        self.assertEqual(1, len([notification
                                 for notification in tx_deploy_notifications if notification.name == 'Deploy']))

        # Saving user's balance before calling method to compare it later
        tokens_before = runner.call_contract(path, 'balanceOf', test_account_script_hash)

        # The bugged method is being called and the user is able to receive tokens for free
        invokes.append(runner.call_contract(path, 'method', test_account_script_hash))
        expected_results.append(None)

        tokens_after = runner.call_contract(path, 'balanceOf', test_account_script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # The amount of tokens will be higher after calling the method
        self.assertGreater(tokens_after.result, tokens_before.result)

        transfer_events = runner.get_events('Transfer', origin=update_contract)
        self.assertEqual(1, len(transfer_events))

        # new smart contract that has the bug fixed
        path_new = self.get_contract_path('examples/auxiliary_contracts', 'update_contract.py')
        new_nef, new_manifest = self.get_bytes_output(path_new)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        # The smart contract will be updated to fix the bug in the method
        invokes.append(runner.call_contract(path, 'update_sc', new_nef, arg_manifest, None))
        expected_results.append(None)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # An `Update` event was be emitted after the update
        event_update = runner.get_events('Update')
        self.assertEqual(1, len(event_update))

        runner.run_contract(path, 'update_sc', new_nef, arg_manifest, None, account=self.OWNER)

        # Saving user's balance before calling method to compare it later
        tokens_before = runner.call_contract(path, 'balanceOf', test_account_script_hash)

        # Now, when method is called, it won't mint new tokens to any user that called it
        invokes.append(runner.call_contract(path, 'method', test_account_script_hash))
        expected_results.append(None)

        # The amount of tokens now is the same before and after calling the method
        tokens_after = runner.call_contract(path, 'balanceOf', test_account_script_hash)

        runner.get_contract(constants.NEO_SCRIPT)

        runner.execute(account=test_account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(tokens_after.result, tokens_before.result)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
