from boa3 import constants
from boa3.neo import to_script_hash
from boa3.neo.cryptography import hash160
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNEP11Template(BoaTest):
    default_folder: str = 'examples'

    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')

    def test_nep11_compile(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-11', manifest['supportedstandards'])

    def test_nep11_symbol(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'symbol')
        self.assertEqual('NEP11', result)

    def test_nep11_decimals(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'decimals')
        self.assertEqual(0, result)

    def test_nep11_total_supply(self):
        # smart contract deploys with zero tokens minted
        total_supply = 0

        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(total_supply, result)

    def test_nep11_mint(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        engine.add_contract(path.replace('.py', '.nef'))

        output, manifest = self.get_output(path)
        nep11_address = hash160(output)

        aux_path = self.get_contract_path('examples/auxiliary_contracts', 'auxiliary_contract.py')
        output, manifest = self.get_output(aux_path)
        aux_address = hash160(output)

        # can't call the mint function directly
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'mint', aux_address, 100)

        gas_used = 2 * 10 ** 8
        engine.add_gas(aux_address, gas_used)

        # transferring GAS to the nep11 will mint some tokens
        result = self.run_smart_contract(engine, aux_path, 'calling_transfer', constants.GAS_SCRIPT,
                                         aux_address, nep11_address, gas_used, None,
                                         signer_accounts=[aux_address])
        self.assertEqual(True, result)

    def test_nep11_total_balance_of(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        engine.add_contract(path.replace('.py', '.nef'))

        output, manifest = self.get_output(path)
        nep11_address = hash160(output)

        aux_path = self.get_contract_path('examples/auxiliary_contracts', 'auxiliary_contract.py')
        output, manifest = self.get_output(aux_path)
        aux_address = hash160(output)

        # every account starts with zero tokens
        result = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        self.assertEqual(0, result)

        gas_used = 2 * 10 ** 8
        engine.add_gas(aux_address, gas_used)

        # transferring GAS to the nep11 will mint some tokens
        result = self.run_smart_contract(engine, aux_path, 'calling_transfer', constants.GAS_SCRIPT,
                                         aux_address, nep11_address, gas_used, None,
                                         signer_accounts=[aux_address])
        self.assertEqual(True, result)

        # after minting 1 token, the amount of tokens should increment by 1
        result = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        self.assertEqual(1, result)

        gas_used = 6 * 10 ** 8
        engine.add_gas(aux_address, gas_used)

        # minting another 3 nfts
        result = self.run_smart_contract(engine, aux_path, 'calling_transfer', constants.GAS_SCRIPT,
                                         aux_address, nep11_address, gas_used, None,
                                         signer_accounts=[aux_address])
        self.assertEqual(True, result)

        # checking if the amount is 4 now
        result = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        self.assertEqual(4, result)

        # should fail when the script length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(10))
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(30))

    def test_nep11_total_tokens_of(self):
        # TODO: Implement this test on issue #855
        pass

    def test_nep11_total_owner_of(self):
        # TODO: Implement this test on issue #855
        pass

    def test_nep11_total_transfer(self):
        # TODO: Implement this test on issue #855
        pass
