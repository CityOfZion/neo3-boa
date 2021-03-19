from boa3.boa3 import Boa3
from boa3.neo import to_script_hash
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTemplate(BoaTest):

    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = bytes(range(20))

    KYC_WHITELIST_PREFIX = b'KYCWhitelistApproved'

    def test_ico_compile(self):
        path = self.get_contract_path('ico.py')
        Boa3.compile(path)

    def test_ico_deploy(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()

        # needs the owner signature
        result = self.run_smart_contract(engine, path, 'deploy',
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

    def test_ico_verify(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'verify',
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'verify',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_ico_totalSupply(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()
        total_supply = 10_000_000 * 10 ** 8

        result = self.run_smart_contract(engine, path, 'totalSupply',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'totalSupply',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(total_supply, result)

    def test_ico_symbol(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'symbol')
        self.assertEqual('ICO', result)

    def test_ico_decimals(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'decimals')
        self.assertEqual(8, result)

    def test_ico_total_balance_of(self):
        total_supply = 10_000_000 * 10 ** 8

        path = self.get_contract_path('ico.py')
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

    def test_ico_kyc_register(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()

        # don't include if not signed by the administrator
        result = self.run_smart_contract(engine, path, 'kyc_register',
                                         [self.OWNER_SCRIPT_HASH, bytes(22)])
        self.assertEqual(0, result)

        # don't include script hashes with size different than 20
        result = self.run_smart_contract(engine, path, 'kyc_register',
                                         [bytes(40), self.OWNER_SCRIPT_HASH, bytes(12)],
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(1, result)
        storage_value = engine.storage_get(self.KYC_WHITELIST_PREFIX + self.OWNER_SCRIPT_HASH, path)
        self.assertIsNotNone(storage_value)

        # script hashes already registered are returned as well
        result = self.run_smart_contract(engine, path, 'kyc_register',
                                         [self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1],
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(2, result)
        storage_value = engine.storage_get(self.KYC_WHITELIST_PREFIX + self.OTHER_ACCOUNT_1, path)
        self.assertIsNotNone(storage_value)

    def test_ico_kyc_remove(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()

        # don't remove if not signed by the administrator
        result = self.run_smart_contract(engine, path, 'kyc_remove',
                                         [self.OWNER_SCRIPT_HASH, bytes(22)])
        self.assertEqual(0, result)

        # script hashes that weren't registered are returned as well
        self.assertTrue(self.KYC_WHITELIST_PREFIX + self.OTHER_ACCOUNT_1 not in engine.storage)
        result = self.run_smart_contract(engine, path, 'kyc_remove',
                                         [self.OTHER_ACCOUNT_1],
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(1, result)
        self.assertTrue(self.KYC_WHITELIST_PREFIX + self.OTHER_ACCOUNT_1 not in engine.storage)

        # don't include script hashes with size different than 20
        result = self.run_smart_contract(engine, path, 'kyc_remove',
                                         [bytes(40), self.OWNER_SCRIPT_HASH, bytes(12)],
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(1, result)

    def test_ico_approve(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()

        approved_amount = 100 * 10 ** 8

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'approve',
                                    self.OWNER_SCRIPT_HASH, bytes(10), approved_amount)
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'approve',
                                    bytes(10), self.OTHER_ACCOUNT_1, approved_amount)

        # should fail when the amount is less than 0
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'approve',
                                    self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, -10)

        # should fail if the origin doesn't sign
        result = self.run_smart_contract(engine, path, 'approve',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, approved_amount,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should fail if origin and target are the same
        result = self.run_smart_contract(engine, path, 'approve',
                                         self.OWNER_SCRIPT_HASH, self.OWNER_SCRIPT_HASH, approved_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should fail if any of the addresses is not included in the kyc
        result = self.run_smart_contract(engine, path, 'approve',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, approved_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'kyc_register',
                                         [self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1],
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(2, result)

        # should fail if the origin's balance is less than passed amount
        result = self.run_smart_contract(engine, path, 'approve',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, approved_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # initialize account and owner's balance
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'approve',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, approved_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_ico_allowance(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()

        approved_amount = 100 * 10 ** 8

        result = self.run_smart_contract(engine, path, 'allowance', self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'kyc_register',
                                         [self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1],
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'approve',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, approved_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'allowance', self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1)
        self.assertEqual(approved_amount, result)

    def test_ico_transferFrom(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()

        transferred_amount = 100 * 10 ** 8

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transferFrom',
                                    self.OWNER_SCRIPT_HASH, bytes(10), self.OTHER_ACCOUNT_2, transferred_amount, None)
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transferFrom',
                                    bytes(10), self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_2, transferred_amount, None)
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transferFrom',
                                    self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, bytes(30), transferred_amount, None)

        # should fail when the amount is less than 0
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transferFrom',
                                    self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_2, -10, None)

        # should fail if the sender doesn't sign
        result = self.run_smart_contract(engine, path, 'transferFrom',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_2,
                                         transferred_amount, None,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should fail if the allowed amount is less than the given amount
        result = self.run_smart_contract(engine, path, 'transferFrom',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_2,
                                         transferred_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'kyc_register',
                                         [self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1],
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(2, result)

        result = self.run_smart_contract(engine, path, 'approve',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount * 2,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # doesn't fire the transfer event when transferring to yourself or amount is zero
        balance_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        result = self.run_smart_contract(engine, path, 'transferFrom',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH,
                                         transferred_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        self.assertEqual(0, len(engine.get_events('transfer')))
        balance_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(balance_after, balance_before)

        balance_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        result = self.run_smart_contract(engine, path, 'transferFrom',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_1,
                                         transferred_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        self.assertEqual(0, len(engine.get_events('transfer')))
        balance_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(balance_after, balance_before)

        result = self.run_smart_contract(engine, path, 'transferFrom',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_2, 0, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        self.assertEqual(0, len(engine.get_events('transfer')))

        balance_originator_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        balance_receiver_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_2)
        result = self.run_smart_contract(engine, path, 'transferFrom',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_2,
                                         transferred_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        balance_originator_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(balance_originator_before, balance_originator_after)
        balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(balance_sender_before, balance_sender_after)
        balance_receiver_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_2)
        self.assertEqual(balance_receiver_before, balance_receiver_after)

    def test_ico_mint(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # should fail if amount is a negative number
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'mint', -10 * 10**8)

        minted_amount = 10_000 * 10 ** 8
        # should fail if not signed by the administrator
        result = self.run_smart_contract(engine, path, 'mint', minted_amount,
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        total_supply_before = self.run_smart_contract(engine, path, 'totalSupply')
        owner_balance_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)

        result = self.run_smart_contract(engine, path, 'mint', minted_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        total_supply_after = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(total_supply_before + minted_amount, total_supply_after)
        owner_balance_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(owner_balance_before + minted_amount, owner_balance_after)

    def test_ico_refund(self):
        path = self.get_contract_path('ico.py')
        engine = TestEngine()
        transferred_amount = 10_000

        # should fail script hash length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'refund', bytes(10), transferred_amount, transferred_amount)

        # should fail no amount is a positive number
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'refund', self.OWNER_SCRIPT_HASH, 0, 0)

        # should fail if not signed by the owner
        result = self.run_smart_contract(engine, path, 'refund',
                                         self.OWNER_SCRIPT_HASH, transferred_amount, transferred_amount)
        self.assertEqual(False, result)

        # TODO: Test if the refund is successful when update the TestEngine to make Neo/Gas transfers
