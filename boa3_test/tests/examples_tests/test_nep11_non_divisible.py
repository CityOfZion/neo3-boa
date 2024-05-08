import json
from typing import Self

from neo3.api import StackItemType
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.wallet import account

from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase, event


class TestNEP11NonDivisibleTemplate(boatestcase.BoaTestCase):
    default_folder: str = 'examples'

    DECIMALS = 0
    OWNER_BALANCE = 0
    TOTAL_SUPPLY = 0

    owner: account.Account
    account1: account.Account
    account2: account.Account

    TOKEN_ID_TRANSFER_TEST: bytes
    TEST_TOKEN_ID: bytes

    TOKEN_META = bytes(
        '{ "name": "NEP11", "description": "Some description", "image": "{some image URI}", "tokenURI": "{some URI}" }',
        'utf-8')
    TOKEN_LOCKED = bytes('lockedContent', 'utf-8')
    ROYALTIES = bytes(
        '[{"address": "NZcuGiwRu1QscpmCyxj5XwQBUf6sk7dJJN", "value": 2000}, '
        '{"address": "NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB", "value": 3000}]',
        'utf-8')

    ACCOUNT_PREFIX = b'ACC'

    @classmethod
    def setupTestCase(cls):
        cls.owner = cls.node.wallet.account_new(label='owner', password='123')
        cls.account1 = cls.node.wallet.account_new(label='test1', password='123')
        cls.account2 = cls.node.wallet.account_new(label='test2', password='123')

        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.owner.script_hash, 100)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 100)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account2.script_hash, 100)

        await cls.set_up_contract('nep11_non_divisible.py', signing_account=cls.owner)

        mint_args = [cls.TOKEN_META, cls.TOKEN_LOCKED, cls.ROYALTIES]
        mint_amount = 5
        account_balance = 2
        for _ in range(mint_amount):
            await cls.call(
                'mint',
                [cls.owner.script_hash, *mint_args],
                return_type=bytes,
                signing_accounts=[cls.owner]
            )

        account_tokens: list[bytes] = []
        for _ in range(account_balance):
            result, _ = await cls.call(
                'mint',
                [cls.account1.script_hash, *mint_args],
                return_type=bytes,
                signing_accounts=[cls.account1]
            )
            account_tokens.append(result)

        cls.TOKEN_ID_TRANSFER_TEST, cls.TEST_TOKEN_ID = account_tokens
        cls.OWNER_BALANCE = mint_amount
        cls.TOTAL_SUPPLY = mint_amount + account_balance

    def test_compile(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        _, manifest = self.assertCompile(path, get_manifest=True)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-11', manifest['supportedstandards'])

    async def test_symbol(self):
        expected = 'EXMP'
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
        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call("balanceOf", [bad_account], return_type=int)
        self.assertEqual(str(context.exception), 'Not a valid address')

        bad_account = bytes(30)
        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call("balanceOf", [bad_account], return_type=int)
        self.assertEqual(str(context.exception), 'Not a valid address')

    async def test_tokens_of(self):
        no_balance_account = types.UInt160.zero()
        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('tokensOf', [no_balance_account], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        tokens_of_storage = await self.get_storage(
            self.ACCOUNT_PREFIX + no_balance_account.to_array(),
            remove_prefix=True
        )
        self.assertEqual(0, len(tokens_of_storage))

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('tokensOf', [self.owner.script_hash], return_type=list)
            self.assertEqual(self.OWNER_BALANCE, len(result))

        self.assertRegex(
            str(context.exception),
            fr"item is not of type 'StackItemType.\w+' but of type '{StackItemType.INTEROP_INTERFACE}'"
        )

        tokens_of_storage = await self.get_storage(
            self.ACCOUNT_PREFIX + self.owner.script_hash.to_array(),
            remove_prefix=True
        )
        self.assertEqual(self.OWNER_BALANCE, len(tokens_of_storage))

    async def test_transfer_success(self):
        token = self.TOKEN_ID_TRANSFER_TEST
        from_account = self.account1.script_hash
        to_account = self.account2.script_hash

        total_supply, _ = await self.call('totalSupply', [], return_type=int)

        # check owner before
        result, _ = await self.call('ownerOf', [token], return_type=types.UInt160)
        self.assertEqual(from_account, result)

        # transfer
        result, notifications = await self.call(
            'transfer',
            [to_account, token, None],
            return_type=bool,
            signing_accounts=[self.account1]
        )
        self.assertEqual(True, result)
        transfer_events = self.filter_events(
            notifications,
            origin=[self.contract_hash],
            event_name='Transfer',
            notification_type=boatestcase.Nep11TransferEvent
        )
        self.assertEqual(len(transfer_events), 1)
        self.assertEqual(from_account, transfer_events[0].source)
        self.assertEqual(to_account, transfer_events[0].destination)
        self.assertEqual(1, transfer_events[0].amount)
        self.assertEqual(token.decode('utf-8'), transfer_events[0].token_id)

        # check owner after
        result, _ = await self.call('ownerOf', [token], return_type=types.UInt160)
        self.assertEqual(self.account2.script_hash, result)

        # check balances after
        result, _ = await self.call('balanceOf', [from_account], return_type=int)
        self.assertEqual(1, result)
        result, _ = await self.call('totalSupply', [], return_type=int)
        self.assertEqual(total_supply, result)

    async def test_transfer_fail_no_sign(self):
        token = self.TEST_TOKEN_ID
        from_account = self.account1.script_hash
        to_account = self.account2.script_hash

        # check owner before
        result, _ = await self.call('ownerOf', [token], return_type=types.UInt160)
        self.assertEqual(from_account, result)

        # transfer
        result, notifications = await self.call(
            'transfer',
            [to_account, token, None],
            return_type=bool
        )
        self.assertEqual(False, result)

        transfers = self.filter_events(
            notifications,
            origin=[self.contract_hash],
            event_name='Transfer',
            notification_type=boatestcase.Nep11TransferEvent
        )
        self.assertEqual(0, len(transfers))

    async def test_transfer_fail_wrong_token_owner(self):
        token = self.TEST_TOKEN_ID
        from_account = self.account2.script_hash
        to_account = self.account1.script_hash

        # check if owner is incorrect
        result, _ = await self.call('ownerOf', [token], return_type=types.UInt160)
        self.assertNotEqual(from_account, result)

        # transfer
        result, notifications = await self.call(
            'transfer',
            [to_account, token, None],
            return_type=bool,
            signing_accounts=[self.account2]
        )
        self.assertEqual(False, result)

        transfers = self.filter_events(
            notifications,
            origin=[self.contract_hash],
            event_name='Transfer',
            notification_type=boatestcase.Nep11TransferEvent
        )
        self.assertEqual(0, len(transfers))

    async def test_transfer_fail_non_existing_token(self):
        token = b'thisisanonexistingtoken'

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call(
                'transfer',
                [self.account2.script_hash, token, None],
                return_type=bool
            )
        self.assertEqual(str(context.exception), 'Token not found')

    async def test_transfer_fail_bad_account(self):
        token = self.TEST_TOKEN_ID
        to_account = bytes(10)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call(
                'transfer',
                [to_account, token, None],
                return_type=bool,
                signing_accounts=[self.account1]
            )
        self.assertEqual(str(context.exception), 'Not a valid address')

    async def test_on_nep11_payment_call(self):
        # trying to call onNEP11Payment() will result in an abort if the one calling it is not NEO or GAS contracts
        with self.assertRaises(boatestcase.AbortException):
            await self.call(
                'onNEP11Payment',
                [self.owner.script_hash, 1, self.TEST_TOKEN_ID, None],
                return_type=None,
                signing_accounts=[self.owner]
            )

    async def test_on_nep11_payment_receive_self(self):
        token = self.TEST_TOKEN_ID
        from_account = self.account1.script_hash
        to_account = self.contract_hash

        # check owner before
        result, _ = await self.call('ownerOf', [token], return_type=types.UInt160)
        self.assertEqual(from_account, result)

        with self.assertRaises(boatestcase.AbortException):
            await self.call(
                'transfer',
                [to_account, token, None],
                return_type=bool,
                signing_accounts=[self.account1]
            )

    async def test_update(self):
        path = self.get_contract_path('nep11_non_divisible.py')

        new_nef, new_manifest = self.get_serialized_output(path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        with self.assertRaises(boatestcase.AssertException) as context:
            # missing signature
            await self.call(
                'update',
                [new_nef, arg_manifest],
                return_type=None
            )
        self.assertEqual(str(context.exception), '`account` is not allowed for update')

        result, notifications = await self.call(
            'update',
            [new_nef, arg_manifest],
            return_type=None,
            signing_accounts=[self.owner]
        )
        self.assertIsNone(result)

        update_events = self.filter_events(
            notifications,
            event_name='Update',
            notification_type=event.UpdateEvent
        )
        self.assertEqual(1, len(update_events))
        self.assertEqual(self.contract_hash, update_events[0].updated_contract)

    async def test_destroy(self):
        owner_test_destroy = self.account2

        contract_hash = await self.compile_and_deploy(
            'nep11_non_divisible.py',
            signing_account=owner_test_destroy
        )

        with self.assertRaises(boatestcase.AssertException) as context:
            # missing signature
            await self.call(
                'destroy', [],
                return_type=None,
                target_contract=contract_hash
            )
        self.assertEqual(str(context.exception), '`account` is not allowed for destroy')

        result, notifications = await self.call(
            'destroy', [],
            return_type=None,
            target_contract=contract_hash,
            signing_accounts=[owner_test_destroy]
        )
        self.assertIsNone(result)

        destroy_events = self.filter_events(
            notifications,
            event_name='Destroy',
            notification_type=event.DestroyEvent
        )
        self.assertEqual(1, len(destroy_events))
        self.assertEqual(contract_hash, destroy_events[0].destroyed_contract)

        # should not exist anymore
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('symbol', [], return_type=str, target_contract=contract_hash)
        self.assertRegex(str(context.exception), f'called contract {contract_hash} not found')

    async def test_verify(self):
        result, _ = await self.call('getAuthorizedAddress', [], return_type=list[types.UInt160])
        self.assertEqual([self.owner.script_hash], result)

        result, _ = await self.call('verify', [], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, result)

        result, _ = await self.call('verify', [], return_type=bool, signing_accounts=[self.account1])
        self.assertEqual(False, result)

        result, _ = await self.call('verify', [], return_type=bool, signing_accounts=[self.account2])
        self.assertEqual(False, result)

    async def test_authorize(self):
        from dataclasses import dataclass
        from neo3.api import noderpc

        @dataclass
        class AuthorizedEvent(boatestcase.BoaTestEvent):
            authorized: types.UInt160
            type: int
            add: bool

            @classmethod
            def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
                inner_args_types = tuple(cls.__annotations__.values())
                e = super().from_notification(n, *inner_args_types)
                return cls(e.contract, e.name, e.state, *e.state)

        account = self.account1.script_hash

        result, notifications = await self.call(
            'setAuthorizedAddress',
            [account, True],
            return_type=None,
            signing_accounts=[self.owner]
        )
        self.assertIsNone(result)

        authorized = self.filter_events(
            notifications,
            event_name='Authorized',
            notification_type=AuthorizedEvent
        )
        self.assertEqual(1, len(authorized))
        self.assertEqual(account, authorized[0].authorized)
        self.assertEqual(0, authorized[0].type)
        self.assertEqual(True, authorized[0].add)

        # now deauthorize the address
        result, notifications = await self.call(
            'setAuthorizedAddress',
            [account, False],
            return_type=None,
            signing_accounts=[self.owner]
        )
        self.assertIsNone(result)

        authorized = self.filter_events(
            notifications,
            event_name='Authorized',
            notification_type=AuthorizedEvent
        )
        self.assertEqual(1, len(authorized))
        self.assertEqual(account, authorized[0].authorized)
        self.assertEqual(0, authorized[0].type)
        self.assertEqual(False, authorized[0].add)

    async def test_pause(self):
        # missing owner signing transaction
        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('updatePause', [True], return_type=bool)
        self.assertEqual(str(context.exception), '`account` is not allowed for updatePause')

        test_account = self.account2.script_hash
        # pause contract
        result, _ = await self.call('updatePause', [True], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, result)

        # should fail because contract is paused
        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call(
                'mint',
                [test_account, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES],
                return_type=str,
                signing_accounts=[self.account2]
            )
        self.assertEqual(str(context.exception), 'Contract is currently paused')

        # unpause contract
        result, _ = await self.call('updatePause', [False], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(False, result)

        _, notifications = await self.call(
            'mint',
            [test_account, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES],
            return_type=str,
            signing_accounts=[self.account2]
        )

        mint_events = self.filter_events(
            notifications,
            origin=[self.contract_hash],
            event_name='Transfer',
            notification_type=boatestcase.Nep11TransferEvent
        )
        self.assertEqual(len(mint_events), 1)

    async def test_mint(self):
        test_account = self.account2

        balance, _ = await self.call('balanceOf', [test_account.script_hash], return_type=int)
        total_supply, _ = await self.call('totalSupply', [], return_type=int)

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call(
                'mint',
                [test_account.script_hash, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES],
                return_type=str
            )
        self.assertEqual(str(context.exception), 'Invalid witness')

        token, notifications = await self.call(
            'mint',
            [test_account.script_hash, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES],
            return_type=str,
            signing_accounts=[test_account]
        )

        mint_events = self.filter_events(
            notifications,
            origin=[self.contract_hash],
            event_name='Transfer',
            notification_type=boatestcase.Nep11TransferEvent
        )
        self.assertEqual(len(mint_events), 1)
        self.assertEqual(None, mint_events[0].source)
        self.assertEqual(test_account.script_hash, mint_events[0].destination)
        self.assertEqual(1, mint_events[0].amount)
        self.assertEqual(token, mint_events[0].token_id)

        result, _ = await self.call('properties', [token], return_type=dict[str, str])
        token_property = json.loads(self.TOKEN_META.decode('utf-8').replace("'", "\""))
        self.assertEqual(token_property, result)

        token_royalties = self.ROYALTIES.decode('utf-8')
        result, _ = await self.call('getRoyalties', [token], return_type=str)
        self.assertEqual(token_royalties, result)

        # check balances after
        result, _ = await self.call('balanceOf', [test_account.script_hash], return_type=int)
        self.assertEqual(balance + 1, result)

        result, _ = await self.call('totalSupply', [], return_type=int)
        self.assertEqual(total_supply + 1, result)

    async def test_properties_success(self):
        token = self.TEST_TOKEN_ID
        expected = json.loads(self.TOKEN_META.decode('utf-8').replace("'", "\""))

        result, _ = await self.call('properties', [token], return_type=dict[str, str])
        self.assertEqual(expected, result)

    async def test_properties_fail_non_existent_token(self):
        token = b'thisisanonexistingtoken'

        with self.assertRaises(boatestcase.AssertException) as context:
            await self.call('properties', [token], return_type=dict[str, str])
        self.assertEqual(str(context.exception), 'No metadata available for token')

    async def test_burn(self):
        test_account = self.account2

        token, _ = await self.call(
            'mint',
            [test_account.script_hash, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES],
            return_type=str,
            signing_accounts=[test_account]
        )

        balance, _ = await self.call('balanceOf', [test_account.script_hash], return_type=int)
        total_supply, _ = await self.call('totalSupply', [], return_type=int)

        result, _ = await self.call(
            'burn',
            [token],
            return_type=bool
        )
        self.assertEqual(False, result)

        result, notifications = await self.call(
            'burn',
            [token],
            return_type=bool,
            signing_accounts=[test_account]
        )
        self.assertEqual(True, result)

        burn_events = self.filter_events(
            notifications,
            origin=[self.contract_hash],
            event_name='Transfer',
            notification_type=boatestcase.Nep11TransferEvent
        )
        self.assertEqual(len(burn_events), 1)
        self.assertEqual(test_account.script_hash, burn_events[0].source)
        self.assertEqual(None, burn_events[0].destination)
        self.assertEqual(1, burn_events[0].amount)
        self.assertEqual(token, burn_events[0].token_id)

        # check balances after
        result, _ = await self.call('balanceOf', [test_account.script_hash], return_type=int)
        self.assertEqual(balance - 1, result)

        result, _ = await self.call('totalSupply', [], return_type=int)
        self.assertEqual(total_supply - 1, result)
