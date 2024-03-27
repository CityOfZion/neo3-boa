import json

from neo3.contracts.contract import CONTRACT_HASHES
from neo3.wallet import account

from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase
from boa3_test.tests.event import UpdateEvent


class TestUpdateContractTemplate(boatestcase.BoaTestCase):
    default_folder: str = 'examples'

    owner: account.Account
    other_account: account.Account

    GAS_TO_DEPLOY = 1000 * 10 ** 8

    @classmethod
    def setupTestCase(cls):
        cls.owner = cls.node.wallet.account_new(label='owner', password='123')
        cls.other_account = cls.node.wallet.account_new(label='otherAccount', password='123')

        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.owner.script_hash, 100)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.other_account.script_hash, 100)

        await cls.set_up_contract('update_contract.py', signing_account=cls.owner)

    def test_update_contract_compile(self):
        self.assertCompile('update_contract.py')
        self.assertCompile('update_contract.py', root_folder='examples/auxiliary_contracts')

    async def test_update_contract(self):
        # Saving user's balance before calling method to compare it later
        tokens_before, _ = await self.call('balanceOf', [self.other_account.script_hash], return_type=int)

        # The bugged method is being called and the user is able to receive tokens for free
        result, notifications = await self.call('method', [self.other_account.script_hash], return_type=None, signing_accounts=[self.other_account])
        self.assertIsNone(result)

        tokens_after, _ = await self.call('balanceOf', [self.other_account.script_hash], return_type=int)

        transfer_events = self.filter_events(notifications, notification_type=boatestcase.Nep17TransferEvent)
        self.assertEqual(1, len(transfer_events))

        # The amount of tokens will be higher after calling the method
        self.assertGreater(tokens_after, tokens_before)

        # new smart contract that has the bug fixed
        path_new = self.get_contract_path('examples/auxiliary_contracts', 'update_contract.py')
        new_nef, new_manifest = self.get_serialized_output(path_new)

        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        # The smart contract will be updated to fix the bug in the method
        result, notifications = await self.call('update_sc', [new_nef, arg_manifest, None], return_type=None, signing_accounts=[self.owner])
        self.assertIsNone(result)

        # An `Update` event was be emitted after the update
        update_events = self.filter_events(notifications, notification_type=UpdateEvent)
        self.assertEqual(1, len(update_events))

        # Saving user's balance before calling method to compare it later
        tokens_before, _ = await self.call('balanceOf', [self.other_account.script_hash], return_type=int)

        # Now, when method is called, it won't mint new tokens to any user that called it
        result, notifications = await self.call('method', [self.other_account.script_hash], return_type=None, signing_accounts=[self.other_account])
        self.assertIsNone(result)

        transfer_events = self.filter_events(notifications, notification_type=boatestcase.Nep17TransferEvent)
        self.assertEqual(0, len(transfer_events))

        # The amount of tokens now is the same before and after calling the method
        tokens_after, _ = await self.call('balanceOf', [self.other_account.script_hash], return_type=int)

        self.assertEqual(tokens_after, tokens_before)

        # If the signing account is the owner, then the method works, and it will mint the new tokens
        tokens_before, _ = await self.call('balanceOf', [self.other_account.script_hash], return_type=int)

        result, notifications = await self.call('method', [self.other_account.script_hash], return_type=None, signing_accounts=[self.owner])
        self.assertIsNone(result)

        transfer_events = self.filter_events(notifications, notification_type=boatestcase.Nep17TransferEvent)
        self.assertEqual(1, len(transfer_events))

        # The amount of tokens will be higher after calling the method
        tokens_after, _ = await self.call('balanceOf', [self.other_account.script_hash], return_type=int)

        self.assertGreater(tokens_after, tokens_before)
