from neo3.contracts.contract import CONTRACT_HASHES
from neo3.wallet import account

from boa3.internal import constants
from boa3_test.tests import boatestcase


class TestICOTemplate(boatestcase.BoaTestCase):
    default_folder: str = 'examples'
    ASSERT_RESULTED_FALSE_MSG = 'ASSERT is executed with false result.'

    owner: account.Account
    account_for_balance_test: account.Account
    account_for_verify_test: account.Account
    account_not_admin_for_allowance: account.Account
    account_not_admin_for_register: account.Account
    account_not_admin_for_remove: account.Account
    account_originator_for_approve_test: account.Account
    account_receiver_for_approve_test: account.Account
    account_for_refund_test: account.Account
    account_originator_for_transfer_test: account.Account
    account_sender_for_transfer_test: account.Account
    account_receiver_for_transfer_test: account.Account

    BALANCE_TO_TEST = 1000
    NEO_TO_REFUND = 1
    GAS_TO_REFUND = 100
    AMOUNT_TO_APPROVE = 100 * 10 ** 8
    AMOUNT_TO_TRANSFER = 100 * 10 ** 8
    TOTAL_SUPPLY = 10_000_000 * 10 ** 8

    KYC_WHITELIST_PREFIX = b'KYCWhitelistApproved'

    @classmethod
    def setupTestCase(cls):
        cls.owner = cls.node.wallet.account_new(label='owner')
        cls.account_for_balance_test = cls.node.wallet.account_new(label='accountBalanceOf')
        cls.account_for_verify_test = cls.node.wallet.account_new(label='accountVerify')
        cls.account_not_admin_for_allowance = cls.node.wallet.account_new(label='accountNotAdminAllowance')
        cls.account_not_admin_for_register = cls.node.wallet.account_new(label='accountNotAdminRegister')
        cls.account_not_admin_for_remove = cls.node.wallet.account_new(label='accountNotAdminRemove')
        cls.account_originator_for_approve_test = cls.node.wallet.account_new(label='accountOriginatorApprove')
        cls.account_receiver_for_approve_test = cls.node.wallet.account_new(label='accountReceiverApprove')
        cls.account_for_refund_test = cls.node.wallet.account_new(label='accountRefund')
        cls.account_originator_for_transfer_test = cls.node.wallet.account_new(label='accountOriginatorTransfer')
        cls.account_sender_for_transfer_test = cls.node.wallet.account_new(label='accountSenderTransfer')
        cls.account_receiver_for_transfer_test = cls.node.wallet.account_new(label='accountReceiverTransfer')

        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.owner.script_hash, 100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account_for_balance_test.script_hash,
                           100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account_for_verify_test.script_hash,
                           100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash,
                           cls.account_not_admin_for_allowance.script_hash, 100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash,
                           cls.account_not_admin_for_register.script_hash, 100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash,
                           cls.account_not_admin_for_remove.script_hash, 100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash,
                           cls.account_originator_for_approve_test.script_hash, 100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash,
                           cls.account_receiver_for_approve_test.script_hash, 100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account_for_refund_test.script_hash,
                           100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash,
                           cls.account_sender_for_transfer_test.script_hash, 100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash,
                           cls.account_receiver_for_transfer_test.script_hash, 100, 8)

        await cls.set_up_contract('ico.py', signing_account=cls.owner)

        await cls.transfer(CONTRACT_HASHES.NEO_TOKEN, cls.genesis.script_hash, cls.contract_hash, 2 * cls.NEO_TO_REFUND,
                           0)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.contract_hash, 2 * cls.GAS_TO_REFUND,
                           8)

        await cls.transfer(
            cls.contract_hash,
            cls.owner.script_hash,
            cls.account_for_balance_test.script_hash,
            cls.BALANCE_TO_TEST, 8,
            signing_account=cls.owner
        )

        await cls.transfer(
            cls.contract_hash,
            cls.owner.script_hash,
            cls.account_originator_for_approve_test.script_hash,
            cls.BALANCE_TO_TEST, 8,
            signing_account=cls.owner
        )

    def test_ico_compile(self):
        self.assertCompile('ico.py')

    async def test_ico_symbol(self):
        result, _ = await self.call('symbol', [], return_type=str)
        self.assertEqual('ICO', result)

    async def test_ico_decimals(self):
        result, _ = await self.call('decimals', [], return_type=int)
        self.assertEqual(8, result)

    async def test_ico_balance_of(self):
        result, _ = await self.call('balanceOf', [self.account_for_balance_test.script_hash], return_type=int)
        self.assertEqual(self.BALANCE_TO_TEST * 10 ** 8, result)

    async def test_ico_balance_of_bad_account(self):
        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('balanceOf', [bytes(10)], return_type=int)
        self.assertRegex(str(context.exception), 'invalid account length')

        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('balanceOf', [bytes(30)], return_type=int)
        self.assertRegex(str(context.exception), 'invalid account length')

    # This test is numbered because numbered tests *must* be run in order
    # and the default order is alphanumerical
    async def test_00_ico_total_supply(self):
        result, _ = await self.call('totalSupply', [], return_type=int)
        self.assertEqual(self.TOTAL_SUPPLY, result)

    async def test_ico_verify(self):
        result, _ = await self.call('verify', [], return_type=bool, signing_accounts=[self.account_for_verify_test])
        self.assertEqual(False, result)

        result, _ = await self.call('verify', [], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, result)

    async def test_ico_kyc_register(self):
        # don't include if not signed by the administrator
        result, _ = await self.call('kyc_register', [[self.owner.script_hash, self.account_not_admin_for_register.script_hash]], return_type=int, signing_accounts=[self.account_not_admin_for_register])
        self.assertEqual(0, result)

        # don't include script hashes with size different from 20
        result, _ = await self.call('kyc_register', [[bytes(40), self.owner.script_hash, bytes(12)]], return_type=int, signing_accounts=[self.owner])
        self.assertEqual(1, result)

        # script hashes already registered are returned as well
        result, _ = await self.call('kyc_register', [[self.owner.script_hash, self.account_not_admin_for_register.script_hash]], return_type=int, signing_accounts=[self.owner])
        self.assertEqual(2, result)

        contract_storage = await self.get_storage()
        self.assertIn(self.KYC_WHITELIST_PREFIX + self.owner.script_hash.to_array(), contract_storage)
        self.assertIsNotNone(contract_storage[self.KYC_WHITELIST_PREFIX + self.owner.script_hash.to_array()])

        self.assertIn(self.KYC_WHITELIST_PREFIX + self.account_not_admin_for_register.script_hash.to_array(), contract_storage)
        self.assertIsNotNone(contract_storage[self.KYC_WHITELIST_PREFIX + self.account_not_admin_for_register.script_hash.to_array()])

    async def test_ico_kyc_remove(self):
        # don't remove if not signed by the administrator
        result, _ = await self.call('kyc_remove', [[self.owner.script_hash, bytes(22)]], return_type=int, signing_accounts=[self.account_not_admin_for_remove])
        self.assertEqual(0, result)

        # script hashes that weren't registered are returned as well
        contract_storage = await self.get_storage()
        self.assertNotIn(self.KYC_WHITELIST_PREFIX + self.account_not_admin_for_remove.script_hash.to_array(), contract_storage)

        result, _ = await self.call('kyc_remove', [[self.account_not_admin_for_remove.script_hash]], return_type=int, signing_accounts=[self.owner])
        self.assertEqual(1, result)

        # don't remove script hashes with size different from 20
        result, _ = await self.call('kyc_remove', [[bytes(40), self.owner.script_hash, bytes(12)]], return_type=int, signing_accounts=[self.owner])
        self.assertEqual(1, result)

        contract_storage = await self.get_storage()
        self.assertNotIn(self.KYC_WHITELIST_PREFIX + self.account_not_admin_for_remove.script_hash.to_array(), contract_storage)

    async def test_ico_approve(self):
        # should fail if the origin doesn't sign
        result, _ = await self.call('approve', [self.account_originator_for_approve_test.script_hash, self.account_receiver_for_approve_test.script_hash, self.AMOUNT_TO_APPROVE], return_type=bool)
        self.assertEqual(False, result)

        # should fail if origin and target are the same
        result, _ = await self.call('approve', [self.account_originator_for_approve_test.script_hash, self.account_originator_for_approve_test.script_hash, self.AMOUNT_TO_APPROVE], return_type=bool, signing_accounts=[self.account_originator_for_approve_test])
        self.assertEqual(False, result)

        # should fail if any of the addresses is not included in the kyc
        result, _ = await self.call('approve', [self.account_originator_for_approve_test.script_hash, self.account_receiver_for_approve_test.script_hash, self.AMOUNT_TO_APPROVE], return_type=bool, signing_accounts=[self.account_originator_for_approve_test])
        self.assertEqual(False, result)

        result, _ = await self.call('kyc_register', [[self.account_originator_for_approve_test.script_hash, self.account_receiver_for_approve_test.script_hash]], return_type=int, signing_accounts=[self.owner])
        self.assertEqual(2, result)

        result, _ = await self.call('approve', [self.account_originator_for_approve_test.script_hash, self.account_receiver_for_approve_test.script_hash, self.AMOUNT_TO_APPROVE], return_type=bool, signing_accounts=[self.account_originator_for_approve_test])
        self.assertEqual(True, result)

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('approve', [self.account_originator_for_approve_test.script_hash, bytes(10), self.AMOUNT_TO_APPROVE], return_type=bool, signing_accounts=[self.account_originator_for_approve_test])
        self.assertRegex(str(context.exception), 'invalid account length')

        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('approve', [bytes(10), self.account_receiver_for_approve_test.script_hash, self.AMOUNT_TO_APPROVE], return_type=bool, signing_accounts=[self.account_originator_for_approve_test])
        self.assertRegex(str(context.exception), 'invalid account length')

        # should fail when the amount is less than 0
        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('approve', [self.account_originator_for_approve_test.script_hash, self.account_receiver_for_approve_test.script_hash, -10], return_type=bool, signing_accounts=[self.account_originator_for_approve_test])
        self.assertRegex(str(context.exception), 'invalid amount')

    async def test_ico_allowance(self):
        result, _ = await self.call('allowance', [self.owner.script_hash, self.account_not_admin_for_allowance.script_hash], return_type=int, signing_accounts=[self.owner])
        self.assertEqual(0, result)

        result, _ = await self.call('kyc_register', [[self.owner.script_hash, self.account_not_admin_for_allowance.script_hash]], return_type=int, signing_accounts=[self.owner])
        self.assertEqual(2, result)

        result, _ = await self.call('approve', [self.owner.script_hash, self.account_not_admin_for_allowance.script_hash, self.AMOUNT_TO_APPROVE], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, result)

        result, _ = await self.call('allowance', [self.owner.script_hash, self.account_not_admin_for_allowance.script_hash], return_type=int)
        self.assertEqual(self.AMOUNT_TO_APPROVE, result)

    async def test_ico_transfer_from(self):
        # should fail when any of the scripts' length is not 20
        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('transferFrom', [self.owner.script_hash, bytes(10), self.account_receiver_for_transfer_test.script_hash, self.AMOUNT_TO_TRANSFER, None], return_type=bool)
        self.assertRegex(str(context.exception), 'invalid account length')

        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('transferFrom', [bytes(10), self.account_sender_for_transfer_test.script_hash, self.account_receiver_for_transfer_test.script_hash, self.AMOUNT_TO_TRANSFER, None], return_type=bool)
        self.assertRegex(str(context.exception), 'invalid account length')

        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('transferFrom', [self.owner.script_hash, self.account_sender_for_transfer_test.script_hash, bytes(30), self.AMOUNT_TO_TRANSFER, None], return_type=bool)
        self.assertRegex(str(context.exception), 'invalid account length')

        # should fail when the amount is less than 0
        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('transferFrom', [self.owner.script_hash, self.account_sender_for_transfer_test.script_hash, self.account_receiver_for_transfer_test.script_hash, -10, None], return_type=bool)
        self.assertRegex(str(context.exception), 'invalid amount')

        # should fail if the sender doesn't sign
        result, _ = await self.call('transferFrom', [self.owner.script_hash, self.account_sender_for_transfer_test.script_hash, self.account_receiver_for_transfer_test.script_hash, self.AMOUNT_TO_TRANSFER, None], return_type=bool)
        self.assertEqual(False, result)

        # should fail if the allowed amount is less than the given amount
        result, _ = await self.call('transferFrom', [self.owner.script_hash, self.account_sender_for_transfer_test.script_hash, self.account_receiver_for_transfer_test.script_hash, self.AMOUNT_TO_TRANSFER, None], return_type=bool, signing_accounts=[self.account_sender_for_transfer_test])
        self.assertEqual(False, result)

        result, _ = await self.call('kyc_register', [[self.owner.script_hash, self.account_sender_for_transfer_test.script_hash]], return_type=int, signing_accounts=[self.owner])
        self.assertEqual(2, result)

        result, _ = await self.call('approve', [self.owner.script_hash, self.account_sender_for_transfer_test.script_hash, self.AMOUNT_TO_TRANSFER * 2], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, result)

        balance_before_1, _ = await self.call('balanceOf', [self.owner.script_hash], return_type=int)
        result, notifications = await self.call('transferFrom', [self.owner.script_hash, self.account_sender_for_transfer_test.script_hash, self.owner.script_hash, self.AMOUNT_TO_TRANSFER, None], return_type=bool, signing_accounts=[self.account_sender_for_transfer_test])
        self.assertEqual(True, result)

        # transfer event when the address that has the tokens is the same as the one receiving
        transfer_events = self.filter_events(notifications, notification_type=boatestcase.Nep17TransferEvent)
        self.assertEqual(1, len(transfer_events))
        event = transfer_events[0]
        self.assertEqual(self.account_sender_for_transfer_test.script_hash, event.source)
        self.assertEqual(self.owner.script_hash, event.destination)
        self.assertEqual(self.AMOUNT_TO_TRANSFER, event.amount)

        balance_after_1, _ = await self.call('balanceOf', [self.owner.script_hash], return_type=int)

        balance_before_2 = await self.call('balanceOf', [self.owner.script_hash], return_type=int)
        result, notifications = await self.call('transferFrom', [self.owner.script_hash, self.account_sender_for_transfer_test.script_hash, self.account_sender_for_transfer_test.script_hash, self.AMOUNT_TO_TRANSFER, None], return_type=bool, signing_accounts=[self.account_sender_for_transfer_test])
        self.assertEqual(True, result)

        # transfer event when the address that is receiving is the same that is calling the transfer
        transfer_events = self.filter_events(notifications, notification_type=boatestcase.Nep17TransferEvent)
        self.assertEqual(1, len(transfer_events))
        event = transfer_events[0]
        self.assertEqual(self.account_sender_for_transfer_test.script_hash, event.source)
        self.assertEqual(self.account_sender_for_transfer_test.script_hash, event.destination)
        self.assertEqual(self.AMOUNT_TO_TRANSFER, event.amount)

        balance_after_2 = await self.call('balanceOf', [self.owner.script_hash], return_type=int)

        result, notifications = await self.call('transferFrom', [self.owner.script_hash, self.account_sender_for_transfer_test.script_hash, self.account_receiver_for_transfer_test.script_hash, 0, None], return_type=bool, signing_accounts=[self.account_sender_for_transfer_test])
        self.assertEqual(True, result)

        # transfer event when the amount transferred is zero
        transfer_events = self.filter_events(notifications, notification_type=boatestcase.Nep17TransferEvent)
        self.assertEqual(1, len(transfer_events))
        event = transfer_events[0]
        self.assertEqual(self.account_sender_for_transfer_test.script_hash, event.source)
        self.assertEqual(self.account_receiver_for_transfer_test.script_hash, event.destination)
        self.assertEqual(0, event.amount)

        balance_originator_before = await self.call('balanceOf', [self.owner.script_hash], return_type=int)
        balance_sender_before = await self.call('balanceOf', [self.account_sender_for_transfer_test.script_hash], return_type=int)
        balance_receiver_before = await self.call('balanceOf', [self.account_receiver_for_transfer_test.script_hash], return_type=int)

        result, _ = await self.call('transferFrom', [self.owner.script_hash, self.account_sender_for_transfer_test.script_hash, self.account_receiver_for_transfer_test.script_hash, self.AMOUNT_TO_TRANSFER, None], return_type=bool, signing_accounts=[self.account_sender_for_transfer_test])
        self.assertEqual(False, result)

        balance_originator_after = await self.call('balanceOf', [self.owner.script_hash], return_type=int)
        balance_sender_after = await self.call('balanceOf', [self.account_sender_for_transfer_test.script_hash], return_type=int)
        balance_receiver_after = await self.call('balanceOf', [self.account_receiver_for_transfer_test.script_hash], return_type=int)

        self.assertEqual(balance_after_1, balance_before_1)
        self.assertEqual(balance_after_2, balance_before_2)
        self.assertEqual(balance_originator_before, balance_originator_after)
        self.assertEqual(balance_sender_before, balance_sender_after)
        self.assertEqual(balance_receiver_before, balance_receiver_after)

    # This test is numbered because numbered tests *must* be run in order
    # and the default order is alphanumerical
    async def test_01_ico_mint(self):
        minted_amount = 10_000 * 10 ** 8

        # should fail if amount is a negative number
        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('mint', [-10], return_type=bool)
        self.assertRegex(str(context.exception), 'invalid amount')

        # should fail if not signed by the administrator
        result, _ = await self.call('mint', [minted_amount], return_type=bool)
        self.assertEqual(False, result)

        total_supply_before, _ = await self.call('totalSupply', [], return_type=int)
        owner_balance_before, _ = await self.call('balanceOf', [self.owner.script_hash], return_type=int)

        result, _ = await self.call('mint', [minted_amount], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, result)

        total_supply_after, _ = await self.call('totalSupply', [], return_type=int)
        owner_balance_after, _ = await self.call('balanceOf', [self.owner.script_hash], return_type=int)

        self.assertEqual(total_supply_before + minted_amount, total_supply_after)
        self.assertEqual(owner_balance_before + minted_amount, owner_balance_after)

    async def test_ico_refund(self):
        # should fail script hash length is not 20
        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('refund', [bytes(10), self.NEO_TO_REFUND, self.GAS_TO_REFUND], return_type=bool)
        self.assertRegex(str(context.exception), 'invalid account length')

        # should fail no amount is a positive number
        with self.assertRaises(boatestcase.AssertException) as context:
            result, _ = await self.call('refund', [self.account_for_refund_test.script_hash, 0, 0], return_type=bool)
        self.assertRegex(str(context.exception), 'invalid amount')

        # should fail if not signed by the owner
        result, _ = await self.call('refund', [self.account_for_refund_test.script_hash, self.NEO_TO_REFUND, self.GAS_TO_REFUND], return_type=bool)
        self.assertEqual(False, result)

        # should fail if given address is not included in the kyc
        result, _ = await self.call('refund', [self.account_for_refund_test.script_hash, self.NEO_TO_REFUND, self.GAS_TO_REFUND], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(False, result)

        result, _ = await self.call('kyc_register', [[self.account_for_refund_test.script_hash]], return_type=int, signing_accounts=[self.owner])
        self.assertEqual(1, result)

        balance_neo_before, _ = await self.call('balanceOf', [self.account_for_refund_test.script_hash], return_type=int, target_contract=constants.NEO_SCRIPT)
        balance_gas_before, _ = await self.call('balanceOf', [self.account_for_refund_test.script_hash], return_type=int, target_contract=constants.GAS_SCRIPT)

        result, _ = await self.call('refund', [self.account_for_refund_test.script_hash, self.NEO_TO_REFUND, self.GAS_TO_REFUND], return_type=bool, signing_accounts=[self.owner])

        balance_neo_after, _ = await self.call('balanceOf', [self.account_for_refund_test.script_hash], return_type=int, target_contract=constants.NEO_SCRIPT)
        balance_gas_after, _ = await self.call('balanceOf', [self.account_for_refund_test.script_hash], return_type=int, target_contract=constants.GAS_SCRIPT)

        self.assertEqual(balance_neo_before + self.NEO_TO_REFUND, balance_neo_after)
        self.assertEqual(balance_gas_before + self.GAS_TO_REFUND, balance_gas_after)
