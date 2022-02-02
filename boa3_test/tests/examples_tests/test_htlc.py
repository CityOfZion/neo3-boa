from typing import List

from boa3 import constants
from boa3.boa3 import Boa3
from boa3.neo import to_script_hash
from boa3.neo.cryptography import hash160
from boa3.neo.smart_contract.notification import Notification
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestHTLCTemplate(BoaTest):
    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = bytes(range(20))

    def test_htlc_compile(self):
        path = self.get_contract_path('htlc.py')
        Boa3.compile(path)

    def test_htlc_atomic_swap(self):
        path = self.get_contract_path('htlc.py')
        engine = TestEngine()

        # starting atomic swap by using the atomic_swap method
        result = self.run_smart_contract(engine, path, 'atomic_swap',
                                         self.OWNER_SCRIPT_HASH, constants.NEO_SCRIPT, 10 * 10 ** 8,
                                         self.OTHER_ACCOUNT_1, constants.GAS_SCRIPT, 10000 * 10 ** 8,
                                         hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_htlc_on_nep17_payment(self):
        path = self.get_contract_path('htlc.py')
        engine = TestEngine()
        transferred_amount_neo = 10 * 10 ** 8
        transferred_amount_gas = 10000 * 10 ** 8

        output, manifest = self.get_output(path)
        htlc_address = hash160(output)

        aux_path = self.get_contract_path('examples/auxiliary_contracts', 'auxiliary_contract.py')
        output, manifest = self.get_output(aux_path)
        aux_address = hash160(output)

        aux_path2 = self.get_contract_path('examples/auxiliary_contracts', 'auxiliary_contract_2.py')
        output, manifest = self.get_output(aux_path2)
        aux_address2 = hash160(output)

        engine.add_neo(aux_address, transferred_amount_neo)
        engine.add_gas(aux_address2, transferred_amount_gas)

        # starting atomic swap
        result = self.run_smart_contract(engine, path, 'atomic_swap',
                                         aux_address, constants.NEO_SCRIPT, transferred_amount_neo,
                                         aux_address2, constants.GAS_SCRIPT, transferred_amount_gas,
                                         hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # transfer wil be aborted at onPayment if the transfer is not valid
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, aux_path, 'calling_transfer',
                                    constants.NEO_SCRIPT, aux_address, htlc_address,
                                    transferred_amount_neo - 100, None,
                                    signer_accounts=[self.OWNER_SCRIPT_HASH],
                                    expected_result_type=bool)

        # since the transfer was aborted, it was not registered in the events
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(0, len(transfer_events))

        # saving the balance to compare after the transfer
        balance_neo_sender_before = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', aux_address)
        balance_neo_receiver_before = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', htlc_address)

        # this transfer will be accepted
        result = self.run_smart_contract(engine, aux_path, 'calling_transfer',
                                         constants.NEO_SCRIPT, aux_address, htlc_address, transferred_amount_neo, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # transfer was accepted so it was registered
        transfer_events = engine.get_events('Transfer', constants.NEO_SCRIPT)
        self.assertEqual(1, len(transfer_events))
        neo_transfer_event = transfer_events[0]
        self.assertEqual(3, len(neo_transfer_event.arguments))

        sender, receiver, amount = neo_transfer_event.arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(aux_address, sender)
        self.assertEqual(htlc_address, receiver)
        self.assertEqual(transferred_amount_neo, amount)

        # saving the balance after to compare with the balance before the transfer
        balance_neo_sender_after = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', aux_address)
        balance_neo_receiver_after = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', htlc_address)

        self.assertEqual(balance_neo_sender_before - transferred_amount_neo, balance_neo_sender_after)
        self.assertEqual(balance_neo_receiver_before + transferred_amount_neo, balance_neo_receiver_after)

        # transfer won't be accepted, because amount is wrong
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, aux_path2, 'calling_transfer',
                                    constants.GAS_SCRIPT, aux_address2, htlc_address,
                                    transferred_amount_gas - 100, None,
                                    signer_accounts=[aux_address2],
                                    expected_result_type=bool)

        transfer_events = engine.get_events('Transfer', origin=constants.NEO_SCRIPT)
        # the NEO transfer
        self.assertEqual(1, len(transfer_events))

        # saving the balance to compare after the transfer
        balance_gas_sender_before = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', aux_address2)
        balance_gas_receiver_before = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', htlc_address)

        # this transfer will be accepted
        result = self.run_smart_contract(engine, aux_path2, 'calling_transfer',
                                         constants.GAS_SCRIPT, aux_address2, htlc_address, transferred_amount_gas, None,
                                         signer_accounts=[aux_address2],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # the transfer was accepted so it was registered
        transfer_events = engine.get_events('Transfer', origin=constants.GAS_SCRIPT)
        self.assertGreaterEqual(len(transfer_events), 1)
        gas_transfer_event = transfer_events[-1]
        self.assertEqual(3, len(gas_transfer_event.arguments))

        sender, receiver, amount = gas_transfer_event.arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(aux_address2, sender)
        self.assertEqual(htlc_address, receiver)
        self.assertEqual(transferred_amount_gas, amount)

        # saving the balance after to compare with the balance before the transfer
        balance_gas_sender_after = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', aux_address2)
        balance_gas_receiver_after = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', htlc_address)

        self.assertEqual(balance_gas_sender_before - transferred_amount_gas, balance_gas_sender_after)
        self.assertEqual(balance_gas_receiver_before + transferred_amount_gas, balance_gas_receiver_after)

    def test_htlc_withdraw(self):
        path = self.get_contract_path('htlc.py')
        engine = TestEngine()
        transferred_amount_neo = 10 * 10 ** 8
        transferred_amount_gas = 10000 * 10 ** 8

        output, manifest = self.get_output(path)
        htlc_address = hash160(output)

        aux_path = self.get_contract_path('examples/auxiliary_contracts', 'auxiliary_contract.py')
        output, manifest = self.get_output(aux_path)
        aux_address = hash160(output)

        aux_path2 = self.get_contract_path('examples/auxiliary_contracts', 'auxiliary_contract_2.py')
        output, manifest = self.get_output(aux_path2)
        aux_address2 = hash160(output)

        engine.add_neo(aux_address, transferred_amount_neo)
        engine.add_gas(aux_address2, transferred_amount_gas)

        # saving the balance to compare after the withdraw
        balance_neo_person_a_before = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', aux_address)
        balance_neo_person_b_before = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', aux_address2)
        balance_neo_htlc_before = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', htlc_address)
        balance_gas_person_a_before = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', aux_address)
        balance_gas_person_b_before = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', aux_address2)
        balance_gas_htlc_before = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', htlc_address)

        # starting atomic swap by using the atomic_swap method
        result = self.run_smart_contract(engine, path, 'atomic_swap',
                                         aux_address, constants.NEO_SCRIPT, transferred_amount_neo,
                                         aux_address2, constants.GAS_SCRIPT, transferred_amount_gas,
                                         hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # won't be able to withdraw, because no one transferred cryptocurrency to the smart contract
        result = self.run_smart_contract(engine, path, 'withdraw', 'unit test',
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, aux_path, 'calling_transfer',
                                         constants.NEO_SCRIPT, aux_address, htlc_address, transferred_amount_neo, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('Transfer', origin=constants.NEO_SCRIPT)
        self.assertEqual(1, len(transfer_events))

        result = self.run_smart_contract(engine, aux_path2, 'calling_transfer',
                                         constants.GAS_SCRIPT, aux_address2, htlc_address, transferred_amount_gas, None,
                                         signer_accounts=[aux_address2],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('Transfer', constants.GAS_SCRIPT)
        self.assertEqual(2, len(transfer_events))

        # the withdraw will fail, because the secret is wrong
        result = self.run_smart_contract(engine, path, 'withdraw', 'wrong one',
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # the withdraw will occur
        result = self.run_smart_contract(engine, path, 'withdraw', 'unit test',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # the transfer were accepted so they were registered
        transfer_events = engine.get_events('Transfer', origin=constants.GAS_SCRIPT)
        self.assertGreaterEqual(len(transfer_events), 1)
        gas_transfer_event = transfer_events[-1]
        self.assertEqual(3, len(gas_transfer_event.arguments))

        transfer_events = engine.get_events('Transfer', constants.NEO_SCRIPT)
        self.assertGreaterEqual(len(transfer_events), 1)
        neo_transfer_event = transfer_events[-1]
        self.assertEqual(3, len(neo_transfer_event.arguments))

        sender, receiver, amount = gas_transfer_event.arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(htlc_address, sender)
        self.assertEqual(aux_address, receiver)
        self.assertEqual(transferred_amount_gas, amount)

        sender, receiver, amount = neo_transfer_event.arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(htlc_address, sender)
        self.assertEqual(aux_address2, receiver)
        self.assertEqual(transferred_amount_neo, amount)

        # saving the balance after to compare with the balance before the transfer
        minted_gas_per_neo_transfer = int(transferred_amount_neo * 0.5)
        balance_neo_person_a_after = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', aux_address)
        balance_neo_person_b_after = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', aux_address2)
        balance_neo_htlc_after = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', htlc_address)
        balance_gas_person_a_after = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', aux_address)
        balance_gas_person_b_after = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', aux_address2)
        balance_gas_htlc_after = self.run_smart_contract(engine, constants.GAS_SCRIPT, 'balanceOf', htlc_address)

        self.assertEqual(balance_neo_person_a_before - transferred_amount_neo, balance_neo_person_a_after)
        self.assertEqual(balance_neo_person_b_before + transferred_amount_neo, balance_neo_person_b_after)
        self.assertEqual(balance_neo_htlc_before, balance_neo_htlc_after)
        self.assertEqual(balance_gas_person_a_before + transferred_amount_gas + minted_gas_per_neo_transfer,
                         balance_gas_person_a_after)
        self.assertEqual(balance_gas_person_b_before - transferred_amount_gas, balance_gas_person_b_after)
        self.assertEqual(balance_gas_htlc_before, balance_gas_htlc_after)

    def test_htlc_refund(self):
        path = self.get_contract_path('htlc.py')
        engine = TestEngine()
        transferred_amount_neo = 10 * 10 ** 8
        transferred_amount_gas = 10000 * 10 ** 8

        output, manifest = self.get_output(path)
        htlc_address = hash160(output)

        aux_path = self.get_contract_path('examples/auxiliary_contracts', 'auxiliary_contract.py')
        output, manifest = self.get_output(aux_path)
        aux_address = hash160(output)

        aux_path2 = self.get_contract_path('examples/auxiliary_contracts', 'auxiliary_contract_2.py')
        output, manifest = self.get_output(aux_path2)
        aux_address2 = hash160(output)

        engine.add_neo(aux_address, transferred_amount_neo)
        engine.add_gas(aux_address2, transferred_amount_gas)

        result = self.run_smart_contract(engine, path, 'atomic_swap',
                                         aux_address, constants.NEO_SCRIPT, transferred_amount_neo,
                                         aux_address2, constants.GAS_SCRIPT, transferred_amount_gas,
                                         hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # won't be able to refund, because not enough time has passed
        result = self.run_smart_contract(engine, path, 'refund',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # this simulates a new block in the blockchain
        # time only changes value when a new block enters the blockchain
        engine.increase_block()
        # will be able to refund, because enough time has passed
        result = self.run_smart_contract(engine, path, 'refund',
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        transfer_events: List[Notification] = []
        # no one transferred cryptocurrency to the contract, so no one was refunded and no Transfer occurred
        # removing possible GAS minting from the List
        for k in engine.get_events('Transfer'):
            if k.arguments[0] is not None:
                transfer_events.append(k)
        self.assertEqual(0, len(transfer_events))

        # starting atomic swap by using the atomic_swap method
        result = self.run_smart_contract(engine, path, 'atomic_swap',
                                         aux_address, constants.NEO_SCRIPT, transferred_amount_neo,
                                         aux_address2, constants.GAS_SCRIPT, transferred_amount_gas,
                                         hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, aux_path, 'calling_transfer',
                                         constants.NEO_SCRIPT, aux_address, htlc_address, transferred_amount_neo, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        for k in engine.get_events('Transfer'):
            if k.arguments[0] is not None:
                transfer_events.append(k)
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        engine.increase_block()
        # will be able to refund, because enough time has passed
        result = self.run_smart_contract(engine, path, 'refund',
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # OWNER transferred cryptocurrency to the contract, so only he will be refunded
        transfer_events = []
        # removing possible GAS minting from the List
        for k in engine.get_events('Transfer'):
            if k.arguments[0] is not None:
                transfer_events.append(k)
        self.assertEqual(2, len(transfer_events))
        self.assertEqual(3, len(transfer_events[1].arguments))

        # HTLC returning the tokens
        sender, receiver, amount = transfer_events[1].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(htlc_address, sender)
        self.assertEqual(aux_address, receiver)
        self.assertEqual(transferred_amount_neo, amount)

        result = self.run_smart_contract(engine, path, 'atomic_swap',
                                         aux_address, constants.NEO_SCRIPT, transferred_amount_neo,
                                         aux_address2, constants.GAS_SCRIPT, transferred_amount_gas,
                                         hash160(String('unit test').to_bytes()),
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, aux_path, 'calling_transfer',
                                         constants.NEO_SCRIPT, aux_address, htlc_address, transferred_amount_neo, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = []
        for k in engine.get_events('Transfer'):
            if k.arguments[0] is not None:
                transfer_events.append(k)
        self.assertEqual(3, len(transfer_events))
        self.assertEqual(3, len(transfer_events[2].arguments))

        result = self.run_smart_contract(engine, aux_path2, 'calling_transfer',
                                         constants.GAS_SCRIPT, aux_address2, htlc_address, transferred_amount_gas, None,
                                         signer_accounts=[aux_address2],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = []
        for k in engine.get_events('Transfer'):
            if k.arguments[0] is not None:
                transfer_events.append(k)
        self.assertEqual(4, len(transfer_events))
        self.assertEqual(3, len(transfer_events[3].arguments))

        engine.increase_block()
        # will be able to refund, because enough time has passed
        result = self.run_smart_contract(engine, path, 'refund',
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # OWNER and OTHER_ACCOUNT transferred cryptocurrency to the contract, so they both will be refunded
        transfer_events = []
        # removing possible GAS minting from the List
        for k in engine.get_events('Transfer'):
            if k.arguments[0] is not None:
                transfer_events.append(k)
        self.assertEqual(6, len(transfer_events))
        self.assertEqual(3, len(transfer_events[4].arguments))
        self.assertEqual(3, len(transfer_events[5].arguments))

        sender, receiver, amount = transfer_events[4].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(htlc_address, sender)
        self.assertEqual(aux_address, receiver)
        self.assertEqual(transferred_amount_neo, amount)

        sender, receiver, amount = transfer_events[5].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(htlc_address, sender)
        self.assertEqual(aux_address2, receiver)
        self.assertEqual(transferred_amount_gas, amount)
