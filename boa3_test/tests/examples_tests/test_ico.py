from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestICOTemplate(BoaTest):
    default_folder: str = 'examples'

    OWNER = neoxp.utils.get_account_by_name('owner')
    OTHER_ACCOUNT_1 = neoxp.utils.get_account_by_name('testAccount1')
    OTHER_ACCOUNT_2 = neoxp.utils.get_account_by_name('testAccount2')
    GAS_TO_DEPLOY = int(10.5 * 10 ** 8)

    KYC_WHITELIST_PREFIX = b'KYCWhitelistApproved'

    def test_ico_compile(self):
        path = self.get_contract_path('ico.py')
        self.compile(path)

    def test_ico_symbol(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invoke = runner.call_contract(path, 'symbol')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual('ICO', invoke.result)

    def test_ico_decimals(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invoke = runner.call_contract(path, 'decimals')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(8, invoke.result)

    def test_ico_total_balance_of(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        total_supply = 10_000_000 * 10 ** 8
        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invoke = runner.call_contract(path, 'balanceOf', self.OWNER.script_hash.to_array())
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(total_supply, invoke.result)

        # should fail when the script length is not 20
        runner.call_contract(path, 'balanceOf', bytes(10))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'balanceOf', bytes(30))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_ico_total_supply(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        total_supply = 10_000_000 * 10 ** 8
        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invoke = runner.call_contract(path, 'totalSupply')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(total_supply, invoke.result)

    def test_ico_verify(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invokes.append(runner.call_contract(path, 'verify'))
        expected_results.append(False)

        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'verify'))
        expected_results.append(True)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_ico_kyc_register(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        contract = runner.deploy_contract(path, account=self.OWNER)
        owner_script_hash = self.OWNER.script_hash.to_array()
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        # don't include if not signed by the administrator
        invokes.append(runner.call_contract(path, 'kyc_register',
                                            [owner_script_hash, bytes(22)]))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # don't include script hashes with size different from 20
        invokes.append(runner.call_contract(path, 'kyc_register',
                                            [bytes(40), owner_script_hash, bytes(12)]))
        expected_results.append(1)

        # script hashes already registered are returned as well
        invokes.append(runner.call_contract(path, 'kyc_register',
                                            [owner_script_hash, other_account_script_hash]))
        expected_results.append(2)

        runner.execute(account=self.OWNER, get_storage_from=contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        storage_value = runner.storages.get(contract, self.KYC_WHITELIST_PREFIX + owner_script_hash)
        self.assertIsNotNone(storage_value)

        storage_value = runner.storages.get(contract, self.KYC_WHITELIST_PREFIX + other_account_script_hash)
        self.assertIsNotNone(storage_value)

    def test_ico_kyc_remove(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        contract = runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)

        owner_script_hash = self.OWNER.script_hash.to_array()
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        # don't remove if not signed by the administrator
        invokes.append(runner.call_contract(path, 'kyc_remove',
                                            [owner_script_hash, bytes(22)]))
        expected_results.append(0)

        runner.execute(get_storage_from=contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # script hashes that weren't registered are returned as well
        self.assertIsNone(runner.storages.get(contract, self.KYC_WHITELIST_PREFIX + other_account_script_hash))

        invokes.append(runner.call_contract(path, 'kyc_remove',
                                            [other_account_script_hash]))
        expected_results.append(1)

        # don't remove script hashes with size different from 20
        invokes.append(runner.call_contract(path, 'kyc_remove',
                                            [bytes(40), owner_script_hash, bytes(12)]))
        expected_results.append(1)

        runner.execute(account=self.OWNER, get_storage_from=contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        self.assertIsNone(runner.storages.get(contract, self.KYC_WHITELIST_PREFIX + other_account_script_hash))

    def test_ico_approve(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        owner_script_hash = self.OWNER.script_hash.to_array()
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()
        approved_amount = 100 * 10 ** 8

        # should fail if the origin doesn't sign
        invokes.append(runner.call_contract(path, 'approve',
                                            owner_script_hash, other_account_script_hash, approved_amount))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # should fail if origin and target are the same
        invokes.append(runner.call_contract(path, 'approve',
                                            owner_script_hash, owner_script_hash, approved_amount))
        expected_results.append(False)

        # should fail if any of the addresses is not included in the kyc
        invokes.append(runner.call_contract(path, 'approve',
                                            owner_script_hash, other_account_script_hash, approved_amount))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'kyc_register',
                                            [owner_script_hash, other_account_script_hash]))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'approve',
                                            owner_script_hash, other_account_script_hash, approved_amount))
        expected_results.append(True)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # should fail when any of the scripts' length is not 20
        runner.call_contract(path, 'approve',
                             owner_script_hash, bytes(10), approved_amount)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'approve',
                             bytes(10), other_account_script_hash, approved_amount)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'approve',
                             other_account_script_hash, owner_script_hash, -10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_ico_allowance(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)
        owner_script_hash = self.OWNER.script_hash.to_array()
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()
        approved_amount = 100 * 10 ** 8

        invokes.append(runner.call_contract(path, 'allowance', owner_script_hash, other_account_script_hash))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'kyc_register',
                                            [owner_script_hash, other_account_script_hash]))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'approve',
                                            owner_script_hash, other_account_script_hash, approved_amount))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'allowance', owner_script_hash, other_account_script_hash))
        expected_results.append(approved_amount)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_ico_transfer_from(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        owner_script_hash = self.OWNER.script_hash.to_array()
        other_account_1_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()
        other_account_2_script_hash = self.OTHER_ACCOUNT_2.script_hash.to_array()
        transferred_amount = 100 * 10 ** 8

        # should fail if the sender doesn't sign
        invokes.append(runner.call_contract(path, 'transferFrom',
                                            owner_script_hash, other_account_1_script_hash, other_account_2_script_hash,
                                            transferred_amount, None))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # should fail if the allowed amount is less than the given amount
        invokes.append(runner.call_contract(path, 'transferFrom',
                                            owner_script_hash, other_account_1_script_hash, other_account_2_script_hash,
                                            transferred_amount, None))
        expected_results.append(False)

        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'kyc_register',
                                            [owner_script_hash, other_account_1_script_hash]))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'approve',
                                            owner_script_hash, other_account_1_script_hash, transferred_amount * 2))
        expected_results.append(True)

        runner.execute(account=self.OWNER, add_invokes_to_batch=True)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        balance_before_1 = runner.call_contract(path, 'balanceOf', owner_script_hash)
        invokes.append(runner.call_contract(path, 'transferFrom',
                                            owner_script_hash, other_account_1_script_hash, owner_script_hash,
                                            transferred_amount, None))
        expected_results.append(True)
        balance_after_1 = runner.call_contract(path, 'balanceOf', owner_script_hash)

        balance_before_2 = runner.call_contract(path, 'balanceOf', owner_script_hash)
        invokes.append(runner.call_contract(path, 'transferFrom',
                                            owner_script_hash, other_account_1_script_hash, other_account_1_script_hash,
                                            transferred_amount, None))
        expected_results.append(True)
        balance_after_2 = runner.call_contract(path, 'balanceOf', owner_script_hash)

        invokes.append(runner.call_contract(path, 'transferFrom',
                                            owner_script_hash, other_account_1_script_hash, other_account_2_script_hash,
                                            0, None))
        expected_results.append(True)

        balance_originator_before = runner.call_contract(path, 'balanceOf', owner_script_hash)
        balance_sender_before = runner.call_contract(path, 'balanceOf', other_account_1_script_hash)
        balance_receiver_before = runner.call_contract(path, 'balanceOf', other_account_2_script_hash)

        invokes.append(runner.call_contract(path, 'transferFrom',
                                            owner_script_hash, other_account_1_script_hash, other_account_2_script_hash,
                                            transferred_amount, None))
        expected_results.append(False)

        balance_originator_after = runner.call_contract(path, 'balanceOf', owner_script_hash)
        balance_sender_after = runner.call_contract(path, 'balanceOf', other_account_1_script_hash)
        balance_receiver_after = runner.call_contract(path, 'balanceOf', other_account_2_script_hash)

        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        transfer_events = runner.get_events('Transfer')
        self.assertEqual(3, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))
        self.assertEqual(3, len(transfer_events[1].arguments))
        self.assertEqual(3, len(transfer_events[2].arguments))

        # transfer event when the address that has the tokens is the same as the one receiving
        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(other_account_1_script_hash, sender)
        self.assertEqual(owner_script_hash, receiver)
        self.assertEqual(transferred_amount, amount)

        # transfer event when the address that is receiving is the same that is calling the transfer
        sender, receiver, amount = transfer_events[1].arguments
        self.assertEqual(other_account_1_script_hash, sender)
        self.assertEqual(other_account_1_script_hash, receiver)
        self.assertEqual(transferred_amount, amount)

        # transfer event when the amount transferred is zero
        sender, receiver, amount = transfer_events[2].arguments
        self.assertEqual(other_account_1_script_hash, sender)
        self.assertEqual(other_account_2_script_hash, receiver)
        self.assertEqual(0, amount)

        self.assertEqual(balance_after_1.result, balance_before_1.result)
        self.assertEqual(balance_after_2.result, balance_before_2.result)
        self.assertEqual(balance_originator_before.result, balance_originator_after.result)
        self.assertEqual(balance_sender_before.result, balance_sender_after.result)
        self.assertEqual(balance_receiver_before.result, balance_receiver_after.result)

        # should fail when any of the scripts' length is not 20
        runner.call_contract(path, 'transferFrom',
                             owner_script_hash, bytes(10), other_account_1_script_hash, transferred_amount, None)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'transferFrom',
                             bytes(10), other_account_1_script_hash, other_account_2_script_hash, transferred_amount, None)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'transferFrom',
                             owner_script_hash, other_account_1_script_hash, bytes(30), transferred_amount, None)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # should fail when the amount is less than 0
        runner.call_contract(path, 'transferFrom',
                             owner_script_hash, other_account_1_script_hash, other_account_2_script_hash, -10, None)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_ico_mint(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        owner_script_hash = self.OWNER.script_hash.to_array()
        minted_amount = 10_000 * 10 ** 8

        # should fail if amount is a negative number
        runner.call_contract(path, 'mint', -10)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # should fail if not signed by the administrator
        invokes.append(runner.call_contract(path, 'mint', minted_amount))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        total_supply_before = runner.call_contract(path, 'totalSupply')
        owner_balance_before = runner.call_contract(path, 'balanceOf', owner_script_hash)

        invokes.append(runner.call_contract(path, 'mint', minted_amount))
        expected_results.append(True)

        total_supply_after = runner.call_contract(path, 'totalSupply')
        owner_balance_after = runner.call_contract(path, 'balanceOf', owner_script_hash)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        self.assertEqual(total_supply_before.result + minted_amount, total_supply_after.result)
        self.assertEqual(owner_balance_before.result + minted_amount, owner_balance_after.result)

    def test_ico_refund(self):
        path, _ = self.get_deploy_file_paths('ico.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        contract = runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)

        transferred_neo_amount = 1
        transferred_gas_amount = 10_000

        owner_script_hash = self.OWNER.script_hash.to_array()
        contract_script_hash = contract.script_hash

        runner.add_neo(contract_script_hash, transferred_neo_amount * 2)
        runner.add_gas(contract_script_hash, transferred_gas_amount * 2)

        # should fail if not signed by the owner
        invokes.append(runner.call_contract(path, 'refund',
                                            owner_script_hash, transferred_neo_amount, transferred_gas_amount))
        expected_results.append(False)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # should fail if given address is not included in the kyc
        invokes.append(runner.call_contract(path, 'refund',
                                            owner_script_hash, transferred_neo_amount, transferred_gas_amount))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'kyc_register', [owner_script_hash]))
        expected_results.append(1)

        balance_neo_before = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', owner_script_hash)
        balance_gas_before = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', owner_script_hash)

        invokes.append(runner.call_contract(path, 'refund',
                                            owner_script_hash, transferred_neo_amount, transferred_gas_amount))
        expected_results.append(True)

        balance_neo_after = runner.call_contract(constants.NEO_SCRIPT, 'balanceOf', owner_script_hash)
        balance_gas_after = runner.call_contract(constants.GAS_SCRIPT, 'balanceOf', owner_script_hash)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        self.assertEqual(balance_neo_before.result + transferred_neo_amount, balance_neo_after.result)
        self.assertEqual(balance_gas_before.result + transferred_gas_amount, balance_gas_after.result)

        # should fail script hash length is not 20
        runner.call_contract(path, 'refund', bytes(10), transferred_neo_amount, transferred_gas_amount)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # should fail no amount is a positive number
        runner.call_contract(path, 'refund', owner_script_hash, 0, 0)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)
