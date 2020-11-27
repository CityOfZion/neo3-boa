from boa3.boa3 import Boa3
from boa3.neo import to_script_hash
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTemplate(BoaTest):

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')

    # region HelloWorld

    def test_hello_world_compile(self):
        path = '%s/boa3_test/examples/HelloWorld.py' % self.dirname
        Boa3.compile(path)

    def test_hello_world_main(self):
        path = '%s/boa3_test/examples/HelloWorld.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsNone(result)

        self.assertTrue(b'hello' in engine.storage)
        self.assertEqual(b'world', engine.storage[b'hello'])

    # endregion

    # region nep5

    def test_nep5_compile(self):
        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        Boa3.compile(path)

    def test_nep5_deploy(self):
        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        engine = TestEngine(self.dirname)

        # needs the owner signature
        result = self.run_smart_contract(engine, path, 'deploy')
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

        # should return false if the signature isn't from the owner
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OTHER_ACCOUNT])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(True, result)

        # must always return false after first execution
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

    def test_nep5_name(self):
        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'name')
        self.assertEqual('NEP5 Standard', result)

    def test_nep5_symbol(self):
        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'symbol')
        self.assertEqual('NEP5', result)

    def test_nep5_decimals(self):
        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'decimals')
        self.assertEqual(8, result)

    def test_nep5_total_supply(self):
        total_supply = 10_000_000 * 10 ** 8

        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(total_supply, result)

    def test_nep5_total_balance_of(self):
        total_supply = 10_000_000 * 10 ** 8

        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(total_supply, result)

        # should fail when the script length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(10))
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(30))

    def test_nep5_total_transfer(self):
        transfered_amount = 10 * 10 ** 8  # 10 tokens

        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        engine = TestEngine(self.dirname)

        # should fail before running deploy
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT, transfered_amount)
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(True, result)

        # should fail if the sender doesn't sign
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT, transfered_amount)
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

        # other account doesn't have enough balance
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OTHER_ACCOUNT, self.OWNER_SCRIPT_HASH, transfered_amount,
                                         signer_accounts=[self.OTHER_ACCOUNT])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    self.OWNER_SCRIPT_HASH, bytes(10), transfered_amount)
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    bytes(10), self.OTHER_ACCOUNT, transfered_amount)

        # should fail when the amount is less than 0
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    self.OTHER_ACCOUNT, self.OWNER_SCRIPT_HASH, -10)

        # doesn't fire the transfer event when transferring to yourself
        balance_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OWNER_SCRIPT_HASH, transfered_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(True, result)
        transfer_events = engine.get_events('transfer')
        self.assertEqual(0, len(transfer_events))

        # transferring to yourself doesn't change the balance
        balance_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(balance_before, balance_after)

        # doesn't fire the transfer event when transferring to yourself
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT, transfered_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
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
        self.assertEqual(self.OTHER_ACCOUNT, receiver)
        self.assertEqual(transfered_amount, amount)

        # transferring to yourself doesn't change the balance
        balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT)
        self.assertEqual(balance_sender_before - transfered_amount, balance_sender_after)
        self.assertEqual(balance_receiver_before + transfered_amount, balance_receiver_after)

    def test_nep5_verify(self):
        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        engine = TestEngine(self.dirname)

        # should fail without signature
        result = self.run_smart_contract(engine, path, 'verify')
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

        # should fail if not signed by the owner
        result = self.run_smart_contract(engine, path, 'verify',
                                         signer_accounts=[self.OTHER_ACCOUNT])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'verify',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(True, result)

    # endregion

    # region ico

    def test_ico_compile(self):
        path = '%s/boa3_test/examples/ico.py' % self.dirname
        Boa3.compile(path)

    def test_ico_deploy(self):
        path = '%s/boa3_test/examples/ico.py' % self.dirname
        engine = TestEngine(self.dirname)

        # needs the owner signature
        result = self.run_smart_contract(engine, path, 'deploy')
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

        # should return false if the signature isn't from the owner
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OTHER_ACCOUNT])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(True, result)

        # must always return false after first execution
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        if isinstance(result, int) and result in (False, True):
            result = bool(result)
        self.assertEqual(False, result)

    # endregion
