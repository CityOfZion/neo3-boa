from boa3 import constants
from boa3.boa3 import Boa3
from boa3.neo import to_script_hash
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTemplate(BoaTest):
    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = to_script_hash(b'NNLi44dJNXtDNSBkofB48aTVYtb1zZrNEs')
    OTHER_ACCOUNT_3 = to_script_hash(b'NZcuGiwRu1QscpmCyxj5XwQBUf6sk7dJJN')

    def test_wrapped_neo_compile(self):
        path = self.get_contract_path('wrapped_neo.py')
        Boa3.compile(path)

    def test_wrapped_neo_symbol(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'symbol')
        self.assertEqual('zNEO', result)

    def test_wrapped_neo_decimals(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'decimals')
        self.assertEqual(8, result)

    def test_wrapped_neo_total_supply(self):
        total_supply = 10_000_000 * 10 ** 8

        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(total_supply, result)

    def test_wrapped_neo_total_balance_of(self):
        total_supply = 10_000_000 * 10 ** 8

        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(total_supply, result)

        # should fail when the script length is not 20
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(10))
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(30))

    def test_wrapped_neo_total_transfer(self):
        transferred_amount = 10 * 10 ** 8  # 10 tokens
        path = self.get_contract_path('wrapped_neo.py')

        engine = TestEngine()

        # should fail if the sender doesn't sign
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, "")
        self.assertEqual(False, result)
        wrapped_neo_address = engine.executed_script_hash.to_array()

        # should fail if the sender doesn't have enough balance
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, transferred_amount, "",
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(False, result)

        # should fail when any of the scripts' length is not 20
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    self.OWNER_SCRIPT_HASH, bytes(10), transferred_amount, "")
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    bytes(10), self.OTHER_ACCOUNT_1, transferred_amount, "")

        # should fail when the amount is less than 0
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, -10, "")

        # fire the transfer event when transferring to yourself
        balance_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OWNER_SCRIPT_HASH, transferred_amount, "",
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(True, result)
        transfer_events = engine.get_events('Transfer', origin=wrapped_neo_address)
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

        # does fire the transfer event when transferring to someone other than yourself
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, "",
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
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

    def test_wrapped_neo_verify(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        # should fail without signature
        result = self.run_smart_contract(engine, path, 'verify')
        self.assertEqual(False, result)

        # should fail if not signed by the owner
        result = self.run_smart_contract(engine, path, 'verify',
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'verify',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(True, result)

    def test_wrapped_neo_burn(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        self.run_smart_contract(engine, path, 'symbol')
        wrapped_neo_address = engine.executed_script_hash.to_array()

        engine.reset_engine()
        engine.add_neo(wrapped_neo_address, 10_000_000 * 10 ** 8)
        burned_amount = 100 * 10 ** 8

        # burning zNEO will end up giving NEO to the one who burned it
        neo_wrapped_before = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_owner_before = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', self.OWNER_SCRIPT_HASH)
        zneo_owner_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        # in this case, NEO will be given to the OWNER_SCRIPT_HASH
        result = self.run_smart_contract(engine, path, 'burn', self.OWNER_SCRIPT_HASH, burned_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertIsVoid(result)

        transfer_events = engine.get_events('Transfer', origin=wrapped_neo_address)
        self.assertGreaterEqual(len(transfer_events), 1)
        wrapped_token_transfer_event = transfer_events[-1]
        self.assertEqual(3, len(wrapped_token_transfer_event.arguments))

        sender, receiver, amount = wrapped_token_transfer_event.arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(self.OWNER_SCRIPT_HASH, sender)
        self.assertEqual(None, receiver)
        self.assertEqual(burned_amount, amount)

        transfer_events = engine.get_events('Transfer', origin=constants.NEO_SCRIPT)
        self.assertGreaterEqual(len(transfer_events), 1)
        neo_transfer_event = transfer_events[-1]
        self.assertEqual(3, len(neo_transfer_event.arguments))

        sender, receiver, amount = neo_transfer_event.arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(wrapped_neo_address, sender)
        self.assertEqual(self.OWNER_SCRIPT_HASH, receiver)
        self.assertEqual(burned_amount, amount)

        # balance after burning
        neo_wrapped_after = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_owner_after = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', self.OWNER_SCRIPT_HASH)
        zneo_owner_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(neo_wrapped_before - burned_amount, neo_wrapped_after)
        self.assertEqual(neo_owner_before + burned_amount, neo_owner_after)
        self.assertEqual(zneo_owner_before - burned_amount, zneo_owner_after)

        # should fail when the script length is not 20
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'burn', bytes(15), burned_amount,
                                    signer_accounts=[self.OWNER_SCRIPT_HASH])
        # or amount is less than 0
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'burn', self.OWNER_SCRIPT_HASH, -1,
                                    signer_accounts=[self.OWNER_SCRIPT_HASH])

    def test_wrapped_neo_approve(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        self.run_smart_contract(engine, path, 'symbol')
        wrapped_neo_address = engine.executed_script_hash.to_array()

        engine.reset_engine()
        engine.add_contract(path.replace('.py', '.nef'))
        allowed_amount = 10 * 10 ** 8

        # this approve will fail, because OTHER_ACCOUNT_1 doesn't have enough zNEO
        result = self.run_smart_contract(engine, wrapped_neo_address, 'approve',
                                         self.OTHER_ACCOUNT_2, allowed_amount,
                                         calling_script_hash=self.OTHER_ACCOUNT_1,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(False, result)

        # OWNER will give zNEO to OTHER_ACCOUNT_1 so that it can approve
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, allowed_amount, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(True, result)

        # this approve will succeed, because OTHER_ACCOUNT_1 have enough zNEO
        result = self.run_smart_contract(engine, wrapped_neo_address, 'approve',
                                         self.OTHER_ACCOUNT_2, allowed_amount,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(True, result)

        # approved fired an event
        approval_events = engine.get_events('Approval')
        self.assertEqual(1, len(approval_events))

        owner, spender, amount = approval_events[0].arguments
        if isinstance(owner, str):
            owner = String(owner).to_bytes()
        if isinstance(spender, str):
            spender = String(spender).to_bytes()
        self.assertEqual(self.OTHER_ACCOUNT_1, owner)
        self.assertEqual(self.OTHER_ACCOUNT_2, spender)
        self.assertEqual(allowed_amount, amount)

    def test_wrapped_neo_allowance(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        self.run_smart_contract(engine, path, 'symbol')
        wrapped_neo_address = engine.executed_script_hash.to_array()

        engine.reset_engine()
        engine.add_contract(path.replace('.py', '.nef'))
        allowed_amount = 10 * 10 ** 8

        # OTHER_ACCOUNT_1 did not approve OTHER_SCRIPT_HASH
        result = self.run_smart_contract(engine, path, 'allowance', self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_2,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(0, result)

        # OWNER will give zNEO to OTHER_ACCOUNT_1 so that it can approve
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, allowed_amount, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(True, result)

        # this approve will succeed, because OTHER_ACCOUNT_1 have enough zNEO
        result = self.run_smart_contract(engine, wrapped_neo_address, 'approve',
                                         self.OTHER_ACCOUNT_2, allowed_amount,
                                         calling_script_hash=self.OTHER_ACCOUNT_1,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(True, result)

        # OTHER_ACCOUNT_1 allowed OTHER_ACCOUNT_2 to spend transferred_amount of zNEO
        result = self.run_smart_contract(engine, path, 'allowance', self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_2,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(allowed_amount, result)

    def test_wrapped_neo_transfer_from(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        self.run_smart_contract(engine, path, 'symbol')
        wrapped_neo_address = engine.executed_script_hash.to_array()

        engine.reset_engine()
        engine.add_contract(path.replace('.py', '.nef'))
        allowed_amount = 10 * 10 ** 8

        # OWNER will give zNEO to OTHER_ACCOUNT_3 so that it can approve another contracts
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_3, 10_000_000 * 10 ** 8, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
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
        self.assertEqual(self.OTHER_ACCOUNT_3, receiver)
        self.assertEqual(10_000_000 * 100_000_000, amount)

        # this approve will succeed, because OTHER_ACCOUNT_3 have enough zNEO
        result = self.run_smart_contract(engine, wrapped_neo_address, 'approve',
                                         self.OTHER_ACCOUNT_1, allowed_amount,
                                         calling_script_hash=self.OTHER_ACCOUNT_3,
                                         signer_accounts=[self.OTHER_ACCOUNT_3])
        self.assertEqual(True, result)

        transferred_amount = allowed_amount

        # this transfer will fail,
        # because OTHER_ACCOUNT_1 is not allowed to transfer more than OTHER_ACCOUNT_3 approved
        result = self.run_smart_contract(engine, path, 'transferFrom', self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_3,
                                         self.OTHER_ACCOUNT_2, transferred_amount + 1 * 10 ** 8, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(False, result)
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(2, len(transfer_events))

        # this transfer will succeed and will fire the Transfer event
        balance_spender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_3)
        balance_receiver_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_2)
        result = self.run_smart_contract(engine, path, 'transferFrom', self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_3,
                                         self.OTHER_ACCOUNT_2, transferred_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(True, result)
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(3, len(transfer_events))
        self.assertEqual(3, len(transfer_events[2].arguments))

        sender, receiver, amount = transfer_events[2].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(self.OTHER_ACCOUNT_3, sender)
        self.assertEqual(self.OTHER_ACCOUNT_2, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring changed the balance
        balance_spender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_3)
        balance_receiver_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_2)
        self.assertEqual(balance_spender_before, balance_spender_after)
        self.assertEqual(balance_sender_before - transferred_amount, balance_sender_after)
        self.assertEqual(balance_receiver_before + transferred_amount, balance_receiver_after)

        # OTHER_ACCOUNT_3 and OTHER_ACCOUNT_1 allowance was reduced to 0
        result = self.run_smart_contract(engine, path, 'allowance', self.OTHER_ACCOUNT_3, self.OTHER_ACCOUNT_1,
                                         signer_accounts=[self.OTHER_ACCOUNT_3])
        self.assertEqual(0, result)

        # this approve will succeed, because OTHER_ACCOUNT_3 have enough zNEO
        result = self.run_smart_contract(engine, wrapped_neo_address, 'approve',
                                         self.OTHER_ACCOUNT_1, allowed_amount,
                                         calling_script_hash=self.OTHER_ACCOUNT_3,
                                         signer_accounts=[self.OTHER_ACCOUNT_3])
        self.assertEqual(True, result)

        transferred_amount = allowed_amount - 4 * 10 ** 8

        result = self.run_smart_contract(engine, path, 'transferFrom', self.OTHER_ACCOUNT_1, self.OTHER_ACCOUNT_3,
                                         self.OTHER_ACCOUNT_2, transferred_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(True, result)

        # OTHER_ACCOUNT_3 and OTHER_ACCOUNT_1 allowance was reduced to allowed_amount - transferred_amount
        result = self.run_smart_contract(engine, path, 'allowance', self.OTHER_ACCOUNT_3, self.OTHER_ACCOUNT_1,
                                         signer_accounts=[self.OTHER_ACCOUNT_3])
        self.assertEqual(allowed_amount - transferred_amount, result)

        # should fail when any of the scripts' length is not 20
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transferFrom',
                                    self.OWNER_SCRIPT_HASH, bytes(10), self.OTHER_ACCOUNT_1, allowed_amount, None)
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transferFrom',
                                    bytes(10), self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, allowed_amount, None)
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transferFrom',
                                    self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, bytes(10), allowed_amount, None)

        # should fail when the amount is less than 0
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transferFrom',
                                    self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_2, -10, None)

    def test_wrapped_neo_on_nep17_payment(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        self.run_smart_contract(engine, path, 'symbol')
        wrapped_neo_address = engine.executed_script_hash.to_array()

        engine.reset_engine()
        engine.add_contract(path.replace('.py', '.nef'))
        minted_amount = 10 * 10 ** 8
        engine.add_neo(self.OTHER_ACCOUNT_1, minted_amount)

        # the smart contract will abort if some address other than NEO calls the onPayment method
        with self.assertRaisesRegex(TestExecutionException, self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'onNEP17Payment', self.OTHER_ACCOUNT_1, minted_amount, None,
                                    signer_accounts=[self.OTHER_ACCOUNT_1])

        neo_wrapped_before = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_aux_before = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', self.OTHER_ACCOUNT_1)
        zneo_aux_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        # transferring NEO to the wrapped_neo_address will mint them
        result = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'transfer',
                                         self.OTHER_ACCOUNT_1, wrapped_neo_address, minted_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual(True, result)

        transfer_events = engine.get_events('Transfer', origin=constants.NEO_SCRIPT)
        self.assertEqual(1, len(transfer_events))
        neo_transfer_event = transfer_events[0]
        self.assertEqual(3, len(neo_transfer_event.arguments))

        sender, receiver, amount = neo_transfer_event.arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(self.OTHER_ACCOUNT_1, sender)
        self.assertEqual(wrapped_neo_address, receiver)
        self.assertEqual(minted_amount, amount)

        transfer_events = engine.get_events('Transfer', origin=wrapped_neo_address)
        self.assertEqual(2, len(transfer_events))
        wrapped_token_transfer_event = transfer_events[1]
        self.assertEqual(3, len(wrapped_token_transfer_event.arguments))

        sender, receiver, amount = wrapped_token_transfer_event.arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(self.OTHER_ACCOUNT_1, receiver)
        self.assertEqual(minted_amount, amount)

        # balance after burning
        neo_wrapped_after = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_aux_after = self.run_smart_contract(engine, constants.NEO_SCRIPT, 'balanceOf', self.OTHER_ACCOUNT_1)
        zneo_aux_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(neo_wrapped_before + minted_amount, neo_wrapped_after)
        self.assertEqual(neo_aux_before - minted_amount, neo_aux_after)
        self.assertEqual(zneo_aux_before + minted_amount, zneo_aux_after)
