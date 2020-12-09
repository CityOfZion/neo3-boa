# region nep17
from boa3.boa3 import Boa3
from boa3.neo import to_script_hash
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException

from boa3_test.tests.test_classes.testengine import TestEngine

class TestTemplate(BoaTest):

    #Testing private key: <PrivateKey>
    #Testing PublicKey: <PublicKey>
    #Testing Address: <Address>

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = bytes(range(20))

    def test_nep17_compile(self):
        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        Boa3.compile(path)


    def test_nep17_deploy(self):
        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        engine = TestEngine(self.dirname)

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
        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'symbol')
        self.assertEqual('NEP17', result)


    def test_nep17_decimals(self):
        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'decimals')
        self.assertEqual(8, result)


    def test_nep17_total_supply(self):
        total_supply = 10_000_000 * 10 ** 8

        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(total_supply, result)


    def test_nep17_total_balance_of(self):
        total_supply = 10_000_000 * 10 ** 8

        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        engine = TestEngine(self.dirname)
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

        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        engine = TestEngine(self.dirname)

        # should fail before running deploy
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, "",
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # should fail if the sender doesn't sign
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, "",
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should fail if the sender doesn't have enough balance
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, transferred_amount, "",
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
                                    self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, -10, "")

        # doesn't fire the transfer event when transferring to yourself
        balance_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OWNER_SCRIPT_HASH, transferred_amount, "",
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('transfer')
        self.assertEqual(0, len(transfer_events))

        # transferring to yourself doesn't change the balance
        balance_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(balance_before, balance_after)

        # does fire the transfer event when transferring to someone other than yourself
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, "",
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(sender).to_bytes()
        self.assertEqual(self.OWNER_SCRIPT_HASH, sender)
        self.assertEqual(self.OTHER_ACCOUNT_1, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring to someone other than yourself does change the balance
        balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(balance_sender_before - transferred_amount, balance_sender_after)
        self.assertEqual(balance_receiver_before + transferred_amount, balance_receiver_after)


    def test_nep17_transfer_to_smart_contract(self):
        transferred_amount = 10 * 10 ** 8  # 10 tokens

        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        contract_path = '%s/boa3_test/examples/nep17onPaymentContract.py' % self.dirname
        engine = TestEngine(self.dirname)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, contract_path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # fire the transfer event when transferring to a smart contract with the correct data
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_before = self.run_smart_contract(engine, contract_path, 'get_balance')
        contract_address = self.run_smart_contract(engine, contract_path, 'get_address')
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, contract_address, transferred_amount,
                                         ['NEP17', 'password'],
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(sender).to_bytes()
        self.assertEqual(self.OWNER_SCRIPT_HASH, sender)
        self.assertEqual(contract_address, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring to another smart_contract does change the balance
        balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_after = self.run_smart_contract(engine, path, 'get_balance', contract_address)
        self.assertEqual(balance_sender_before - transferred_amount, balance_sender_after)
        self.assertEqual(balance_receiver_before + transferred_amount, balance_receiver_after)
        '''
        # does not fire the transfer event when transferring to a smart contract with the incorrect data
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_before = self.run_smart_contract(engine, contract_path, 'get_balance')
        contract_address = self.run_smart_contract(engine, contract_path, 'get_address')
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    self.OWNER_SCRIPT_HASH, contract_address, transferred_amount,
                                    ['NEP17', 'wrong password'],
                                    signer_accounts=[self.OWNER_SCRIPT_HASH],
                                    expected_result_type=bool)
    
        transfer_events = engine.get_events('transfer')
        self.assertEqual(1, len(transfer_events))
    
        # transferring to another smart_contract does not change the balance
        balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_after = self.run_smart_contract(engine, path, 'get_balance', contract_address)
        self.assertEqual(balance_sender_before - transferred_amount, balance_sender_after)
        self.assertEqual(balance_receiver_before + transferred_amount, balance_receiver_after)
        '''


    def test_nep17_verify(self):
        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        engine = TestEngine(self.dirname)

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

    # endregion
