from boa3.boa3 import Boa3
from boa3.neo import to_script_hash
from boa3.neo.cryptography import hash160
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
        transfer_events = engine.get_events('Transfer')
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
        transfer_events = engine.get_events('Transfer')
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

    def test_nep17_onPayment(self):
        transferred_amount = 10 * 10 ** 8  # 10 tokens

        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        path_native_tokens = '%s/boa3_test/examples/test_native/native_token_methods.py' % self.dirname
        engine = TestEngine(self.dirname)

        engine.add_contract(path.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        nep17_address = hash160(output)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        engine.add_gas(self.OWNER_SCRIPT_HASH, transferred_amount)
        engine.add_neo(self.OTHER_ACCOUNT_1, transferred_amount)

        # fire the Transfer event if sender is NEO when transferring to NEP17 script hash
        neo_balance_sender_before = self.run_smart_contract(engine, path_native_tokens, 'balanceOf_neo', self.OWNER)
        neo_balance_nep17_before = self.run_smart_contract(engine, path_native_tokens, 'balanceOf_neo', nep17_address)
        nep17_balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)

        result = self.run_smart_contract(engine, path_native_tokens, 'transfer_neo', nep17_address, transferred_amount,
                                         '',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        transfer_events = engine.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(sender).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(self.OWNER_SCRIPT_HASH, receiver)
        self.assertEqual(transferred_amount * 10, amount)

        # balance changed
        neo_balance_sender_after = self.run_smart_contract(engine, path_native_tokens, 'balanceOf_neo', self.OWNER)
        neo_balance_nep17_after = self.run_smart_contract(engine, path_native_tokens, 'balanceOf_neo', nep17_address)
        nep17_balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(neo_balance_sender_before - transferred_amount, neo_balance_sender_after)
        self.assertEqual(neo_balance_nep17_before + transferred_amount, neo_balance_nep17_after)
        self.assertEqual(nep17_balance_sender_before + transferred_amount * 10, nep17_balance_sender_after)

        # fire the Transfer event if sender is GAS when transferring to NEP17 script hash
        gas_balance_sender_before = self.run_smart_contract(engine, path_native_tokens, 'balanceOf_gas', self.OWNER)
        gas_balance_nep17_before = self.run_smart_contract(engine, path_native_tokens, 'balanceOf_gas', nep17_address)
        nep17_balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)

        result = self.run_smart_contract(engine, path_native_tokens, 'transfer_gas', nep17_address, transferred_amount,
                                         '',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        transfer_events = engine.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(sender).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(self.OWNER_SCRIPT_HASH, receiver)
        self.assertEqual(transferred_amount * 10, amount)

        # balance changed
        gas_balance_sender_after = self.run_smart_contract(engine, path_native_tokens, 'balanceOf_gas', self.OWNER)
        gas_balance_nep17_after = self.run_smart_contract(engine, path_native_tokens, 'balanceOf_gas', nep17_address)
        nep17_balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(gas_balance_sender_before - transferred_amount, gas_balance_sender_after)
        self.assertEqual(gas_balance_nep17_before + transferred_amount, gas_balance_nep17_after)
        self.assertEqual(nep17_balance_sender_before + transferred_amount * 10, nep17_balance_sender_after)

        # does not fire the transfer event when transferring to a smart contract with the incorrect information
        nep17_balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)

        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    self.OWNER_SCRIPT_HASH, nep17_address, transferred_amount, "",
                                    signer_accounts=[self.OWNER_SCRIPT_HASH],
                                    expected_result_type=bool)

        transfer_events = engine.get_events('Transfer')
        self.assertEqual(0, len(transfer_events))
    
        # balance did not change
        nep17_balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(nep17_balance_sender_before, nep17_balance_sender_after)

    """
    def test_nep17_mint(self):
        transferred_amount = 10 * 10 ** 8  # 10 tokens

        path = '%s/boa3_test/examples/NEP17.py' % self.dirname
        engine = TestEngine(self.dirname)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        transfer_events = engine.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))

        # AssertionError will be raised if amount is less than 0 and balance won't change
        nep17_balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'mint', self.OWNER_SCRIPT_HASH, -transferred_amount,
                                    signer_accounts=[self.OWNER_SCRIPT_HASH],
                                    expected_result_type=bool)

        transfer_events = engine.get_events('Transfer')
        self.assertEqual(0, len(transfer_events))
        nep17_balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(nep17_balance_sender_before, nep17_balance_sender_after)

        # Transfer event won't be fired if sender sends a amount equals to 0
        nep17_balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        result = self.run_smart_contract(engine, path, 'mint', self.OWNER_SCRIPT_HASH, 0,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)

        transfer_events = engine.get_events('Transfer')
        self.assertEqual(0, len(transfer_events))
        nep17_balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(nep17_balance_sender_before, nep17_balance_sender_after)

        # Transfer event will be fired if sender sends a amount greater than 0
        nep17_balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        result = self.run_smart_contract(engine, path, 'mint', self.OWNER_SCRIPT_HASH, transferred_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(nep17_balance_sender_before, nep17_balance_sender_after)

        transfer_events = engine.get_events('Transfer')
        self.assertEqual(1, len(transfer_events))
        nep17_balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(nep17_balance_sender_before + transferred_amount, nep17_balance_sender_after)
    """

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
