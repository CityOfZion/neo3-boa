from boa3_test.tests import boatestcase


class TestContractInterface(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/nep17_contract_interface_test'

    async def test_balance_of(self):
        await self.set_up_contract('Nep17BalanceOf.py')

        genesis = self.genesis.script_hash

        expected_result = 10 ** 8
        balance_of_result, _ = await self.call('main', [genesis], return_type=int)
        self.assertEqual(expected_result, balance_of_result)

    async def test_decimals(self):
        await self.set_up_contract('Nep17Decimals.py')

        expected_result = 0
        decimals_result, _ = await self.call('main', return_type=int)
        self.assertEqual(expected_result, decimals_result)

    async def test_symbol(self):
        await self.set_up_contract('Nep17Symbol.py')

        expected_result = 'NEO'
        symbol_result, _ = await self.call('main', return_type=str)
        self.assertEqual(expected_result, symbol_result)

    async def test_total_supply(self):
        await self.set_up_contract('Nep17TotalSupply.py')

        expected_result = 10 ** 8
        total_supply_result, _ = await self.call('main', return_type=int)
        self.assertEqual(expected_result, total_supply_result)

    async def test_transfer(self):
        await self.set_up_contract('Nep17Transfer.py')

        genesis = self.genesis.script_hash

        # TODO: Methods and contract hash are not being added to the contract permissions yet #86drpncxa
        with self.assertRaises(boatestcase.FaultException) as context:
            expected_result = False
            transfer_result, _ = await self.call('main', [genesis, genesis, -1], return_type=bool)
            self.assertEqual(expected_result, transfer_result)

        self.assertRegex(str(context.exception), 'disallowed method call')
