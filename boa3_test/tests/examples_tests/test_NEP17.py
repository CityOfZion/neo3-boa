from boa3.boa3 import Boa3
from boa3.constants import GAS_SCRIPT, NEO_SCRIPT
from boa3.neo import to_script_hash
from boa3.neo.cryptography import hash160
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNEP17Template(BoaTest):

    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = bytes(range(20))

    def test_nep17_compile(self):
        path = self.get_contract_path('NEP17.py')
        Boa3.compile(path)

    def test_nep17_deploy(self):
        path = self.get_contract_path('NEP17.py')
        engine = TestEngine()

        # needs the owner signature
        result = self.run_smart_contract(engine, path, method='deploy',
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should return false if the signature isn't from the owner
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # must always return false after first execution
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

    def test_nep17_symbol(self):
        path = self.get_contract_path('NEP17.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'symbol')
        self.assertEqual('NEP17', result)

    def test_nep17_decimals(self):
        path = self.get_contract_path('NEP17.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'decimals')
        self.assertEqual(8, result)

    def test_nep17_total_supply(self):
        total_supply = 10_000_000 * 10 ** 8

        path = self.get_contract_path('NEP17.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(0, result)
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(total_supply, result)

    def test_nep17_total_balance_of(self):
        total_supply = 10_000_000 * 10 ** 8

        path = self.get_contract_path('NEP17.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(total_supply, result)

        # should fail when the script length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(10))
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(30))

    def test_nep17_total_transfer(self):
        transferred_amount = 10 * 10 ** 8  # 10 tokens

        path = self.get_contract_path('NEP17.py')
        engine = TestEngine()

        # should fail before running deploy
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, None,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        # when deploying, the contract will mint tokens to the owner
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(self.OWNER_SCRIPT_HASH, receiver)
        self.assertEqual(10_000_000 * 100_000_000, amount)

        # should fail if the sender doesn't sign
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, None,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should fail if the sender doesn't have enough balance
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, transferred_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    self.OWNER_SCRIPT_HASH, bytes(10), transferred_amount, "")
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    bytes(10), self.OTHER_ACCOUNT_1, transferred_amount, "")

        # should fail when the amount is less than 0
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, -10, None)

        # fire the transfer event when transferring to yourself
        balance_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OWNER_SCRIPT_HASH, transferred_amount, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(2, len(transfer_events))
        self.assertEqual(3, len(transfer_events[1].arguments))

        sender, receiver, amount = transfer_events[1].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(self.OWNER_SCRIPT_HASH, sender)
        self.assertEqual(self.OWNER_SCRIPT_HASH, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring to yourself doesn't change the balance
        balance_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(balance_before, balance_after)

        # does fire the transfer event
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(3, len(transfer_events))
        self.assertEqual(3, len(transfer_events[2].arguments))

        sender, receiver, amount = transfer_events[2].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(self.OWNER_SCRIPT_HASH, sender)
        self.assertEqual(self.OTHER_ACCOUNT_1, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring to someone other than yourself does change the balance
        balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(balance_sender_before - transferred_amount, balance_sender_after)
        self.assertEqual(balance_receiver_before + transferred_amount, balance_receiver_after)

    def test_nep17_onPayment(self):
        transferred_amount = 10 * 10 ** 8  # 10 tokens

        path = self.get_contract_path('NEP17.py')
        engine = TestEngine()

        engine.add_contract(path.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        nep17_address = hash160(output)

        aux_path = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')
        output, manifest = self.compile_and_save(aux_path)
        aux_address = hash160(output)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        # when deploying, the contract will mint tokens to the owner
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(self.OWNER_SCRIPT_HASH, receiver)
        self.assertEqual(10_000_000 * 100_000_000, amount)

        engine.add_neo(aux_address, transferred_amount)
        engine.add_gas(aux_address, transferred_amount)

        # transferring NEO to the smart contract
        # saving the balance before the transfer to be able to compare after it
        neo_balance_sender_before = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', aux_address)
        neo_balance_nep17_before = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', nep17_address)
        nep17_balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', aux_address)

        result = self.run_smart_contract(engine, aux_path, 'calling_transfer', NEO_SCRIPT,
                                         aux_address, nep17_address, transferred_amount, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(3, len(transfer_events))
        self.assertEqual(3, len(transfer_events[1].arguments))
        self.assertEqual(3, len(transfer_events[2].arguments))

        # this is the event NEO emitted
        sender, receiver, amount = transfer_events[1].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(aux_address, sender)
        self.assertEqual(nep17_address, receiver)
        self.assertEqual(transferred_amount, amount)

        # this is the event NEP17 emitted
        sender, receiver, amount = transfer_events[2].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(aux_address, receiver)
        # transferred_amount is multiplied by 10, because this smart contract is minting the NEO received
        self.assertEqual(transferred_amount * 10, amount)

        # saving the balance after the transfer to compare it with the previous data
        neo_balance_sender_after = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', aux_address)
        neo_balance_nep17_after = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', nep17_address)
        nep17_balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', aux_address)

        self.assertEqual(neo_balance_sender_before - transferred_amount, neo_balance_sender_after)
        self.assertEqual(neo_balance_nep17_before + transferred_amount, neo_balance_nep17_after)
        # transferred_amount is multiplied by 10, because this smart contract is minting the NEO received
        self.assertEqual(nep17_balance_sender_before + transferred_amount * 10, nep17_balance_sender_after)

        # transferring GAS to the smart contract
        # saving the balance before the transfer to be able to compare after it
        gas_balance_sender_before = self.run_smart_contract(engine, GAS_SCRIPT, 'balanceOf', aux_address)
        gas_balance_nep17_before = self.run_smart_contract(engine, GAS_SCRIPT, 'balanceOf', nep17_address)
        nep17_balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', aux_address)

        result = self.run_smart_contract(engine, aux_path, 'calling_transfer', GAS_SCRIPT,
                                         aux_address, nep17_address, transferred_amount, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(5, len(transfer_events))
        self.assertEqual(3, len(transfer_events[3].arguments))
        self.assertEqual(3, len(transfer_events[4].arguments))

        # this is the event GAS emitted
        sender, receiver, amount = transfer_events[3].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(aux_address, sender)
        self.assertEqual(nep17_address, receiver)
        self.assertEqual(transferred_amount, amount)

        # this is the event NEP17 emitted
        sender, receiver, amount = transfer_events[4].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(aux_address, receiver)
        # transferred_amount is multiplied by 2, because this smart contract is minting the GAS received
        self.assertEqual(transferred_amount * 2, amount)

        # saving the balance after the transfer to compare it with the previous data
        gas_balance_sender_after = self.run_smart_contract(engine, GAS_SCRIPT, 'balanceOf', aux_address)
        gas_balance_nep17_after = self.run_smart_contract(engine, GAS_SCRIPT, 'balanceOf', nep17_address)
        nep17_balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', aux_address)

        self.assertEqual(gas_balance_sender_before - transferred_amount, gas_balance_sender_after)
        self.assertEqual(gas_balance_nep17_before + transferred_amount, gas_balance_nep17_after)
        # transferred_amount is multiplied by 2, because this smart contract is minting the GAS received
        self.assertEqual(nep17_balance_sender_before + transferred_amount * 2, nep17_balance_sender_after)

        # trying to call onNEP17Transfer() will result in an abort if the one calling it is not NEO or GAS contracts
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'onNEP17Transfer',
                                    self.OWNER_SCRIPT_HASH, transferred_amount, None)

    def test_nep17_verify(self):
        path = self.get_contract_path('NEP17.py')
        engine = TestEngine()

        # should fail without signature
        result = self.run_smart_contract(engine, path, 'verify',
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should fail if not signed by the owner
        result = self.run_smart_contract(engine, path, 'verify',
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'verify',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
