from boa3.boa3 import Boa3
from boa3.constants import NEO_SCRIPT
from boa3.neo import to_script_hash
from boa3.neo.cryptography import hash160
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTemplate(BoaTest):

    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = bytes(range(20))

    def test_wrapped_neo_compile(self):
        path = self.get_contract_path('wrapped_neo.py')
        Boa3.compile(path)

    def test_wrapped_neo_deploy(self):
        path = self.get_contract_path('wrapped_neo.py')
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
        self.assertEqual(0, result)
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(total_supply, result)

    def test_wrapped_neo_total_balance_of(self):
        total_supply = 10_000_000 * 10 ** 8

        path = self.get_contract_path('wrapped_neo.py')
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

    def test_wrapped_neo_total_transfer(self):
        transferred_amount = 10 * 10 ** 8  # 10 tokens

        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        # should fail before running deploy
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, "",
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

        # fire the transfer event when transferring to yourself
        balance_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OWNER_SCRIPT_HASH, transferred_amount, "",
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

        # does fire the transfer event when transferring to someone other than yourself
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        balance_receiver_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_1, transferred_amount, "",
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

    def test_wrapped_neo_verify(self):
        path = self.get_contract_path('wrapped_neo.py')
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

    def test_wrapped_neo_burn(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()

        output, manifest = self.compile_and_save(path)
        wrapped_neo_address = hash160(output)

        engine.add_neo(wrapped_neo_address, 10_000_000 * 10**8)
        burned_amount = 100 * 10**8

        # deploying this smart contract will give 10m total supply * 10^8 zNEOs to OWNER
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

        # burning zNEO will end up giving NEO to the one who burned it
        neo_wrapped_before = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_owner_before = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', self.OWNER_SCRIPT_HASH)
        zneo_owner_before = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        # in this case, NEO will be given to the OWNER_SCRIPT_HASH
        result = self.run_smart_contract(engine, path, 'burn', self.OWNER_SCRIPT_HASH, burned_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertIsVoid(result)

        transfer_events = engine.get_events('Transfer')
        self.assertEqual(3, len(transfer_events))
        self.assertEqual(3, len(transfer_events[1].arguments))

        sender, receiver, amount = transfer_events[1].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(self.OWNER_SCRIPT_HASH, sender)
        self.assertEqual(None, receiver)
        self.assertEqual(burned_amount, amount)

        self.assertEqual(3, len(transfer_events[2].arguments))

        sender, receiver, amount = transfer_events[2].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(wrapped_neo_address, sender)
        self.assertEqual(self.OWNER_SCRIPT_HASH, receiver)
        self.assertEqual(burned_amount, amount)

        # balance after burning
        neo_wrapped_after = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_owner_after = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', self.OWNER_SCRIPT_HASH)
        zneo_owner_after = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(neo_wrapped_before - burned_amount, neo_wrapped_after)
        self.assertEqual(neo_owner_before + burned_amount, neo_owner_after)
        self.assertEqual(zneo_owner_before - burned_amount, zneo_owner_after)

        # should fail when the script length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'burn', bytes(15), burned_amount,
                                    signer_accounts=[self.OWNER_SCRIPT_HASH])
        # or amount is less than 0
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'burn', self.OWNER_SCRIPT_HASH, -1,
                                    signer_accounts=[self.OWNER_SCRIPT_HASH])

    def test_wrapped_neo_approve(self):
        path = self.get_contract_path('wrapped_neo.py')
        path_aux_contract = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')
        engine = TestEngine()
        engine.add_contract(path.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        wrapped_neo_address = hash160(output)
        output, manifest = self.compile_and_save(path_aux_contract)
        aux_contract_address = hash160(output)

        allowed_amount = 10 * 10 ** 8

        # this approve will fail, because aux_contract_address doesn't have enough zNEO
        result = self.run_smart_contract(engine, path_aux_contract, 'calling_approve',
                                         wrapped_neo_address, self.OTHER_ACCOUNT_1, allowed_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # deploying this smart contract will give 10m total supply * 10^8 zNEOs to OWNER
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # OWNER will give zNEO to aux_contract_address so that it can approve
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, aux_contract_address, allowed_amount, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # this approve will succeed, because aux_contract_address have enough zNEO
        result = self.run_smart_contract(engine, path_aux_contract, 'calling_approve',
                                         wrapped_neo_address, self.OTHER_ACCOUNT_1, allowed_amount,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # approved fired an event
        approval_events = engine.get_events('Approval')
        self.assertEqual(1, len(approval_events))

        owner, spender, amount = approval_events[0].arguments
        if isinstance(owner, str):
            owner = String(owner).to_bytes()
        if isinstance(spender, str):
            spender = String(spender).to_bytes()
        self.assertEqual(aux_contract_address, owner)
        self.assertEqual(self.OTHER_ACCOUNT_1, spender)
        self.assertEqual(allowed_amount, amount)

    def test_wrapped_neo_allowance(self):
        path = self.get_contract_path('wrapped_neo.py')
        path_aux_contract = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')
        engine = TestEngine()
        engine.add_contract(path.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        wrapped_neo_address = hash160(output)
        output, manifest = self.compile_and_save(path_aux_contract)
        aux_contract_address = hash160(output)

        allowed_amount = 10 * 10 ** 8

        # aux_contract_address did not approve OTHER_SCRIPT_HASH
        result = self.run_smart_contract(engine, path, 'allowance', aux_contract_address, self.OTHER_ACCOUNT_1,
                                         signer_accounts=[aux_contract_address],
                                         expected_result_type=bool)
        self.assertEqual(0, result)

        # deploying smart contract
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # OWNER will give zNEO to aux_contract_address so that it can approve
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, aux_contract_address, allowed_amount, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # this approve will succeed, because aux_contract_address have enough zNEO
        result = self.run_smart_contract(engine, path_aux_contract, 'calling_approve',
                                         wrapped_neo_address, self.OTHER_ACCOUNT_1, allowed_amount,
                                         signer_accounts=[aux_contract_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # aux_contract_address allowed OTHER_SCRIPT_HASH to spend transferred_amount of zNEO
        result = self.run_smart_contract(engine, path, 'allowance', aux_contract_address, self.OTHER_ACCOUNT_1,
                                         signer_accounts=[aux_contract_address])
        self.assertEqual(allowed_amount, result)

    def test_wrapped_neo_transfer_from(self):
        path = self.get_contract_path('wrapped_neo.py')
        path_aux_contract = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')
        engine = TestEngine()
        engine.add_contract(path.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        wrapped_neo_address = hash160(output)
        output, manifest = self.compile_and_save(path_aux_contract)
        aux_contract_address = hash160(output)

        allowed_amount = 10 * 10 ** 8

        # deploying smart contract
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

        # OWNER will give zNEO to aux_contract_address so that it can approve another contracts
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OWNER_SCRIPT_HASH, aux_contract_address, 10_000_000 * 10 ** 8, None,
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
        self.assertEqual(aux_contract_address, receiver)
        self.assertEqual(10_000_000 * 100_000_000, amount)

        # this approve will succeed, because aux_contract_address have enough zNEO
        result = self.run_smart_contract(engine, path_aux_contract, 'calling_approve',
                                         wrapped_neo_address, self.OTHER_ACCOUNT_1, allowed_amount,
                                         signer_accounts=[aux_contract_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        transferred_amount = allowed_amount

        # this transfer will fail,
        # because OTHER_SCRIPT_HASH is not allowed to transfer more than aux_contract_address approved
        result = self.run_smart_contract(engine, path, 'transfer_from', self.OTHER_ACCOUNT_1, aux_contract_address,
                                         self.OTHER_ACCOUNT_2, transferred_amount + 1 * 10 ** 8, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)
        transfer_events = engine.get_events('Transfer')
        self.assertEqual(2, len(transfer_events))

        # this transfer will succeed and will fire the Transfer event
        balance_spender_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        balance_sender_before = self.run_smart_contract(engine, path, 'balanceOf', aux_contract_address)
        balance_receiver_before = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_2)
        result = self.run_smart_contract(engine, path, 'transfer_from', self.OTHER_ACCOUNT_1, aux_contract_address,
                                         self.OTHER_ACCOUNT_2, transferred_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
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
        self.assertEqual(aux_contract_address, sender)
        self.assertEqual(self.OTHER_ACCOUNT_2, receiver)
        self.assertEqual(transferred_amount, amount)

        # transferring changed the balance
        balance_spender_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        balance_sender_after = self.run_smart_contract(engine, path, 'balanceOf', aux_contract_address)
        balance_receiver_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_2)
        self.assertEqual(balance_spender_before, balance_spender_after)
        self.assertEqual(balance_sender_before - transferred_amount, balance_sender_after)
        self.assertEqual(balance_receiver_before + transferred_amount, balance_receiver_after)

        # aux_contract_address and OTHER_SCRIPT_HASH allowance was reduced to 0
        result = self.run_smart_contract(engine, path, 'allowance', aux_contract_address, self.OTHER_ACCOUNT_1,
                                         signer_accounts=[aux_contract_address],
                                         expected_result_type=bool)
        self.assertEqual(0, result)

        # this approve will succeed, because aux_contract_address have enough zNEO
        result = self.run_smart_contract(engine, path_aux_contract, 'calling_approve',
                                         wrapped_neo_address, self.OTHER_ACCOUNT_1, allowed_amount,
                                         signer_accounts=[aux_contract_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        transferred_amount = allowed_amount - 4 * 10 ** 8

        result = self.run_smart_contract(engine, path, 'transfer_from', self.OTHER_ACCOUNT_1, aux_contract_address,
                                         self.OTHER_ACCOUNT_2, transferred_amount, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # aux_contract_address and OTHER_SCRIPT_HASH allowance was reduced to allowed_amount - transferred_amount
        result = self.run_smart_contract(engine, path, 'allowance', aux_contract_address, self.OTHER_ACCOUNT_1,
                                         signer_accounts=[aux_contract_address],
                                         expected_result_type=bool)
        self.assertEqual(allowed_amount - transferred_amount, result)

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer_from',
                                    self.OWNER_SCRIPT_HASH, bytes(10), self.OTHER_ACCOUNT_1, allowed_amount, None)
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer_from',
                                    bytes(10), self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, allowed_amount, None)
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer_from',
                                    self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, bytes(10), allowed_amount, None)

        # should fail when the amount is less than 0
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer_from',
                                    self.OTHER_ACCOUNT_1, self.OWNER_SCRIPT_HASH, self.OTHER_ACCOUNT_2, -10, None)

    def test_wrapped_neo_onNEP17Payment(self):
        path = self.get_contract_path('wrapped_neo.py')
        engine = TestEngine()
        engine.add_contract(path.replace('.py', '.nef'))

        aux_path = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')

        output, manifest = self.compile_and_save(path)
        wrapped_neo_address = hash160(output)

        output, manifest = self.compile_and_save(aux_path)
        aux_address = hash160(output)

        minted_amount = 10 * 10 ** 8
        # deploying wrapped_neo smart contract
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

        engine.add_neo(aux_address, minted_amount)

        # the smart contract will abort if some address other than NEO calls the onPayment method
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'onNEP17Payment', aux_address, minted_amount, None,
                                    signer_accounts=[aux_address])

        neo_wrapped_before = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_aux_before = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', aux_address)
        zneo_aux_before = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        # transferring NEO to the wrapped_neo_address will mint them
        result = self.run_smart_contract(engine, aux_path, 'calling_transfer', NEO_SCRIPT,
                                         aux_address, wrapped_neo_address, minted_amount, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        transfer_events = engine.get_events('Transfer')
        self.assertEqual(3, len(transfer_events))
        self.assertEqual(3, len(transfer_events[1].arguments))

        sender, receiver, amount = transfer_events[1].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(aux_address, sender)
        self.assertEqual(wrapped_neo_address, receiver)
        self.assertEqual(minted_amount, amount)

        self.assertEqual(3, len(transfer_events[2].arguments))

        sender, receiver, amount = transfer_events[2].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(aux_address, receiver)
        self.assertEqual(minted_amount, amount)

        # balance after burning
        neo_wrapped_after = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', wrapped_neo_address)
        neo_aux_after = self.run_smart_contract(engine, NEO_SCRIPT, 'balanceOf', aux_address)
        zneo_aux_after = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        self.assertEqual(neo_wrapped_before + minted_amount, neo_wrapped_after)
        self.assertEqual(neo_aux_before - minted_amount, neo_aux_after)
        self.assertEqual(zneo_aux_before + minted_amount, zneo_aux_after)
