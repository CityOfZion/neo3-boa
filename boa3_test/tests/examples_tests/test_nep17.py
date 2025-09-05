from neo3.contracts.contract import CONTRACT_HASHES
from neo3.wallet import account

from boa3_test.tests import boatestcase


class TestNEP17Template(boatestcase.BoaTestCase):
    default_folder: str = 'examples'

    DECIMALS = 8
    TOTAL_SUPPLY = 10_000_000 * 10 ** DECIMALS
    OWNER_BALANCE = TOTAL_SUPPLY

    owner: account.Account
    account1: account.Account
    account2: account.Account

    @classmethod
    def setupTestCase(cls):
        cls.owner = cls.node.wallet.account_new(label='owner')
        cls.account1 = cls.node.wallet.account_new(label='test1')
        cls.account2 = cls.node.wallet.account_new(label='test2')

        cls.OWNER_BALANCE = cls.TOTAL_SUPPLY
        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.owner.script_hash, 100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 100, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account2.script_hash, 100, 8)

        await cls.set_up_contract('nep17.py', signing_account=cls.owner)
        mint_amount = 100
        await cls.transfer(
            cls.contract_hash,
            cls.owner.script_hash,
            cls.account1.script_hash,
            mint_amount, cls.DECIMALS,
            signing_account=cls.owner
        )
        cls.OWNER_BALANCE -= mint_amount * 10 ** cls.DECIMALS

    def test_compile(self):
        path = self.get_contract_path('nep17.py')
        _, manifest = self.assertCompile(path, get_manifest=True)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-17', manifest['supportedstandards'])

    async def test_symbol(self):
        expected = 'NEP17'
        result, _ = await self.call('symbol', return_type=str)
        self.assertEqual(expected, result)

    async def test_decimals(self):
        expected = self.DECIMALS
        result, _ = await self.call('decimals', return_type=int)
        self.assertEqual(expected, result)

    async def test_before_mint_total_supply(self):
        total_supply = self.TOTAL_SUPPLY
        result, _ = await self.call('totalSupply', return_type=int)
        self.assertEqual(total_supply, result)

    async def test_balance_of(self):
        expected = self.OWNER_BALANCE
        owner_account = self.owner.script_hash
        result, _ = await self.call('balanceOf', [owner_account], return_type=int)
        self.assertEqual(expected, result)

        bad_account = bytes(10)
        with self.assertRaises(boatestcase.AssertException):
            await self.call("balanceOf", [bad_account], return_type=int)

        bad_account = bytes(30)
        with self.assertRaises(boatestcase.AssertException):
            await self.call("balanceOf", [bad_account], return_type=int)

    async def test_transfer_success(self):
        from_account = self.account1
        to_account = self.account2

        from_script_hash = from_account.script_hash
        to_script_hash = to_account.script_hash
        amount = 10

        balance_from, _ = await self.call('balanceOf', [from_script_hash], return_type=int)
        balance_to, _ = await self.call('balanceOf', [to_script_hash], return_type=int)
        self.assertGreater(balance_from, amount)

        # transferring tokens to yourself
        result, notifications = await self.call(
            'transfer',
            [from_script_hash, from_script_hash, amount, None],
            return_type=bool,
            signing_accounts=[from_account]
        )
        self.assertEqual(True, result)

        # fire the transfer event when transferring to yourself
        transfer_events = self.filter_events(notifications, notification_type=boatestcase.Nep17TransferEvent)
        self.assertEqual(1, len(transfer_events))
        event = transfer_events[0]

        self.assertEqual(from_script_hash, event.source)
        self.assertEqual(from_script_hash, event.destination)
        self.assertEqual(amount, event.amount)

        # # transferring tokens to another account
        result, notifications = await self.call(
            'transfer',
            [from_script_hash, to_script_hash, amount, None],
            return_type=bool,
            signing_accounts=[from_account]
        )
        self.assertEqual(True, result)

        # fire the transfer event when transferring to yourself
        transfer_events = self.filter_events(notifications, notification_type=boatestcase.Nep17TransferEvent)
        self.assertEqual(1, len(transfer_events))
        event = transfer_events[0]

        self.assertEqual(from_script_hash, event.source)
        self.assertEqual(to_script_hash, event.destination)
        self.assertEqual(amount, event.amount)

        new_balance_from, _ = await self.call('balanceOf', [from_script_hash], return_type=int)
        new_balance_to, _ = await self.call('balanceOf', [to_script_hash], return_type=int)

        self.assertEqual(balance_from - amount, new_balance_from)
        self.assertEqual(balance_to + amount, new_balance_to)

    async def test_transfer_fail_no_sign(self):
        from_account = self.owner.script_hash
        to_account = self.account1.script_hash
        amount = 10

        balance, _ = await self.call('balanceOf', [from_account], return_type=int)
        self.assertGreater(balance, amount)

        result, _ = await self.call(
            'transfer',
            [from_account, to_account, amount, None],
            return_type=bool
        )
        self.assertEqual(False, result)

    async def test_transfer_fail_insufficient_balance(self):
        no_balance_account = self.account2
        other_account = self.account1.script_hash
        amount = 10

        balance, _ = await self.call('balanceOf', [no_balance_account.script_hash], return_type=int)
        self.assertEqual(0, balance)

        result, _ = await self.call(
            'transfer',
            [no_balance_account.script_hash, other_account, amount, None],
            return_type=bool,
            signing_accounts=[no_balance_account]
        )
        self.assertEqual(False, result)

    async def test_transfer_fail_bad_account(self):
        bad_account = bytes(10)
        other_account = self.owner
        account_script_hash = other_account.script_hash
        amount = 10

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call(
                'transfer',
                [account_script_hash, bad_account, amount, None],
                return_type=bool,
                signing_accounts=[other_account]
            )

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call(
                'transfer',
                [bad_account, account_script_hash, amount, None],
                return_type=bool,
                signing_accounts=[other_account]
            )

    async def test_transfer_fail_invalid_amount(self):
        from_account = self.owner.script_hash
        to_account = self.account1.script_hash
        amount = -1

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'transfer',
                [from_account, to_account, amount, None],
                return_type=bool,
                signing_accounts=[self.owner]
            )

    async def test_on_nep17_payment_receive_neo(self):
        # transferring NEO to the smart contract
        # saving the balance before the transfer to be able to compare after it
        sender = self.genesis
        sender_script_hash = sender.script_hash
        neo_amount = 10
        neo_decimals = 0
        mint_per_neo = 10 * 10 ** neo_decimals

        balance_sender, _ = await self.call(
            'balanceOf',
            [sender_script_hash],
            return_type=int
        )

        mint_amount = mint_per_neo * neo_amount
        result, notifications = await self.transfer(
            CONTRACT_HASHES.NEO_TOKEN,
            sender_script_hash,
            self.contract_hash,
            neo_amount, neo_decimals,
            signing_account=sender
        )
        self.assertEqual(True, result)

        transfer_events = self.filter_events(notifications,
                                             origin=[self.contract_hash, CONTRACT_HASHES.NEO_TOKEN],
                                             notification_type=boatestcase.Nep17TransferEvent
                                             )
        self.assertEqual(len(transfer_events), 2)
        neo_transfer_event, nep17_mint_event = transfer_events

        self.assertEqual(sender_script_hash, neo_transfer_event.source)
        self.assertEqual(self.contract_hash, neo_transfer_event.destination)
        self.assertEqual(neo_amount, neo_transfer_event.amount)

        self.assertIsNone(nep17_mint_event.source)
        self.assertEqual(sender_script_hash, nep17_mint_event.destination)
        self.assertEqual(mint_amount, nep17_mint_event.amount)

        new_balance_sender, _ = await self.call(
            'balanceOf',
            [sender_script_hash],
            return_type=int
        )
        self.assertEqual(balance_sender + mint_amount, new_balance_sender)

    async def test_on_nep17_payment_receive_gas(self):
        # transferring GAS to the smart contract
        # saving the balance before the transfer to be able to compare after it
        sender = self.genesis
        sender_script_hash = sender.script_hash
        gas_amount = 10
        gas_decimals = 8
        mint_per_gas = 2 * 10 ** gas_decimals

        balance_sender, _ = await self.call(
            'balanceOf',
            [sender_script_hash],
            return_type=int
        )

        mint_amount = mint_per_gas * gas_amount
        result, notifications = await self.transfer(
            CONTRACT_HASHES.GAS_TOKEN,
            sender_script_hash,
            self.contract_hash,
            gas_amount, gas_decimals,
            signing_account=sender
        )
        self.assertEqual(True, result)

        transfer_events = self.filter_events(notifications,
                                             origin=[self.contract_hash, CONTRACT_HASHES.GAS_TOKEN],
                                             notification_type=boatestcase.Nep17TransferEvent
                                             )
        self.assertEqual(2, len(transfer_events))
        gas_transfer_event, nep17_mint_event = transfer_events

        self.assertEqual(sender_script_hash, gas_transfer_event.source)
        self.assertEqual(self.contract_hash, gas_transfer_event.destination)
        self.assertEqual(gas_amount * 10 ** gas_decimals, gas_transfer_event.amount)

        self.assertIsNone(nep17_mint_event.source)
        self.assertEqual(sender_script_hash, nep17_mint_event.destination)
        self.assertEqual(mint_amount, nep17_mint_event.amount)

        new_balance_sender, _ = await self.call(
            'balanceOf',
            [sender_script_hash],
            return_type=int
        )
        self.assertEqual(balance_sender + mint_amount, new_balance_sender)

    async def test_on_nep17_payment_abort(self):
        # trying to call onNEP17Payment() will result in an abort if the one calling it is not NEO or GAS contracts
        with self.assertRaises(boatestcase.AbortException):
            await self.call(
                'onNEP17Payment',
                [self.owner.script_hash, 0, None],
                return_type=None,
                signing_accounts=[self.owner]
            )

    async def test_verify(self):
        # should fail without signature
        result, _ = await self.call('verify', return_type=bool)
        self.assertEqual(False, result)

        # should fail if not signed by the owner
        result, _ = await self.call('verify', return_type=bool, signing_accounts=[self.account1])
        self.assertEqual(False, result)

        result, _ = await self.call('verify', return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, result)
