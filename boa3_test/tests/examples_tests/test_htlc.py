from typing import List, Any

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.neo.cryptography import hash160
from boa3.internal.neo.smart_contract.notification import Notification
from boa3.internal.neo3.core.types import UInt256
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.model.network.payloads.testtransaction import TransactionExecution
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestHTLCTemplate(BoaTest):
    default_folder: str = 'examples'

    OWNER = neoxp.utils.get_account_by_name('owner')
    OTHER_ACCOUNT_1 = neoxp.utils.get_account_by_name('testAccount1')
    OTHER_ACCOUNT_2 = neoxp.utils.get_account_by_name('testAccount2')
    GAS_TO_DEPLOY = 1000 * 10 ** 8
    REFUND_WAIT_TIME = 24 * 60 * 60     # smart contract constant in seconds

    def _validate_execution_result(self, runner: BoaTestRunner, tx_id: UInt256, expected_result: Any) -> TransactionExecution:
        # Test Runner isn't returning the runtime.time value correctly when using `call_contract`, so we have to get the
        # data from the transaction directly
        transactions_log = runner.get_transaction_result(tx_id)
        self.assertEqual(1, len(transactions_log.executions))
        transaction_execution = transactions_log.executions[0]
        self.assertEqual(VMState.HALT, transaction_execution.vm_state, msg=transaction_execution.exception)
        self.assertEqual(1, len(transaction_execution.result_stack))
        self.assertEqual(expected_result, transaction_execution.result_stack[0])

        return transaction_execution

    def test_htlc_compile(self):
        path = self.get_contract_path('htlc.py')
        self.compile(path)

    def test_htlc_atomic_swap(self):
        path, _ = self.get_deploy_file_paths('htlc.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        tokens_neo = 10 * 10 ** 0
        tokens_gas = 10000 * 10 ** 8
        secret_hash = hash160(b'unit test')

        # starting atomic swap by using the atomic_swap method
        invoke = runner.run_contract(path, 'atomic_swap',
                                     self.OWNER.script_hash.to_array(), constants.NEO_SCRIPT, tokens_neo,
                                     self.OTHER_ACCOUNT_1.script_hash.to_array(), constants.GAS_SCRIPT, tokens_gas,
                                     secret_hash, account=self.OWNER)

        runner.update_contracts(export_checkpoint=True)

        # The `atomic_swap` method uses runtime.time, but BoaTestRunner fails to get it
        self._validate_execution_result(runner, invoke.tx_id, expected_result=True)

    def test_htlc_on_nep17_payment(self):
        path, _ = self.get_deploy_file_paths('htlc.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 10000 * 10 ** 8
        test_account1 = self.OTHER_ACCOUNT_1
        test_account1_script_hash = test_account1.script_hash.to_array()
        test_account2 = self.OTHER_ACCOUNT_2
        test_account2_script_hash = test_account2.script_hash.to_array()
        secret_hash = hash160(b'unit test')

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        htlc_contract = runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)
        htlc_script_hash = htlc_contract.script_hash

        runner.add_neo(test_account1.address, transferred_amount_neo)
        runner.add_gas(test_account2.address, transferred_amount_gas)

        # starting atomic swap
        runner.run_contract(path, 'atomic_swap',
                            test_account1_script_hash, constants.NEO_SCRIPT, transferred_amount_neo,
                            test_account2_script_hash, constants.GAS_SCRIPT, transferred_amount_gas,
                            secret_hash, account=self.OWNER)

        # saving the balance to compare after the transfer
        balance_neo_sender_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', test_account1_script_hash)
        balance_neo_receiver_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', htlc_script_hash)

        # this transfer will be accepted
        invoke = runner.call_contract(constants.NEO_SCRIPT, 'transfer', test_account1_script_hash,
                                      htlc_script_hash, transferred_amount_neo, None)

        # saving the balance after to compare with the balance before the transfer
        balance_neo_sender_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', test_account1_script_hash)
        balance_neo_receiver_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', htlc_script_hash)

        runner.execute(account=test_account1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(True, invoke.result)

        # transfer was accepted so it was registered
        transfer_events = runner.get_events('Transfer', constants.NEO_SCRIPT)
        self.assertEqual(1, len(transfer_events))
        neo_transfer_event = transfer_events[0]
        self.assertEqual(3, len(neo_transfer_event.arguments))

        sender, receiver, amount = neo_transfer_event.arguments
        self.assertEqual(test_account1_script_hash, sender)
        self.assertEqual(htlc_script_hash, receiver)
        self.assertEqual(transferred_amount_neo, amount)

        self.assertEqual(balance_neo_sender_before.result - transferred_amount_neo, balance_neo_sender_after.result)
        self.assertEqual(balance_neo_receiver_before.result + transferred_amount_neo, balance_neo_receiver_after.result)

        # transfer won't be accepted, because amount is wrong
        runner.call_contract(constants.GAS_SCRIPT, 'transfer', test_account2_script_hash, htlc_script_hash,
                             transferred_amount_gas - 1, None)
        runner.execute(account=test_account2)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ABORTED_CONTRACT_MSG)

        # saving the balance to compare after the transfer
        balance_gas_sender_before = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', test_account2_script_hash)
        balance_gas_receiver_before = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', htlc_script_hash)

        # this transfer will be accepted
        invoke = runner.call_contract(constants.GAS_SCRIPT, 'transfer', test_account2_script_hash,
                                      htlc_script_hash, transferred_amount_gas, None)

        # saving the balance after to compare with the balance before the transfer
        balance_gas_sender_after = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', test_account2_script_hash)
        balance_gas_receiver_after = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', htlc_script_hash)

        runner.execute(account=test_account2)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(True, invoke.result)

        # the transfer was accepted so it was registered
        transfer_events = runner.get_events('Transfer', origin=constants.GAS_SCRIPT)
        self.assertGreaterEqual(len(transfer_events), 1)
        gas_transfer_event = transfer_events[-1]
        self.assertEqual(3, len(gas_transfer_event.arguments))

        sender, receiver, amount = gas_transfer_event.arguments
        self.assertEqual(test_account2_script_hash, sender)
        self.assertEqual(htlc_script_hash, receiver)
        self.assertEqual(transferred_amount_gas, amount)

        self.assertEqual(balance_gas_sender_before.result - transferred_amount_gas, balance_gas_sender_after.result)
        self.assertEqual(balance_gas_receiver_before.result + transferred_amount_gas, balance_gas_receiver_after.result)

        # transfer wil be aborted at onPayment if the transfer is not valid
        runner.call_contract(constants.NEO_SCRIPT, 'transfer', test_account1_script_hash,
                             htlc_script_hash, transferred_amount_neo - 1, None)
        runner.execute(account=test_account1)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ABORTED_CONTRACT_MSG)

    def test_htlc_withdraw(self):
        path, _ = self.get_deploy_file_paths('htlc.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 10000 * 10 ** 8
        person_a = self.OTHER_ACCOUNT_1
        person_a_script_hash = person_a.script_hash.to_array()
        person_b = self.OTHER_ACCOUNT_2
        person_b_script_hash = person_b.script_hash.to_array()
        secret_hash = hash160(b'unit test')

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_gas(person_a.address, self.GAS_TO_DEPLOY)    # adding GAS to let them be able to invoke contracts
        runner.add_gas(person_b.address, self.GAS_TO_DEPLOY)    # adding GAS to let them be able to invoke contracts
        runner.add_neo(person_a.address, transferred_amount_neo)    # adding NEO that will be swapped
        runner.add_gas(person_b.address, transferred_amount_gas)    # adding GAS that will be swapped

        htlc_contract = runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)
        htlc_script_hash = htlc_contract.script_hash

        # starting atomic swap by using the atomic_swap method
        runner.run_contract(path, 'atomic_swap',
                            person_a_script_hash, constants.NEO_SCRIPT, transferred_amount_neo,
                            person_b_script_hash, constants.GAS_SCRIPT, transferred_amount_gas,
                            secret_hash, account=self.OWNER)

        # saving the balance to compare after the withdraw
        balance_neo_person_a_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', person_a_script_hash)
        balance_neo_person_b_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', person_b_script_hash)
        balance_neo_htlc_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', htlc_script_hash)
        balance_gas_person_a_before = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', person_a_script_hash)
        balance_gas_person_b_before = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', person_b_script_hash)
        balance_gas_htlc_before = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', htlc_script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # won't be able to withdraw, because no one transferred cryptocurrency to the smart contract
        invoke_withdraw_wrong1 = runner.run_contract(path, 'withdraw', b'unit test', account=self.OWNER)

        invoke_transfer_person_a = runner.run_contract(constants.NEO_SCRIPT, 'transfer',
                                                       person_a_script_hash, htlc_script_hash, transferred_amount_neo,
                                                       None, account=person_a)
        invoke_transfer_person_b = runner.run_contract(constants.GAS_SCRIPT, 'transfer',
                                                       person_b_script_hash, htlc_script_hash, transferred_amount_gas,
                                                       None, account=person_b)

        # the withdraw will fail, because the secret is wrong
        invoke_withdraw_wrong2 = runner.run_contract(path, 'withdraw', b'wrong one', account=self.OWNER)

        # the withdraw will occur
        invoke_withdraw_right = runner.run_contract(path, 'withdraw', b'unit test', account=self.OWNER)

        # saving the balance after to compare with the balance before the transfer
        balance_neo_person_a_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', person_a_script_hash)
        balance_neo_person_b_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', person_b_script_hash)
        balance_neo_htlc_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', htlc_script_hash)

        balance_gas_person_a_after = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', person_a_script_hash)
        balance_gas_person_b_after = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', person_b_script_hash)
        balance_gas_htlc_after = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', htlc_script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # The `withdraw` method uses runtime.time, but BoaTestRunner fails to get it
        self._validate_execution_result(runner, invoke_withdraw_wrong1.tx_id, expected_result=False)
        self._validate_execution_result(runner, invoke_withdraw_wrong2.tx_id, expected_result=False)
        transaction_withdraw = self._validate_execution_result(runner, invoke_withdraw_right.tx_id, expected_result=True)

        # the transfer were accepted so they were registered
        transfer_events = transaction_withdraw.notifications
        self.assertEqual(3, len(transfer_events))
        self.assertEqual(True, all(event.name == 'Transfer' for event in transfer_events))
        gas_transfer_event = transfer_events[0]
        self.assertEqual(3, len(gas_transfer_event.arguments))
        self.assertEqual(constants.GAS_SCRIPT, gas_transfer_event.contract.script_hash)

        neo_transfer_event = transfer_events[1]
        self.assertEqual(3, len(neo_transfer_event.arguments))
        self.assertEqual(constants.NEO_SCRIPT, neo_transfer_event.contract.script_hash)

        gas_mint_event = transfer_events[2]
        self.assertEqual(3, len(gas_mint_event.arguments))
        self.assertEqual(constants.GAS_SCRIPT, gas_transfer_event.contract.script_hash)

        sender, receiver, amount = gas_transfer_event.arguments
        self.assertEqual(htlc_script_hash, sender)
        self.assertEqual(person_a_script_hash, receiver)
        self.assertEqual(transferred_amount_gas, amount)

        sender, receiver, amount = neo_transfer_event.arguments
        self.assertEqual(htlc_script_hash, sender)
        self.assertEqual(person_b_script_hash, receiver)
        self.assertEqual(transferred_amount_neo, amount)

        sender, receiver, gas_minted_htlc = gas_mint_event.arguments
        self.assertEqual(None, sender)
        self.assertEqual(htlc_script_hash, receiver)

        transaction_transfer_person_a = runner.get_transaction(invoke_transfer_person_a.tx_id)
        transaction_result_transfer_person_a = runner.get_transaction_result(invoke_transfer_person_a.tx_id)
        gas_consumed_person_a = (transaction_result_transfer_person_a.executions[0].gas_consumed +
                                 transaction_transfer_person_a.network_fee)
        # since person_a already has NEO, the system will mint some GAS to them
        gas_minted_person_a = transaction_result_transfer_person_a.executions[0].notifications[1].arguments[2]

        transaction_transfer_person_b = runner.get_transaction(invoke_transfer_person_b.tx_id)
        transaction_result_transfer_person_b = runner.get_transaction_result(invoke_transfer_person_b.tx_id)
        gas_consumed_person_b = (transaction_result_transfer_person_b.executions[0].gas_consumed +
                                 transaction_transfer_person_b.network_fee)

        self.assertEqual(balance_neo_person_a_before.result - transferred_amount_neo, balance_neo_person_a_after.result)
        self.assertEqual(balance_neo_person_b_before.result + transferred_amount_neo, balance_neo_person_b_after.result)
        self.assertEqual(balance_neo_htlc_before.result, balance_neo_htlc_after.result)
        self.assertEqual(balance_gas_person_a_before.result + transferred_amount_gas - gas_consumed_person_a + gas_minted_person_a,
                         balance_gas_person_a_after.result)
        self.assertEqual(balance_gas_person_b_before.result - transferred_amount_gas - gas_consumed_person_b, balance_gas_person_b_after.result)
        self.assertEqual(balance_gas_htlc_before.result + gas_minted_htlc, balance_gas_htlc_after.result)

    def test_htlc_refund_zero_transfers(self):
        path, _ = self.get_deploy_file_paths('htlc.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 10000 * 10 ** 8
        person_a = self.OTHER_ACCOUNT_1
        person_a_script_hash = person_a.script_hash.to_array()
        person_b = self.OTHER_ACCOUNT_2
        person_b_script_hash = person_b.script_hash.to_array()
        secret_hash = hash160(b'unit test')

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_gas(person_a.address, self.GAS_TO_DEPLOY)    # adding GAS to let them be able to invoke contracts
        runner.add_gas(person_b.address, self.GAS_TO_DEPLOY)    # adding GAS to let them be able to invoke contracts
        runner.deploy_contract(path, account=self.OWNER)

        runner.add_neo(person_a.address, transferred_amount_neo)    # adding NEO that will be swapped
        runner.add_gas(person_b.address, transferred_amount_gas)    # adding GAS that will be swapped

        runner.call_contract(path, 'atomic_swap',
                             person_a_script_hash, constants.NEO_SCRIPT, transferred_amount_neo,
                             person_b_script_hash, constants.GAS_SCRIPT, transferred_amount_gas,
                             secret_hash)

        runner.execute(add_invokes_to_batch=True, account=self.OWNER)
        # Test Runner isn't returning runtime.time value correctly and is returning VMState.FAULT, but the method
        # should work, that's why the invoke is being added to the batch
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)

        # won't be able to refund, because not enough time has passed
        invoke_refund_fail = runner.run_contract(path, 'refund')

        # this simulates a new block in the blockchain
        # time only changes value when a new block enters the blockchain
        runner.increase_block(time_interval_in_secs=self.REFUND_WAIT_TIME)
        # will be able to refund, because enough time has passed
        invoke_refund_success = runner.run_contract(path, 'refund', account=self.OWNER)

        runner.update_contracts(export_checkpoint=True)

        # The `refund` method uses runtime.time, but BoaTestRunner fails to get it
        self._validate_execution_result(runner, invoke_refund_fail.tx_id, expected_result=False)

        # The `refund` method uses runtime.time, but BoaTestRunner fails to get it
        self._validate_execution_result(runner, invoke_refund_success.tx_id, expected_result=True)

        transfer_events: List[Notification] = []
        # no one transferred cryptocurrency to the contract, so no one was refunded and no Transfer occurred
        # removing possible GAS minting from the List
        for k in runner.get_events('Transfer'):
            if k.arguments[0] is not None and k.name == 'Transfer':
                transfer_events.append(k)
        self.assertEqual(0, len(transfer_events))

    def test_htlc_refund_one_transfer(self):
        path, _ = self.get_deploy_file_paths('htlc.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 10000 * 10 ** 8
        person_a = self.OTHER_ACCOUNT_1
        person_a_script_hash = person_a.script_hash.to_array()
        person_b = self.OTHER_ACCOUNT_2
        person_b_script_hash = person_b.script_hash.to_array()
        secret_hash = hash160(b'unit test')

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_gas(person_a.address, self.GAS_TO_DEPLOY)  # adding GAS to let them be able to invoke contracts
        runner.add_gas(person_b.address, self.GAS_TO_DEPLOY)  # adding GAS to let them be able to invoke contracts
        htlc_contract = runner.deploy_contract(path, account=self.OWNER)

        runner.add_neo(person_a.address, transferred_amount_neo)  # adding NEO that will be swapped
        runner.add_gas(person_b.address, transferred_amount_gas)  # adding GAS that will be swapped

        runner.call_contract(path, 'atomic_swap',
                             person_a_script_hash, constants.NEO_SCRIPT, transferred_amount_neo,
                             person_b_script_hash, constants.GAS_SCRIPT, transferred_amount_gas,
                             secret_hash)

        runner.execute(add_invokes_to_batch=True, account=self.OWNER)
        # Test Runner isn't returning runtime.time value correctly and is returning VMState.FAULT, but the method
        # should work, that's why the invoke is being added to the batch
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)

        htlc_script_hash = htlc_contract.script_hash

        runner.call_contract(constants.NEO_SCRIPT, 'transfer', person_a_script_hash, htlc_script_hash,
                             transferred_amount_neo, None)

        runner.execute(add_invokes_to_batch=True, account=person_a)
        # Neo Express is failing to run `contract run` inside the batch, if it follows another `contract run` that has
        # arguments, that's why transfer is being executed with call_contract and being added to an invoke
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # this simulates a new block in the blockchain
        # time only changes value when a new block enters the blockchain
        runner.increase_block(time_interval_in_secs=self.REFUND_WAIT_TIME)
        # will be able to refund, because enough time has passed
        invoke_refund_success = runner.run_contract(path, 'refund', account=self.OWNER)

        runner.update_contracts(export_checkpoint=True)

        # The `refund` method uses runtime.time, but BoaTestRunner fails to get it
        transaction_refund = self._validate_execution_result(runner, invoke_refund_success.tx_id, expected_result=True)

        # person_a transferred cryptocurrency to the contract, so only he will be refunded
        transfer_events = []
        # removing possible GAS minting from the List
        for k in transaction_refund.notifications:
            if k.arguments[0] is not None and k.name == 'Transfer':
                transfer_events.append(k)
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        # HTLC returning the tokens
        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(htlc_script_hash, sender)
        self.assertEqual(person_a_script_hash, receiver)
        self.assertEqual(transferred_amount_neo, amount)

    def test_htlc_refund_two_transfers(self):
        path, _ = self.get_deploy_file_paths('htlc.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 10000 * 10 ** 8
        person_a = self.OTHER_ACCOUNT_1
        person_a_script_hash = person_a.script_hash.to_array()
        person_b = self.OTHER_ACCOUNT_2
        person_b_script_hash = person_b.script_hash.to_array()
        secret_hash = hash160(b'unit test')

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_gas(person_a.address, self.GAS_TO_DEPLOY)  # adding GAS to let them be able to invoke contracts
        runner.add_gas(person_b.address, self.GAS_TO_DEPLOY)  # adding GAS to let them be able to invoke contracts
        htlc_contract = runner.deploy_contract(path, account=self.OWNER)

        runner.add_neo(person_a.address, transferred_amount_neo)  # adding NEO that will be swapped
        runner.add_gas(person_b.address, transferred_amount_gas)  # adding GAS that will be swapped

        runner.call_contract(path, 'atomic_swap',
                             person_a_script_hash, constants.NEO_SCRIPT, transferred_amount_neo,
                             person_b_script_hash, constants.GAS_SCRIPT, transferred_amount_gas,
                             secret_hash)

        runner.execute(add_invokes_to_batch=True, account=self.OWNER)
        # Test Runner isn't returning runtime.time value correctly and is returning VMState.FAULT, but the method
        # should work, that's why the invoke is being added to the batch
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)

        htlc_script_hash = htlc_contract.script_hash

        runner.run_contract(constants.NEO_SCRIPT, 'transfer', person_a_script_hash, htlc_script_hash,
                            transferred_amount_neo, None, account=person_a)

        runner.run_contract(constants.GAS_SCRIPT, 'transfer', person_b_script_hash, htlc_script_hash,
                            transferred_amount_gas, None, account=person_b)

        # Neo Express is failing to run `contract run` inside the batch, if it follows another `contract run` that has
        # arguments, that's why the transfers are being update directly
        runner.update_contracts(export_checkpoint=True)

        # this simulates a new block in the blockchain
        # time only changes value when a new block enters the blockchain
        runner.increase_block(time_interval_in_secs=self.REFUND_WAIT_TIME)
        # will be able to refund, because enough time has passed
        invoke_refund_success = runner.run_contract(path, 'refund', account=self.OWNER)

        runner.update_contracts(export_checkpoint=True)

        # The `refund` method uses runtime.time, but BoaTestRunner fails to get it
        transaction_refund = self._validate_execution_result(runner, invoke_refund_success.tx_id, expected_result=True)

        # person_a and person_b transferred cryptocurrency to the contract, so they both will be refunded
        transfer_events = []
        # removing possible GAS minting from the List
        for k in transaction_refund.notifications:
            if k.arguments[0] is not None and k.name == 'Transfer':
                transfer_events.append(k)
        self.assertEqual(2, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))
        self.assertEqual(3, len(transfer_events[1].arguments))

        # HTLC returning the tokens
        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(htlc_script_hash, sender)
        self.assertEqual(person_a_script_hash, receiver)
        self.assertEqual(transferred_amount_neo, amount)

        sender, receiver, amount = transfer_events[1].arguments
        self.assertEqual(htlc_script_hash, sender)
        self.assertEqual(person_b_script_hash, receiver)
        self.assertEqual(transferred_amount_gas, amount)
