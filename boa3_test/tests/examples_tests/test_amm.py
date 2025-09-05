from dataclasses import dataclass
from typing import Self

from neo3.api import noderpc
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.network.payloads import verification

from boa3.internal import constants
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.tests import boatestcase


@dataclass
class SyncEvent(boatestcase.BoaTestEvent):
    reserve_token_a: int
    reserve_token_b: int

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


@dataclass
class BurnOrMintEvent(boatestcase.BoaTestEvent):
    sender: types.UInt160
    amount_token_a: int
    amount_token_b: int

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


@dataclass
class SwapEvent(boatestcase.BoaTestEvent):
    sender: types.UInt160
    amount_token_a_in: int
    amount_token_b_in: int
    amount_token_a_out: int
    amount_token_b_out: int

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


class TestAMMTemplate(boatestcase.BoaTestCase):
    default_folder: str = 'examples'

    owner: Account
    account1: Account
    account2: Account
    balance_test: Account

    z_neo: types.UInt160
    z_gas: types.UInt160

    @classmethod
    def setupTestCase(cls):
        cls.owner = cls.node.wallet.account_new(label='test0')
        cls.account1 = cls.node.wallet.account_new(label='test1')
        cls.account2 = cls.node.wallet.account_new(label='test2')
        cls.balance_test = cls.node.wallet.account_new(label='balanceTestAccount')

        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 10_000, 8)
        await cls.transfer(CONTRACT_HASHES.NEO_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 10_000, 0)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account2.script_hash, 10_000, 8)
        await cls.transfer(CONTRACT_HASHES.NEO_TOKEN, cls.genesis.script_hash, cls.account2.script_hash, 10_000, 0)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.balance_test.script_hash, 10, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.owner.script_hash, 3000, 8)
        cls.z_neo = await cls.compile_and_deploy('wrapped_neo.py', signing_account=cls.owner)
        cls.z_gas = await cls.compile_and_deploy('wrapped_gas.py', signing_account=cls.owner)

        await cls.set_up_contract('amm.py', signing_account=cls.owner)

    @classmethod
    async def set_address(cls):
        signer = verification.Signer(cls.owner.script_hash)
        can_set_address, _ = await cls.call('set_address',
                                   [cls.z_neo, cls.z_gas],
                                   signers=[signer],
                                   return_type=bool)
        if can_set_address:
            is_set, _ = await cls.call('set_address',
                                       [cls.z_neo, cls.z_gas],
                                       signing_accounts=[cls.owner],
                                       return_type=bool)
            cls.assertEqual(cls(), True, is_set)

    def test_compile(self):
        path = self.get_contract_path('amm.py')
        self.assertCompile(path)

    async def test_set_address(self):
        # won't work because it needs the owner signature
        result, _ = await self.call('set_address', [self.z_neo, self.z_gas], return_type=bool)
        self.assertEqual(False, result)

        # set_address is conflicting with other tests
        await self.set_address()

        result, _ = await self.call('get_token_a', [], return_type=types.UInt160)
        self.assertEqual(self.z_neo, result)

        result, _ = await self.call('get_token_b', [], return_type=types.UInt160)
        self.assertEqual(self.z_gas, result)

        # initialize will work once
        result, _ = await self.call('set_address',
                                    [self.z_neo, self.z_gas],
                                    signing_accounts=[self.owner],
                                    return_type=bool)
        self.assertEqual(False, result)

    async def test_symbol(self):
        result, _ = await self.call('symbol', [], return_type=str)
        self.assertEqual('AMM', result)

    async def test_decimals(self):
        result, _ = await self.call('decimals', [], return_type=int)
        self.assertEqual(8, result)

    async def test_0_total_supply(self):
        result, _ = await self.call('totalSupply', [], return_type=int)
        self.assertEqual(0, result)

    async def test_total_balance_of(self):
        result, _ = await self.call('balanceOf', [self.owner.script_hash], return_type=int)
        self.assertEqual(0, result)

        # should fail when the script length is not 20
        with self.assertRaises(boatestcase.AssertException):
            await self.call('balanceOf', [bytes(10)], return_type=int)

        with self.assertRaises(boatestcase.AssertException):
            await self.call('balanceOf', [bytes(30)], return_type=int)

    async def test_quote(self):
        amount_zneo = 1
        reserve_zneo = 100
        reserve_zgas = 1100 * 10 ** 8

        result, _ = await self.call('quote', [amount_zneo, reserve_zneo, reserve_zgas], return_type=int)
        amount_zgas = amount_zneo * reserve_zgas // reserve_zneo
        self.assertEqual(amount_zgas, result)

    async def test_on_nep17_payment(self):
        transferred_amount = 10

        account = self.account1.script_hash
        amm = self.contract.hash

        # set_address is conflicting with other tests
        await self.set_address()

        # adding the transferred_amount into account
        result, _ = await self.call('transfer',
                                    [account, self.z_neo, transferred_amount, None],
                                    signing_accounts=[self.account1],
                                    target_contract=constants.NEO_SCRIPT,
                                    return_type=bool)
        self.assertEqual(True, result)

        # the AMM will accept this transaction, but there is no reason to send tokens directly to the smart contract.
        # to send tokens to the AMM you should use the add_liquidity function
        result, _ = await self.call('transfer',
                                    [account, amm, transferred_amount, None],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_neo,
                                    return_type=bool)
        self.assertEqual(True, result)

        # the smart contract will abort if some address other than zNEO or zGAS calls the onPayment method
        with self.assertRaises(boatestcase.AbortException):
            await self.call('onNEP17Payment',
                            [account, transferred_amount, None],
                            return_type=None)

    async def test_add_liquidity(self):
        test_balance_zneo = 1_000
        test_balance_zgas = 1_000 * 10 ** 8
        transferred_amount_zneo = 10
        transferred_amount_zgas = 110 * 10 ** 8

        account = self.account1.script_hash
        amm = self.contract.hash

        # set_address is conflicting with other tests
        await self.set_address()

        # minting zNEO to account
        result, _ = await self.call('transfer',
                                    [account, self.z_neo, test_balance_zneo, None],
                                    signing_accounts=[self.account1],
                                    target_contract=constants.NEO_SCRIPT,
                                    return_type=bool)
        self.assertEqual(True, result)

        # minting zGAS to account
        result, _ = await self.call('transfer',
                                    [account, self.z_gas, test_balance_zgas, None],
                                    signing_accounts=[self.account1],
                                    target_contract=constants.GAS_SCRIPT,
                                    return_type=bool)
        self.assertEqual(True, result)

        # won't work, because the user did not allow the amm to transfer zNEO and zGAS
        with self.assertRaises(boatestcase.AssertException):
            await self.call('add_liquidity',
                            [transferred_amount_zneo, transferred_amount_zgas, 0, 0, account],
                            signing_accounts=[self.account1],
                            return_type=list[int])

        # approving the AMM contract, so that it will be able to transfer zNEO from account
        result, _ = await self.call('approve',
                                    [account, amm, test_balance_zneo],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_neo,
                                    return_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from account
        result, _ = await self.call('approve',
                                    [account, amm, test_balance_zgas],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_gas,
                                    return_type=bool)
        self.assertEqual(True, result)

        # saving data to demonstrate that the value will change later
        total_supply_before, _ = await self.call('totalSupply', [], return_type=int)
        balance_user_amm_before, _ = await self.call('balanceOf', [account], return_type=int)
        reserves_before, _ = await self.call('get_reserves', [], return_type=list[int])
        balance_user_zneo_before, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_neo)
        balance_user_zgas_before, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_gas)
        balance_amm_zneo_before, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_neo)
        balance_amm_zgas_before, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_gas)

        # adding liquidity to the pool will give you AMM tokens in return
        liquidity, sent_amount_zneo, sent_amount_zgas = await self.calculate_add_liquidity(transferred_amount_zneo, transferred_amount_zgas)
        result, notifications = await self.call('add_liquidity',
                                                [transferred_amount_zneo, transferred_amount_zgas, 0, 0, account],
                                                signing_accounts=[self.account1],
                                                return_type=list[int])
        self.assertEqual([sent_amount_zneo, sent_amount_zgas, liquidity], result)

        # data that will be compared with the previously saved data
        total_supply_after, _ = await self.call('totalSupply', [], return_type=int)
        balance_user_amm_after, _ = await self.call('balanceOf', [account], return_type=int)
        reserves_after, _ = await self.call('get_reserves', [], return_type=list[int])
        balance_user_zneo_after, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_neo)
        balance_user_zgas_after, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_gas)
        balance_amm_zneo_after, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_neo)
        balance_amm_zgas_after, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_gas)

        transfer_events = self.filter_events(notifications,
                                             origin=amm,
                                             event_name='Transfer',
                                             notification_type=boatestcase.Nep17TransferEvent
                                             )
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(None, transfer_events[0].source)
        self.assertEqual(account, transfer_events[0].destination)
        self.assertEqual(liquidity, transfer_events[0].amount)

        sync_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Sync',
                                         notification_type=SyncEvent
                                         )
        self.assertEqual(1, len(sync_events))
        self.assertEqual(sent_amount_zneo, sync_events[0].reserve_token_a)
        self.assertEqual(sent_amount_zgas, sync_events[0].reserve_token_b)

        mint_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Mint',
                                         notification_type=BurnOrMintEvent
                                         )
        self.assertEqual(1, len(mint_events))
        self.assertEqual(account, mint_events[0].sender)
        self.assertEqual(sent_amount_zneo, mint_events[0].amount_token_a)
        self.assertEqual(sent_amount_zgas, mint_events[0].amount_token_b)

        self.assertEqual(total_supply_before + liquidity, total_supply_after)
        self.assertEqual(balance_user_amm_before + liquidity, balance_user_amm_after)
        self.assertEqual(reserves_before[0] + sent_amount_zneo, reserves_after[0])
        self.assertEqual(reserves_before[1] + sent_amount_zgas, reserves_after[1])
        self.assertEqual(balance_user_zneo_before - sent_amount_zneo, balance_user_zneo_after)
        self.assertEqual(balance_user_zgas_before - sent_amount_zgas, balance_user_zgas_after)
        self.assertEqual(reserves_before[0], balance_amm_zneo_before)
        self.assertEqual(reserves_before[1], balance_amm_zgas_before)
        self.assertEqual(reserves_after[0], balance_amm_zneo_after)
        self.assertEqual(reserves_after[1], balance_amm_zgas_after)

        transferred_amount_zneo = 2
        transferred_amount_zgas = 23 * 10 ** 8

        # approving the AMM contract, so that it will be able to transfer zNEO from account
        result, _ = await self.call('approve',
                                    [account, amm, transferred_amount_zneo],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_neo,
                                    return_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from account
        result, _ = await self.call('approve',
                                    [account, amm, transferred_amount_zgas],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_gas,
                                    return_type=bool)
        self.assertEqual(True, result)

        # saving data to demonstrate that the value will change later
        total_supply_before, _ = await self.call('totalSupply', [], return_type=int)
        reserves_before, _ = await self.call('get_reserves', [], return_type=list[int])

        # adding liquidity to the pool will give you AMM tokens in return
        result, notifications = await self.call('add_liquidity',
                                                [transferred_amount_zneo, transferred_amount_zgas, 0, 0, account],
                                                signing_accounts=[self.account1],
                                                return_type=list[int])

        # since there are tokens in the pool already, liquidity will be calculated as follows
        liquidity, sent_amount_zneo, sent_amount_zgas = await self.calculate_add_liquidity(transferred_amount_zneo, transferred_amount_zgas)
        self.assertEqual([sent_amount_zneo, sent_amount_zgas, liquidity], result)

        # zGAS will be quoted to keep the same ratio between zNEO and zGAS, the current ratio is 1 NEO to 11 GAS,
        # therefore, if 2 NEO are being added to the AMM, 22 GAS will be added instead of 23
        transferred_amount_zgas_quoted = transferred_amount_zneo * reserves_before[1] // reserves_before[0]
        self.assertEqual(sent_amount_zgas, transferred_amount_zgas_quoted)

        transfer_events = self.filter_events(notifications,
                                             origin=amm,
                                             event_name='Transfer',
                                             notification_type=boatestcase.Nep17TransferEvent
                                             )
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(None, transfer_events[0].source)
        self.assertEqual(account, transfer_events[0].destination)
        self.assertEqual(liquidity, transfer_events[0].amount)

        sync_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Sync',
                                         notification_type=SyncEvent
                                         )
        self.assertEqual(1, len(sync_events))
        self.assertEqual(reserves_before[0] + sent_amount_zneo, sync_events[0].reserve_token_a)
        self.assertEqual(reserves_before[1] + sent_amount_zgas, sync_events[0].reserve_token_b)

        mint_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Mint',
                                         notification_type=BurnOrMintEvent
                                         )
        self.assertEqual(1, len(mint_events))
        self.assertEqual(account, mint_events[0].sender)
        self.assertEqual(sent_amount_zneo, mint_events[0].amount_token_a)
        self.assertEqual(sent_amount_zgas, mint_events[0].amount_token_b)

    async def calculate_add_liquidity(self, amount_a: int, amount_b: int) -> tuple[int, int, int]:
        import math
        total_supply, _ = await self.call('totalSupply', [], return_type=int)
        reserves, _ = await self.call('get_reserves', [], return_type=list[int])

        if total_supply == 0:
            liquidity = int(math.sqrt(amount_a * amount_b))
        else:
            token_b_quoted, _ = await self.call('quote',
                                                [amount_a, reserves[0], reserves[1]],
                                                return_type=int)
            if token_b_quoted <= amount_b:
                amount_b = token_b_quoted
            else:
                token_a_quoted, _ = await self.call('quote',
                                                    [amount_b, reserves[1], reserves[0]],
                                                    return_type=int)
                amount_a = token_a_quoted
            liquidity = min(amount_a * total_supply // reserves[0], amount_b * total_supply // reserves[1])

        return liquidity, amount_a, amount_b

    async def calculate_remove_liquidity(self, liquidity: int) -> list[int]:
        total_supply, _ = await self.call('totalSupply', [], return_type=int)
        reserves, _ = await self.call('get_reserves', [], return_type=list[int])

        return [liquidity * reserves[0] // total_supply, liquidity * reserves[1] // total_supply]

    async def test_remove_liquidity(self):
        test_balance_zneo = 1_000
        test_balance_zgas = 1_000 * 10 ** 8
        transferred_amount_zneo = 10
        transferred_amount_zgas = 110 * 10 ** 8

        account = self.account2.script_hash
        amm = self.contract.hash

        # set_address is conflicting with other tests
        await self.set_address()

        # can't remove liquidity, because the user doesn't have any
        with self.assertRaises(boatestcase.AssertException):
            await self.call('remove_liquidity',
                            [10000, 0, 0, account],
                            signing_accounts=[self.account2],
                            return_type=list[int])

        # minting zNEO to account
        result, _ = await self.call('transfer',
                                    [account, self.z_neo, test_balance_zneo, None],
                                    signing_accounts=[self.account2],
                                    target_contract=constants.NEO_SCRIPT,
                                    return_type=bool)
        self.assertEqual(True, result)

        # minting zGAS to account
        result, _ = await self.call('transfer',
                                    [account, self.z_gas, test_balance_zgas, None],
                                    signing_accounts=[self.account2],
                                    target_contract=constants.GAS_SCRIPT,
                                    return_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zNEO from account
        result, _ = await self.call('approve',
                                    [account, amm, test_balance_zneo],
                                    signing_accounts=[self.account2],
                                    target_contract=self.z_neo,
                                    return_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from account
        result, _ = await self.call('approve',
                                    [account, amm, test_balance_zgas],
                                    signing_accounts=[self.account2],
                                    target_contract=self.z_gas,
                                    return_type=bool)
        self.assertEqual(True, result)

        total_supply_before, _ = await self.call('totalSupply', [], return_type=int)
        reserves_before, _ = await self.call('get_reserves', [], return_type=list[int])

        # adding liquidity to the pool will give you AMM tokens in return
        liquidity, sent_amount_zneo, sent_amount_zgas = await self.calculate_add_liquidity(transferred_amount_zneo, transferred_amount_zgas)

        result, notifications = await self.call('add_liquidity',
                                                [transferred_amount_zneo, transferred_amount_zgas, 0, 0, account],
                                                signing_accounts=[self.account2],
                                                return_type=list[int])
        self.assertEqual([sent_amount_zneo, sent_amount_zgas, liquidity], result)

        # saving data to demonstrate that the value will change later
        total_supply_before, _ = await self.call('totalSupply', [], return_type=int)
        balance_user_before, _ = await self.call('balanceOf', [account], return_type=int)
        reserves_before, _ = await self.call('get_reserves', [], return_type=list[int])
        balance_user_zneo_before, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_neo)
        balance_user_zgas_before, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_gas)
        balance_amm_zneo_before, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_neo)
        balance_amm_zgas_before, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_gas)

        # removing liquidity from the pool will return the equivalent zNEO and zGAS that were used to fund the pool
        zneo_received, zgas_received = await self.calculate_remove_liquidity(liquidity)
        result, notifications = await self.call('remove_liquidity',
                                    [liquidity, 0, 0, account],
                                    signing_accounts=[self.account2],
                                    return_type=list[int])
        self.assertEqual([zneo_received, zgas_received], result)

        # data that will be compared with the previously saved data
        total_supply_after, _ = await self.call('totalSupply', [], return_type=int)
        balance_user_after, _ = await self.call('balanceOf', [account], return_type=int)
        reserves_after, _ = await self.call('get_reserves', [], return_type=list[int])
        balance_user_zneo_after, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_neo)
        balance_user_zgas_after, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_gas)
        balance_amm_zneo_after, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_neo)
        balance_amm_zgas_after, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_gas)

        transfer_events = self.filter_events(notifications,
                                             origin=amm,
                                             event_name='Transfer',
                                             notification_type=boatestcase.Nep17TransferEvent
                                             )
        # add_liquidity sent a Transfer event and remove_liquidity sent another
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(account, transfer_events[0].source)
        self.assertEqual(None, transfer_events[0].destination)
        self.assertEqual(liquidity, transfer_events[0].amount)

        sync_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Sync',
                                         notification_type=SyncEvent
                                         )
        self.assertEqual(1, len(sync_events))
        self.assertEqual(reserves_before[0] - zneo_received, sync_events[0].reserve_token_a)
        self.assertEqual(reserves_before[1] - zgas_received, sync_events[0].reserve_token_b)

        burn_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Burn',
                                         notification_type=BurnOrMintEvent
                                         )
        self.assertEqual(1, len(burn_events))
        self.assertEqual(account, burn_events[0].sender)
        self.assertEqual(zneo_received, burn_events[0].amount_token_a)
        self.assertEqual(zgas_received, burn_events[0].amount_token_b)

        self.assertEqual(total_supply_before - liquidity, total_supply_after)
        self.assertEqual(balance_user_before - liquidity, balance_user_after)
        self.assertEqual(reserves_before[0] - zneo_received, reserves_after[0])
        self.assertEqual(reserves_before[1] - zgas_received, reserves_after[1])
        self.assertEqual(balance_user_zneo_before + zneo_received, balance_user_zneo_after)
        self.assertEqual(balance_user_zgas_before + zgas_received, balance_user_zgas_after)
        self.assertEqual(reserves_before[0], balance_amm_zneo_before)
        self.assertEqual(reserves_before[1], balance_amm_zgas_before)
        self.assertEqual(reserves_after[0], balance_amm_zneo_after)
        self.assertEqual(reserves_after[1], balance_amm_zgas_after)

    async def test_swap_zneo_to_zgas(self):
        test_balance_zneo = 1_000
        test_balance_zgas = 1_000 * 10 ** 8
        transferred_amount_zneo = 10
        transferred_amount_zgas = 110 * 10 ** 8

        account = self.account1.script_hash
        amm = self.contract.hash

        # set_address is conflicting with other tests
        await self.set_address()

        # minting zNEO to account
        result, _ = await self.call('transfer',
                                    [account, self.z_neo, test_balance_zneo, None],
                                    signing_accounts=[self.account1],
                                    target_contract=constants.NEO_SCRIPT,
                                    return_type=bool)
        self.assertEqual(True, result)

        # minting zGAS to account
        result, _ = await self.call('transfer',
                                    [account, self.z_gas, test_balance_zgas, None],
                                    signing_accounts=[self.account1],
                                    target_contract=constants.GAS_SCRIPT,
                                    return_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zNEO from account
        result, _ = await self.call('approve',
                                    [account, amm, transferred_amount_zneo],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_neo,
                                    return_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from account
        result, _ = await self.call('approve',
                                    [account, amm, transferred_amount_zgas],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_gas,
                                    return_type=bool)
        self.assertEqual(True, result)

        # adding liquidity to the pool will give you AMM tokens in return
        liquidity, sent_amount_zneo, sent_amount_zgas = await self.calculate_add_liquidity(transferred_amount_zneo, transferred_amount_zgas)
        result, notifications = await self.call('add_liquidity',
                                                [transferred_amount_zneo, transferred_amount_zgas, 0, 0, account],
                                                signing_accounts=[self.account1],
                                                return_type=list[int])
        self.assertEqual([sent_amount_zneo, sent_amount_zgas, liquidity], result)

        swapped_zneo = 1

        # won't work, because user did not have enough zNEO tokens
        with self.assertRaises(boatestcase.AssertException):
            await self.call('swap_tokens',
                            [swapped_zneo, 0, self.z_neo, account],
                            signing_accounts=[self.account1],
                            return_type=int)

        # approving the AMM contract, so that it will be able to transfer zNEO from account
        result, _ = await self.call('approve',
                                    [account, amm, swapped_zneo],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_neo,
                                    return_type=bool)
        self.assertEqual(True, result)

        # saving data to demonstrate that the value will change later
        total_supply_before, _ = await self.call('totalSupply', [], return_type=int)
        reserves_before, _ = await self.call('get_reserves', [], return_type=list[int])
        balance_user_zneo_before, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_neo)
        balance_user_zgas_before, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_gas)
        balance_amm_zneo_before, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_neo)
        balance_amm_zgas_before, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_gas)

        # swapping zneo for zgas
        result, notifications = await self.call('swap_tokens',
                                                [swapped_zneo, 0, self.z_neo, account],
                                                signing_accounts=[self.account1],
                                                return_type=int)
        # there is a 0.3% fee when doing a swap
        swapped_zneo_with_fee = swapped_zneo * (1000 - 3)
        swapped_zgas = swapped_zneo_with_fee * reserves_before[1] // (reserves_before[0] * 1000 + swapped_zneo_with_fee)
        self.assertEqual(swapped_zgas, result)

        # data that will be compared with the previously saved data
        total_supply_after, _ = await self.call('totalSupply', [], return_type=int)
        reserves_after, _ = await self.call('get_reserves', [], return_type=list[int])
        balance_user_zneo_after, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_neo)
        balance_user_zgas_after, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_gas)
        balance_amm_zneo_after, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_neo)
        balance_amm_zgas_after, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_gas)

        sync_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Sync',
                                         notification_type=SyncEvent
                                         )
        self.assertEqual(1, len(sync_events))
        self.assertEqual(reserves_before[0] + swapped_zneo, sync_events[0].reserve_token_a)
        self.assertEqual(reserves_before[1] - swapped_zgas, sync_events[0].reserve_token_b)

        swap_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Swap',
                                         notification_type=SwapEvent
                                         )
        self.assertEqual(1, len(swap_events))
        self.assertEqual(account, swap_events[0].sender)
        self.assertEqual(swapped_zneo, swap_events[0].amount_token_a_in)
        self.assertEqual(0, swap_events[0].amount_token_b_in)
        self.assertEqual(0, swap_events[0].amount_token_a_out)
        self.assertEqual(swapped_zgas, swap_events[0].amount_token_b_out)

        self.assertEqual(total_supply_before, total_supply_after)
        self.assertEqual(reserves_before[0] + swapped_zneo, reserves_after[0])
        self.assertEqual(reserves_before[1] - swapped_zgas, reserves_after[1])
        self.assertEqual(balance_user_zneo_before - swapped_zneo, balance_user_zneo_after)
        self.assertEqual(balance_user_zgas_before + swapped_zgas, balance_user_zgas_after)
        self.assertEqual(reserves_before[0], balance_amm_zneo_before)
        self.assertEqual(reserves_before[1], balance_amm_zgas_before)
        self.assertEqual(reserves_after[0], balance_amm_zneo_after)
        self.assertEqual(reserves_after[1], balance_amm_zgas_after)
        self.assertEqual(reserves_before[0] + swapped_zneo, reserves_after[0])
        self.assertEqual(reserves_before[1] - swapped_zgas, reserves_after[1])

    async def test_swap_zgas_to_zneo(self):
        test_balance_zneo = 1_000
        test_balance_zgas = 1_000 * 10 ** 8
        transferred_amount_zneo = 100
        transferred_amount_zgas = 110 * 10 ** 8

        account = self.account1.script_hash
        amm = self.contract.hash

        # set_address is conflicting with other tests
        await self.set_address()

        # minting zNEO to account
        result, _ = await self.call('transfer',
                                    [account, self.z_neo, test_balance_zneo, None],
                                    signing_accounts=[self.account1],
                                    target_contract=constants.NEO_SCRIPT,
                                    return_type=bool)
        self.assertEqual(True, result)

        # minting zGAS to account
        result, _ = await self.call('transfer',
                                    [account, self.z_gas, test_balance_zgas, None],
                                    signing_accounts=[self.account1],
                                    target_contract=constants.GAS_SCRIPT,
                                    return_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zNEO from account
        result, _ = await self.call('approve',
                                    [account, amm, test_balance_zneo],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_neo,
                                    return_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from account
        result, _ = await self.call('approve',
                                    [account, amm, test_balance_zgas],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_gas,
                                    return_type=bool)
        self.assertEqual(True, result)

        # adding liquidity to the pool will give you AMM tokens in return
        liquidity, sent_amount_zneo, sent_amount_zgas = await self.calculate_add_liquidity(transferred_amount_zneo, transferred_amount_zgas)
        result, notifications = await self.call('add_liquidity',
                                                [transferred_amount_zneo, transferred_amount_zgas, 0, 0, account],
                                                signing_accounts=[self.account1],
                                                return_type=list[int])
        self.assertEqual([sent_amount_zneo, sent_amount_zgas, liquidity], result)

        swapped_zgas = 11 * 10 ** 8

        # won't work, because user did not enough zGAS tokens
        with self.assertRaises(boatestcase.AssertException):
            await self.call('swap_tokens',
                            [swapped_zgas, 0, self.z_neo, account],
                            signing_accounts=[self.account1],
                            return_type=int)

        # approving the AMM contract, so that it will be able to transfer zGAS from account
        result, _ = await self.call('approve',
                                    [account, amm, swapped_zgas],
                                    signing_accounts=[self.account1],
                                    target_contract=self.z_gas,
                                    return_type=bool)
        self.assertEqual(True, result)

        # saving data to demonstrate that the value will change later
        total_supply_before, _ = await self.call('totalSupply', [], return_type=int)
        reserves_before, _ = await self.call('get_reserves', [], return_type=list[int])
        balance_user_zneo_before, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_neo)
        balance_user_zgas_before, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_gas)
        balance_amm_zneo_before, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_neo)
        balance_amm_zgas_before, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_gas)

        # swapping zgas for zneo
        result, notifications = await self.call('swap_tokens',
                                                [swapped_zgas, 0, self.z_gas, account],
                                                signing_accounts=[self.account1],
                                                return_type=int)
        # there is a 0.3% fee when doing a swap
        swapped_zgas_with_fee = swapped_zgas * (1000 - 3)
        swapped_zneo = swapped_zgas_with_fee * reserves_before[0] // (reserves_before[1] * 1000 + swapped_zgas_with_fee)
        self.assertEqual(swapped_zneo, result)

        # data that will be compared with the previously saved data
        total_supply_after, _ = await self.call('totalSupply', [], return_type=int)
        reserves_after, _ = await self.call('get_reserves', [], return_type=list[int])
        balance_user_zneo_after, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_neo)
        balance_user_zgas_after, _ = await self.call('balanceOf', [account], return_type=int, target_contract=self.z_gas)
        balance_amm_zneo_after, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_neo)
        balance_amm_zgas_after, _ = await self.call('balanceOf', [amm], return_type=int, target_contract=self.z_gas)

        # add_liquidity sent a Sync before
        sync_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Sync',
                                         notification_type=SyncEvent
                                         )
        self.assertEqual(1, len(sync_events))
        self.assertEqual(reserves_before[0] - swapped_zneo, sync_events[0].reserve_token_a)
        self.assertEqual(reserves_before[1] + swapped_zgas, sync_events[0].reserve_token_b)

        swap_events = self.filter_events(notifications,
                                         origin=amm,
                                         event_name='Swap',
                                         notification_type=SwapEvent
                                         )
        self.assertEqual(1, len(swap_events))
        self.assertEqual(account, swap_events[0].sender)
        self.assertEqual(0, swap_events[0].amount_token_a_in)
        self.assertEqual(swapped_zgas, swap_events[0].amount_token_b_in)
        self.assertEqual(swapped_zneo, swap_events[0].amount_token_a_out)
        self.assertEqual(0, swap_events[0].amount_token_b_out)

        self.assertEqual(total_supply_before, total_supply_after)
        self.assertEqual(reserves_before[0] - swapped_zneo, reserves_after[0])
        self.assertEqual(reserves_before[1] + swapped_zgas, reserves_after[1])
        self.assertEqual(balance_user_zneo_before + swapped_zneo, balance_user_zneo_after)
        self.assertEqual(balance_user_zgas_before - swapped_zgas, balance_user_zgas_after)
        self.assertEqual(reserves_before[0], balance_amm_zneo_before)
        self.assertEqual(reserves_before[1], balance_amm_zgas_before)
        self.assertEqual(reserves_after[0], balance_amm_zneo_after)
        self.assertEqual(reserves_after[1], balance_amm_zgas_after)
        self.assertEqual(reserves_before[0] - swapped_zneo, reserves_after[0])
        self.assertEqual(reserves_before[1] + swapped_zgas, reserves_after[1])
