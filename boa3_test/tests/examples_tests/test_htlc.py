import asyncio

from neo3.contracts.contract import CONTRACT_HASHES
from neo3.wallet import account

from boa3.internal import constants
from boa3.internal.neo.cryptography import hash160


from boa3_test.tests import boatestcase


class TestHTLCTemplate(boatestcase.BoaTestCase):
    default_folder: str = 'examples'

    owner: account.Account
    account1: account.Account
    account2: account.Account

    REFUND_WAIT_TIME = 7     # smart contract constant in seconds

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
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 1000)
        await cls.transfer(CONTRACT_HASHES.NEO_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 100)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account2.script_hash, 1000)

        await cls.set_up_contract('htlc.py', signing_account=cls.owner)

    async def wait_refund_time(self):
        await asyncio.sleep(self.REFUND_WAIT_TIME)

    def test_htlc_compile(self):
        path = self.get_contract_path('htlc.py')
        self.assertCompile(path)

    async def test_htlc_on_nep17_payment_fail_amount(self):
        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 100 * 10 ** 8
        person_a = self.account1.script_hash
        person_b = self.account2.script_hash
        secret_hash = hash160(b'unit test')
        htlc = self.contract.hash

        result, _ = await self.call('atomic_swap',
                                    [person_a, constants.NEO_SCRIPT, transferred_amount_neo,
                                     person_b, constants.GAS_SCRIPT, transferred_amount_gas,
                                     secret_hash],
                                    return_type=bool,
                                    signing_accounts=[self.owner])
        self.assertEqual(True, result)

        # transfer won't be accepted, because amount is wrong
        with self.assertRaises(boatestcase.AbortException):
            await self.call('transfer',
                            [person_a, htlc, transferred_amount_neo + 1, None],
                            signing_accounts=[self.account1],
                            return_type=bool,
                            target_contract=constants.NEO_SCRIPT)

        with self.assertRaises(boatestcase.AbortException):
            await self.call('transfer',
                            [person_b, htlc, transferred_amount_gas - 1, None],
                            signing_accounts=[self.account2],
                            return_type=bool,
                            target_contract=constants.GAS_SCRIPT)

        await self.wait_refund_time()
        # will be able to refund, because enough time has passed
        invoke_refund_success, notifications = await self.call('refund', [], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, invoke_refund_success)

    async def test_htlc_on_nep17_payment(self):
        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 100 * 10 ** 8

        account1 = self.account1.script_hash
        account2 = self.account2.script_hash
        htlc = self.contract.hash
        secret_hash = hash160(b'unit test')

        # starting atomic swap
        result, _ = await self.call('atomic_swap',
                                    [account1, constants.NEO_SCRIPT, transferred_amount_neo,
                                     account2, constants.GAS_SCRIPT, transferred_amount_gas,
                                     secret_hash],
                                    return_type=bool,
                                    signing_accounts=[self.owner])
        self.assertEqual(True, result)

        # saving the NEO balance to compare after the transfer
        balance_neo_receiver_before, _ = await self.call('balanceOf', [htlc], return_type=int, target_contract=constants.NEO_SCRIPT)

        # this transfer will be accepted
        result, _ = await self.call('transfer',
                                    [account1, htlc, transferred_amount_neo, None],
                                    signing_accounts=[self.account1],
                                    return_type=bool,
                                    target_contract=constants.NEO_SCRIPT)
        self.assertEqual(True, result)

        # saving the NEO balance after to compare with the balance before the transfer
        balance_neo_receiver_after, _ = await self.call('balanceOf', [htlc], return_type=int, target_contract=constants.NEO_SCRIPT)
        self.assertEqual(balance_neo_receiver_before + transferred_amount_neo, balance_neo_receiver_after)

        # saving the balance GAS to compare after the transfer
        balance_gas_receiver_before, _ = await self.call('balanceOf', [htlc], return_type=int, target_contract=constants.GAS_SCRIPT)

        # this transfer will be accepted
        result, _ = await self.call('transfer',
                                    [account2, htlc, transferred_amount_gas, None],
                                    signing_accounts=[self.account2],
                                    return_type=bool,
                                    target_contract=constants.GAS_SCRIPT)
        self.assertEqual(True, result)

        # saving the balance GAS after to compare with the balance before the transfer
        balance_gas_receiver_after, _ = await self.call('balanceOf', [htlc], return_type=int, target_contract=constants.GAS_SCRIPT)
        self.assertEqual(balance_gas_receiver_before + transferred_amount_gas, balance_gas_receiver_after)

        await self.wait_refund_time()
        result, _ = await self.call('refund', [], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, result)

    async def test_htlc_withdraw(self):
        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 100 * 10 ** 8
        person_a = self.account1.script_hash
        person_b = self.account2.script_hash
        secret_hash = hash160(b'unit test')
        htlc = self.contract.hash

        # starting atomic swap by using the atomic_swap method
        result, _ = await self.call('atomic_swap',
                                    [person_a, constants.NEO_SCRIPT, transferred_amount_neo,
                                     person_b, constants.GAS_SCRIPT, transferred_amount_gas,
                                     secret_hash],
                                    return_type=bool,
                                    signing_accounts=[self.owner])
        self.assertEqual(True, result)

        # saving the balance to compare after the withdraw
        balance_neo_htlc_before, _ = await self.call('balanceOf', [htlc], return_type=int, target_contract=constants.NEO_SCRIPT)
        balance_gas_htlc_before, _ = await self.call('balanceOf', [htlc], return_type=int, target_contract=constants.GAS_SCRIPT)

        # won't be able to withdraw, because no one transferred cryptocurrency to the smart contract
        invoke_withdraw_wrong1, _ = await self.call('withdraw', [b'unit test'], signing_accounts=[self.owner], return_type=bool)
        self.assertEqual(False, invoke_withdraw_wrong1)

        invoke_transfer_person_a, _ = await self.call('transfer',
                                                      [person_a, htlc, transferred_amount_neo, None],
                                                      signing_accounts=[self.account1],
                                                      return_type=bool,
                                                      target_contract=constants.NEO_SCRIPT)
        self.assertEqual(True, result)

        invoke_transfer_person_b, _ = await self.call('transfer',
                                                      [person_b, htlc, transferred_amount_gas, None],
                                                      signing_accounts=[self.account2],
                                                      return_type=bool,
                                                      target_contract=constants.GAS_SCRIPT)
        self.assertEqual(True, result)

        # the withdraw will fail, because the secret is wrong
        invoke_withdraw_wrong2, _ = await self.call('withdraw', [b'wrong'], signing_accounts=[self.owner], return_type=bool)
        self.assertEqual(False, invoke_withdraw_wrong2)

        # the withdraw will occur
        invoke_withdraw_right, notifications = await self.call('withdraw', [b'unit test'], signing_accounts=[self.owner], return_type=bool)
        self.assertEqual(True, invoke_withdraw_right)

        # saving the balance after to compare with the balance before the transfer
        balance_neo_htlc_after, _ = await self.call('balanceOf', [htlc], return_type=int, target_contract=constants.NEO_SCRIPT)
        balance_gas_htlc_after, _ = await self.call('balanceOf', [htlc], return_type=int, target_contract=constants.GAS_SCRIPT)

        # the transfer were accepted so they were registered
        transfer_events = self.filter_events(
            notifications,
            event_name='Transfer',
            notification_type=boatestcase.Nep17TransferEvent
        )
        self.assertEqual(3, len(transfer_events))

        gas_transfer_event = transfer_events[0]
        self.assertEqual(htlc, gas_transfer_event.source)
        self.assertEqual(person_a, gas_transfer_event.destination)
        self.assertEqual(transferred_amount_gas, gas_transfer_event.amount)

        neo_transfer_event = transfer_events[1]
        self.assertEqual(htlc, neo_transfer_event.source)
        self.assertEqual(person_b, neo_transfer_event.destination)
        self.assertEqual(transferred_amount_neo, neo_transfer_event.amount)

        gas_mint_event = transfer_events[2]
        self.assertEqual(None, gas_mint_event.source)
        self.assertEqual(htlc, gas_mint_event.destination)
        self.assertGreater(gas_mint_event.amount, 0)

        self.assertEqual(balance_neo_htlc_before, balance_neo_htlc_after)
        self.assertEqual(balance_gas_htlc_before + gas_mint_event.amount, balance_gas_htlc_after)

    async def test_htlc_refund_zero_transfers(self):
        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 100 * 10 ** 8
        person_a = self.account1.script_hash
        person_b = self.account2.script_hash
        secret_hash = hash160(b'unit test')

        result, _ = await self.call('atomic_swap',
                                    [person_a, constants.NEO_SCRIPT, transferred_amount_neo,
                                     person_b, constants.GAS_SCRIPT, transferred_amount_gas,
                                     secret_hash],
                                    return_type=bool,
                                    signing_accounts=[self.owner])
        self.assertEqual(True, result)

        # won't be able to refund, because not enough time has passed
        invoke_refund_fail, _ = await self.call('refund', [], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(False, invoke_refund_fail)

        await self.wait_refund_time()
        # will be able to refund, because enough time has passed
        invoke_refund_success, _ = await self.call('refund', [], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, invoke_refund_success)

    async def test_htlc_refund_one_transfer(self):
        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 100 * 10 ** 8
        person_a = self.account1.script_hash
        person_b = self.account2.script_hash
        secret_hash = hash160(b'unit test')
        htlc = self.contract.hash

        result, _ = await self.call('atomic_swap',
                                    [person_a, constants.NEO_SCRIPT, transferred_amount_neo,
                                     person_b, constants.GAS_SCRIPT, transferred_amount_gas,
                                     secret_hash],
                                    return_type=bool,
                                    signing_accounts=[self.owner])
        self.assertEqual(True, result)

        result, _ = await self.call('transfer',
                                    [person_a, htlc, transferred_amount_neo, None],
                                    signing_accounts=[self.account1],
                                    return_type=bool,
                                    target_contract=constants.NEO_SCRIPT)
        self.assertEqual(True, result)

        await self.wait_refund_time()
        # will be able to refund, because enough time has passed
        invoke_refund_success, notifications = await self.call('refund', [], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, invoke_refund_success)

        # person_a transferred cryptocurrency to the contract, so only he will be refunded
        transfer_events = self.filter_events(
            notifications,
            event_name='Transfer',
            notification_type=boatestcase.Nep17TransferEvent
        )
        filtered_transfer_events = list(filter(lambda x: x.source is not None, transfer_events))
        self.assertEqual(1, len(filtered_transfer_events))
        self.assertEqual(htlc, filtered_transfer_events[0].source)
        self.assertEqual(person_a, filtered_transfer_events[0].destination)
        self.assertEqual(transferred_amount_neo, filtered_transfer_events[0].amount)

    async def test_htlc_refund_two_transfers(self):
        transferred_amount_neo = 10 * 10 ** 0
        transferred_amount_gas = 100 * 10 ** 8
        person_a = self.account1.script_hash
        person_b = self.account2.script_hash
        secret_hash = hash160(b'unit test')
        htlc = self.contract.hash

        result, _ = await self.call('atomic_swap',
                                    [person_a, constants.NEO_SCRIPT, transferred_amount_neo,
                                     person_b, constants.GAS_SCRIPT, transferred_amount_gas,
                                     secret_hash],
                                    return_type=bool,
                                    signing_accounts=[self.owner])
        self.assertEqual(True, result)

        result, _ = await self.call('transfer',
                                    [person_a, htlc, transferred_amount_neo, None],
                                    signing_accounts=[self.account1],
                                    return_type=bool,
                                    target_contract=constants.NEO_SCRIPT)
        self.assertEqual(True, result)
        result, _ = await self.call('transfer',
                                    [person_b, htlc, transferred_amount_gas, None],
                                    signing_accounts=[self.account2],
                                    return_type=bool,
                                    target_contract=constants.GAS_SCRIPT)
        self.assertEqual(True, result)

        await self.wait_refund_time()
        # will be able to refund, because enough time has passed
        invoke_refund_success, notifications = await self.call('refund', [], return_type=bool, signing_accounts=[self.owner])
        self.assertEqual(True, invoke_refund_success)

        # person_a and person_b transferred cryptocurrency to the contract, so they both will be refunded
        transfer_events = self.filter_events(
            notifications,
            event_name='Transfer',
            notification_type=boatestcase.Nep17TransferEvent
        )
        filtered_transfer_events = list(filter(lambda x: x.source is not None, transfer_events))
        self.assertEqual(2, len(filtered_transfer_events))
        refund_a, refund_b = filtered_transfer_events

        # HTLC returning the tokens
        self.assertEqual(htlc, refund_a.source)
        self.assertEqual(person_a, refund_a.destination)
        self.assertEqual(transferred_amount_neo, refund_a.amount)

        self.assertEqual(htlc, refund_b.source)
        self.assertEqual(person_b, refund_b.destination)
        self.assertEqual(transferred_amount_gas, refund_b.amount)
