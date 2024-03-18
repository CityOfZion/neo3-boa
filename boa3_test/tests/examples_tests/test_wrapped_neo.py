from dataclasses import dataclass

from neo3.api import noderpc
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.wallet import account

from boa3_test.tests import boatestcase


class TestWrappedTokenTemplate(boatestcase.BoaTestCase):
    default_folder: str = 'examples'

    DECIMALS = 0
    TOTAL_SUPPLY = 10_000_000 * 10 ** DECIMALS
    OWNER_BALANCE = TOTAL_SUPPLY

    owner: account.Account
    account1: account.Account
    account2: account.Account
    account3: account.Account

    @classmethod
    def setupTestCase(cls):
        cls.owner = cls.node.wallet.account_new(label='owner', password='123')
        cls.account1 = cls.node.wallet.account_new(label='test1', password='123')
        cls.account2 = cls.node.wallet.account_new(label='test2', password='123')
        cls.account3 = cls.node.wallet.account_new(label='test3', password='123')

        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.owner.script_hash, 100)
        await cls.transfer(CONTRACT_HASHES.NEO_TOKEN, cls.genesis.script_hash, cls.owner.script_hash, 100)
        await cls.set_up_contract('wrapped_neo.py', signing_account=cls.owner)

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 100)
        await cls.transfer(CONTRACT_HASHES.NEO_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 100)

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account2.script_hash, 100)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account3.script_hash, 100)

        mint_owner = 50
        mint_account = 20
        success, _ = await cls.transfer(
            CONTRACT_HASHES.NEO_TOKEN,
            cls.owner.script_hash, cls.contract_hash, mint_owner,
            signing_account=cls.owner
        )
        cls.OWNER_BALANCE += mint_owner

        success, _ = await cls.transfer(
            CONTRACT_HASHES.NEO_TOKEN,
            cls.account1.script_hash, cls.contract_hash, mint_account,
            signing_account=cls.account1
        )
        cls.TOTAL_SUPPLY += mint_owner + mint_account

        await cls.call(
            'approve',
            [cls.account1.script_hash, cls.account3.script_hash, 5],
            return_type=bool,
            signing_accounts=[cls.account1]
        )

    def test_compile(self):
        path = self.get_contract_path('wrapped_neo.py')
        self.assertCompile(path)

    async def test_symbol(self):
        expected = 'zNEO'
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
        self.assertGreaterEqual(balance_from, amount)

        # transferring tokens to yourself
        result, notifications = await self.call(
            'transfer',
            [from_script_hash, from_script_hash, amount, None],
            return_type=bool,
            signing_accounts=[from_account]
        )
        self.assertEqual(True, result)

        # fire the transfer event when transferring to yourself
        transfer_events = self.filter_events(
            notifications,
            origin=self.contract_hash,
            notification_type=boatestcase.Nep17TransferEvent
        )
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
        transfer_events = self.filter_events(
            notifications,
            origin=self.contract_hash,
            notification_type=boatestcase.Nep17TransferEvent
        )
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

        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'transfer',
                [bad_account, account_script_hash, amount, None],
                return_type=bool,
                signing_accounts=[other_account]
            )

    async def test_transfer_fail_invalid_amount(self):
        some_account = self.owner
        account_script_hash = some_account.script_hash
        invalid_amount = -10

        # should fail when given amount is negative
        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'transfer',
                [account_script_hash, account_script_hash, invalid_amount, None],
                return_type=bool,
                signing_accounts=[some_account]
            )

    async def test_on_nep17_payment_receive_neo(self):
        # transferring NEO to the smart contract
        # saving the balance before the transfer to be able to compare after it
        sender = self.genesis
        sender_script_hash = sender.script_hash
        neo_amount = 10

        balance_sender, _ = await self.call(
            'balanceOf',
            [sender_script_hash],
            return_type=int
        )

        result, notifications = await self.transfer(
            CONTRACT_HASHES.NEO_TOKEN,
            sender_script_hash,
            self.contract_hash,
            neo_amount,
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
        self.assertEqual(neo_amount, nep17_mint_event.amount)

        new_balance_sender, _ = await self.call(
            'balanceOf',
            [sender_script_hash],
            return_type=int
        )
        self.assertEqual(balance_sender + neo_amount, new_balance_sender)

    async def test_on_nep17_payment_receive_gas(self):
        # transferring GAS to the smart contract
        sender = self.genesis
        sender_script_hash = sender.script_hash
        gas_amount = 10
        gas_decimals = 8

        result, notifications = await self.transfer(
            CONTRACT_HASHES.GAS_TOKEN,
            sender_script_hash,
            self.contract_hash,
            gas_amount,
            signing_account=sender
        )
        self.assertEqual(True, result)

        transfer_events = self.filter_events(notifications,
                                             origin=CONTRACT_HASHES.GAS_TOKEN,
                                             notification_type=boatestcase.Nep17TransferEvent
                                             )
        self.assertEqual(1, len(transfer_events))
        gas_transfer_event = transfer_events[0]

        self.assertEqual(sender_script_hash, gas_transfer_event.source)
        self.assertEqual(self.contract_hash, gas_transfer_event.destination)
        self.assertEqual(gas_amount * 10 ** gas_decimals, gas_transfer_event.amount)

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
        result, _ = await self.call('verify', return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('verify', return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, result)

        result, _ = await self.call('verify', return_type=bool, signing_accounts=[self.account1])
        self.assertEqual(False, result)

    async def test_burn_success(self):
        burned_amount = 5
        user = self.account1
        user_script_hash = user.script_hash

        balance, _ = await self.call('balanceOf', [user_script_hash], return_type=int)
        self.assertGreaterEqual(balance, burned_amount)

        _, notifications = await self.call(
            'burn',
            [user_script_hash, burned_amount],
            return_type=None,
            signing_accounts=[user]
        )

        transfer_events = self.filter_events(notifications,
                                             origin=[self.contract_hash, CONTRACT_HASHES.NEO_TOKEN],
                                             notification_type=boatestcase.Nep17TransferEvent
                                             )
        self.assertEqual(len(transfer_events), 2)
        nep17_burn_event, neo_transfer_event = transfer_events

        self.assertEqual(self.contract_hash, neo_transfer_event.source)
        self.assertEqual(user_script_hash, neo_transfer_event.destination)
        self.assertEqual(burned_amount, neo_transfer_event.amount)

        self.assertEqual(user_script_hash, nep17_burn_event.source)
        self.assertIsNone(nep17_burn_event.destination)
        self.assertEqual(burned_amount, nep17_burn_event.amount)

        new_balance, _ = await self.call(
            'balanceOf',
            [user_script_hash],
            return_type=int
        )
        self.assertEqual(balance - burned_amount, new_balance)

    async def test_burn_fail_no_sign(self):
        burned_amount = 5
        user = self.account1

        balance, _ = await self.call('balanceOf', [user.script_hash], return_type=int)
        self.assertGreaterEqual(balance, burned_amount)

        _, notifications = await self.call(
            'burn',
            [user.script_hash, burned_amount],
            return_type=None
        )
        self.assertEqual(0, len(notifications))

    async def test_burn_fail_insufficient_balance(self):
        burned_amount = 100
        no_balance_account = self.account2

        balance, _ = await self.call('balanceOf', [no_balance_account.script_hash], return_type=int)
        self.assertEqual(0, balance)

        with self.assertRaises(boatestcase.AssertException):
            result, _ = await self.call(
                'burn',
                [no_balance_account.script_hash, burned_amount],
                return_type=None,
                signing_accounts=[no_balance_account]
            )

    async def test_burn_fail_bad_account(self):
        burned_amount = 10
        bad_account = bytes(10)

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'burn',
                [bad_account, burned_amount],
                return_type=None,
            )

    async def test_burn_fail_invalid_amount(self):
        some_account = self.account1
        invalid_amount = -10

        # should fail when given amount is negative
        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'burn',
                [some_account.script_hash, invalid_amount],
                return_type=None,
                signing_accounts=[some_account]
            )

    async def test_approve_success(self):
        token_owner = self.account1
        spender = self.account2
        amount = 2

        balance, _ = await self.call('balanceOf', [token_owner.script_hash], return_type=int)
        self.assertGreaterEqual(balance, amount)

        result, notifications = await self.call(
            'approve',
            [token_owner.script_hash, spender.script_hash, amount],
            return_type=bool,
            signing_accounts=[token_owner]
        )
        self.assertEqual(True, result)
        approvals = self.filter_events(
            notifications,
            origin=self.contract_hash,
            notification_type=ApprovalEvent
        )
        self.assertEqual(1, len(approvals))

        approval_event = approvals[0]
        self.assertEqual(token_owner.script_hash, approval_event.owner)
        self.assertEqual(spender.script_hash, approval_event.spender)
        self.assertEqual(amount, approval_event.amount)

    async def test_approve_success_no_sign(self):
        token_owner = self.account1
        spender = self.account2
        amount = 2

        balance, _ = await self.call('balanceOf', [token_owner.script_hash], return_type=int)
        self.assertGreaterEqual(balance, amount)

        result, notifications = await self.call(
            'approve',
            [token_owner.script_hash, spender.script_hash, amount],
            return_type=bool
        )
        self.assertEqual(False, result)
        self.assertEqual(0, len(notifications))

    async def test_approve_success_insufficient_balance(self):
        token_owner = self.account2
        spender = self.account1
        amount = 2

        balance, _ = await self.call('balanceOf', [token_owner.script_hash], return_type=int)
        self.assertLess(balance, amount)

        result, notifications = await self.call(
            'approve',
            [token_owner.script_hash, spender.script_hash, amount],
            return_type=bool,
            signing_accounts=[token_owner]
        )
        self.assertEqual(False, result)
        self.assertEqual(0, len(notifications))

    async def test_approve_success_bad_account(self):
        bad_account = bytes(10)
        other_account = self.owner.script_hash
        amount = 2

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'approve',
                [bad_account, other_account, amount],
                return_type=bool,
                signing_accounts=[self.owner]
            )

        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'approve',
                [other_account, bad_account, amount],
                return_type=bool,
                signing_accounts=[self.owner]
            )

    async def test_allowance(self):
        allowed_amount = 10
        owner = self.owner
        test_account_1 = self.account1
        test_account_2 = self.account2

        # owner did not approve account2
        result, _ = await self.call('allowance', [owner.script_hash, test_account_2.script_hash], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call(
            'approve',
            [owner.script_hash, test_account_1.script_hash, allowed_amount],
            return_type=bool,
            signing_accounts=[owner]
        )
        self.assertEqual(True, result)

        result, _ = await self.call('allowance', [owner.script_hash, test_account_1.script_hash], return_type=int)
        self.assertEqual(allowed_amount, result)

    async def test_transfer_from_success(self):
        spender = self.account3
        from_ = self.account1
        to = self.account2
        amount = 3

        balance_from, _ = await self.call('balanceOf', [from_.script_hash], return_type=int)
        balance_to, _ = await self.call('balanceOf', [to.script_hash], return_type=int)
        self.assertGreaterEqual(balance_from, amount)

        allowance, _ = await self.call('allowance', [from_.script_hash, spender.script_hash], return_type=int)
        self.assertGreaterEqual(allowance, amount)

        result, notifications = await self.call(
            'transferFrom',
            [spender.script_hash, from_.script_hash, to.script_hash, amount, None],
            return_type=bool,
            signing_accounts=[spender]
        )
        self.assertEqual(True, result)

        # fire the transfer event when transferring to yourself
        transfer_events = self.filter_events(
            notifications,
            origin=self.contract_hash,
            notification_type=boatestcase.Nep17TransferEvent
        )
        self.assertEqual(1, len(transfer_events))
        event = transfer_events[0]

        self.assertEqual(from_.script_hash, event.source)
        self.assertEqual(to.script_hash, event.destination)
        self.assertEqual(amount, event.amount)

        new_balance_from, _ = await self.call('balanceOf', [from_.script_hash], return_type=int)
        new_balance_to, _ = await self.call('balanceOf', [to.script_hash], return_type=int)

        self.assertEqual(balance_from - amount, new_balance_from)
        self.assertEqual(balance_to + amount, new_balance_to)

    async def test_transfer_from_fail_no_sign(self):
        spender = self.account3
        from_ = self.account1
        to = self.account2
        amount = 3

        balance_from, _ = await self.call('balanceOf', [from_.script_hash], return_type=int)
        self.assertGreaterEqual(balance_from, amount)

        allowance, _ = await self.call('allowance', [from_.script_hash, spender.script_hash], return_type=int)
        self.assertGreaterEqual(allowance, amount)

        result, _ = await self.call(
            'transferFrom',
            [spender.script_hash, from_.script_hash, to.script_hash, amount, None],
            return_type=bool
        )
        self.assertEqual(False, result)

    async def test_transfer_from_fail_insufficient_balance(self):
        no_balance_account = self.account2.script_hash
        spender_account = self.account3
        other_account = self.account1.script_hash
        amount = 10

        balance, _ = await self.call('balanceOf', [no_balance_account], return_type=int)
        self.assertLess(balance, amount)

        result, _ = await self.call(
            'transferFrom',
            [spender_account.script_hash, no_balance_account, other_account, amount, None],
            return_type=bool,
            signing_accounts=[spender_account]
        )
        self.assertEqual(False, result)

    async def test_transfer_from_fail_insufficient_allowance(self):
        spender = self.account3
        from_ = self.account1
        to = self.account2
        amount = 6

        balance_from, _ = await self.call('balanceOf', [from_.script_hash], return_type=int)
        self.assertGreaterEqual(balance_from, amount)

        allowance, _ = await self.call('allowance', [from_.script_hash, spender.script_hash], return_type=int)
        self.assertLess(allowance, amount)

        result, _ = await self.call(
            'transferFrom',
            [spender.script_hash, from_.script_hash, to.script_hash, amount, None],
            return_type=bool,
            signing_accounts=[spender]
        )
        self.assertEqual(False, result)

    async def test_transfer_from_fail_bad_account(self):
        bad_account = bytes(10)
        other_account = self.owner
        account_script_hash = other_account.script_hash
        amount = 10

        # should fail when any of the scripts' length is not 20
        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'transferFrom',
                [bad_account, account_script_hash, account_script_hash, amount, None],
                return_type=bool,
                signing_accounts=[other_account]
            )

        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'transferFrom',
                [account_script_hash, bad_account, account_script_hash, amount, None],
                return_type=bool,
                signing_accounts=[other_account]
            )

        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'transferFrom',
                [account_script_hash, account_script_hash, bad_account, amount, None],
                return_type=bool,
                signing_accounts=[other_account]
            )

    async def test_transfer_from_fail_invalid_amount(self):
        spender = self.account3
        from_ = self.account1
        to = self.account2
        invalid_amount = -10

        # should fail when given amount is negative
        with self.assertRaises(boatestcase.AssertException):
            await self.call(
                'transferFrom',
                [spender.script_hash, from_.script_hash, to.script_hash, invalid_amount, None],
                return_type=bool,
                signing_accounts=[spender]
            )


@dataclass
class ApprovalEvent(boatestcase.BoaTestEvent):
    owner: types.UInt160
    spender: types.UInt160
    amount: int

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification):
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)
