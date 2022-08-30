import json
from typing import Dict, List

from boa3.neo import to_script_hash
from boa3.neo.vm.type.String import String
from boa3.neo3.core.types import UInt160
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNEP11Template(BoaTest):
    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = to_script_hash(b'NZcuGiwRu1QscpmCyxj5XwQBUf6sk7dJJN')
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = to_script_hash(b'NNLi44dJNXtDNSBkofB48aTVYtb1zZrNEs')

    TOKEN_META = bytes(
        '{ "name": "NEP11", "description": "Some description", "image": "{some image URI}", "tokenURI": "{some URI}" }',
        'utf-8')
    TOKEN_LOCKED = bytes('lockedContent', 'utf-8')
    ROYALTIES = bytes(
        '[{"address": "NZcuGiwRu1QscpmCyxj5XwQBUf6sk7dJJN", "value": 2000}, '
        '{"address": "NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB", "value": 3000}]',
        'utf-8')

    def deploy_contract(self, engine, path):
        engine.add_signer_account(self.OWNER_SCRIPT_HASH)
        self.run_smart_contract(engine, path, '_deploy', self.OWNER_SCRIPT_HASH, False,
                                signer_accounts=[self.OWNER_SCRIPT_HASH],
                                expected_result_type=bool)

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
        self.deploy_contract(engine, path)
        result = self.run_smart_contract(engine, path, 'symbol')
        self.assertEqual('EXMP', result)

    def test_nep11_decimals(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)
        result = self.run_smart_contract(engine, path, 'decimals')
        self.assertEqual(0, result)

    def test_nep11_total_supply(self):
        # smart contract deploys with zero tokens minted
        total_supply = 0

        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)
        result = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(total_supply, result)

    def test_nep11_deploy(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)
        # contract is already deployed

        result = self.run_smart_contract(engine, path, '_deploy', None, False,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertIsVoid(result)
        # contract was deployed only once
        self.assertEqual(1, len([notification for notification in engine.notifications if notification.name == "Deploy"]))

    def test_nep11_update(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        new_nef, new_manifest = self.get_bytes_output(path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        # update contract
        result = self.run_smart_contract(engine, path, 'update',
                                         new_nef, arg_manifest,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertIsVoid(result)

    def test_nep11_destroy(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        # destroy contract
        result = self.run_smart_contract(engine, path, 'destroy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertIsVoid(result)

        # should not exist anymore
        result = self.run_smart_contract(engine, path, 'symbol')
        self.assertNotEqual('', result)

    def test_nep11_verify(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        # should fail because account does not have enough for fees
        verified = self.run_smart_contract(engine, path, 'verify',
                                           signer_accounts=[self.OTHER_ACCOUNT_2],
                                           expected_result_type=bool)
        self.assertEqual(verified, False)

        addresses = self.run_smart_contract(engine, path, 'getAuthorizedAddress',
                                            expected_result_type=List[UInt160],
                                            signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(addresses[0], self.OWNER_SCRIPT_HASH)
        self.assertEqual(len(addresses), 1)

        verified = self.run_smart_contract(engine, path, 'verify',
                                           signer_accounts=[self.OTHER_ACCOUNT_1],
                                           expected_result_type=bool)
        self.assertEqual(verified, False)

        verified = self.run_smart_contract(engine, path, 'verify',
                                           signer_accounts=[self.OTHER_ACCOUNT_2],
                                           expected_result_type=bool)
        self.assertEqual(verified, False)

        verified = self.run_smart_contract(engine, path, 'verify',
                                           signer_accounts=[self.OWNER_SCRIPT_HASH],
                                           expected_result_type=bool)
        self.assertEqual(verified, True)

    def test_nep11_authorize_2(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        self.run_smart_contract(engine, path, 'setAuthorizedAddress',
                                self.OTHER_ACCOUNT_1, True,
                                signer_accounts=[self.OWNER_SCRIPT_HASH])
        auth_events = engine.get_events('Authorized')

        # check if the event was triggered and the address was authorized
        self.assertEqual(0, auth_events[0].arguments[1])
        self.assertEqual(1, auth_events[0].arguments[2])

        # now deauthorize the address
        self.run_smart_contract(engine, path, 'setAuthorizedAddress',
                                self.OTHER_ACCOUNT_1, False,
                                signer_accounts=[self.OWNER_SCRIPT_HASH])
        auth_events = engine.get_events('Authorized')
        # check if the event was triggered and the address was authorized
        self.assertEqual(0, auth_events[1].arguments[1])
        self.assertEqual(0, auth_events[1].arguments[2])

    def test_nep11_authorize(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        self.run_smart_contract(engine, path, 'setAuthorizedAddress',
                                self.OTHER_ACCOUNT_1, True,
                                signer_accounts=[self.OWNER_SCRIPT_HASH])
        auth_events = engine.get_events('Authorized')

        # check if the event was triggered and the address was authorized
        self.assertEqual(0, auth_events[0].arguments[1])
        self.assertEqual(1, auth_events[0].arguments[2])

        # now deauthorize the address
        self.run_smart_contract(engine, path, 'setAuthorizedAddress',
                                self.OTHER_ACCOUNT_1, False,
                                signer_accounts=[self.OWNER_SCRIPT_HASH])
        auth_events = engine.get_events('Authorized')
        # check if the event was triggered and the address was authorized
        self.assertEqual(0, auth_events[1].arguments[1])
        self.assertEqual(0, auth_events[1].arguments[2])

    def test_nep11_pause(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        engine.add_contract(path.replace('.py', '.nef'))

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        engine.add_gas(self.OTHER_ACCOUNT_1, add_amount)

        # pause contract
        result = self.run_smart_contract(engine, path, 'updatePause', True,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # should fail because contract is paused
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'mint',
                                    self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                    signer_accounts=[self.OTHER_ACCOUNT_1])

        # unpause contract
        result = self.run_smart_contract(engine, path, 'updatePause', False,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # mint
        result = self.run_smart_contract(engine, path, 'mint',
                                         self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                         signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual('\x01', result)

    def test_nep11_mint(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        engine.add_contract(path.replace('.py', '.nef'))

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        engine.add_gas(self.OTHER_ACCOUNT_1, add_amount)

        # should succeed now that account has enough fees
        token = self.run_smart_contract(engine, path, 'mint',
                                        self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                        signer_accounts=[self.OTHER_ACCOUNT_1])

        properties = self.run_smart_contract(engine, path, 'properties', token, expected_result_type=Dict[str, str])
        token_property = json.loads(self.TOKEN_META.decode('utf-8').replace("'", "\""))
        self.assertEqual(token_property, properties)

        royalties = self.run_smart_contract(engine, path, 'getRoyalties', token, expected_result_type=str)
        self.assertEqual(royalties, self.ROYALTIES.decode('utf-8'))

        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'properties',
                                    bytes('thisisanonexistingtoken', 'utf-8'),
                                    expected_result_type=str)

        # check balances after
        nep11_balance_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        nep11_supply_after = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(1, nep11_balance_after)
        self.assertEqual(1, nep11_supply_after)

    def test_nep11_transfer(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        engine.add_contract(path.replace('.py', '.nef'))

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        engine.add_gas(self.OTHER_ACCOUNT_1, add_amount)

        # mint
        token = self.run_smart_contract(engine, path, 'mint',
                                        self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                        signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual('\x01', token)

        # check owner before
        nep11_owner_of_before = self.run_smart_contract(engine, path, 'ownerOf', token)
        self.assertEqual(self.OTHER_ACCOUNT_1, nep11_owner_of_before)

        # transfer
        result = self.run_smart_contract(engine, path, 'transfer',
                                         self.OTHER_ACCOUNT_2, token, None,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # check owner after
        nep11_owner_of_after = self.run_smart_contract(engine, path, 'ownerOf', token)
        self.assertEqual(self.OTHER_ACCOUNT_2, nep11_owner_of_after)

        # check balances after
        nep11_balance_after_transfer = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        nep11_supply_after_transfer = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(0, nep11_balance_after_transfer)
        self.assertEqual(1, nep11_supply_after_transfer)

        # try to transfer non existing token id
        with self.assertRaisesRegex(TestExecutionException, self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'transfer',
                                    self.OTHER_ACCOUNT_2, bytes('thisisanonexistingtoken', 'utf-8'), None,
                                    signer_accounts=[self.OTHER_ACCOUNT_1])

    def test_nep11_burn(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        engine.add_contract(path.replace('.py', '.nef'))

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        engine.add_gas(self.OTHER_ACCOUNT_1, add_amount)

        # mint
        token = self.run_smart_contract(engine, path, 'mint',
                                        self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                        signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual('\x01', token)

        # burn
        burn = self.run_smart_contract(engine, path, 'burn', token,
                                       signer_accounts=[self.OTHER_ACCOUNT_1],
                                       expected_result_type=bool)
        self.assertEqual(True, burn)

        # check balances after
        nep11_balance_after = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(0, nep11_balance_after)
        nep11_supply_after = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(0, nep11_supply_after)

    def test_nep11_onNEP11Payment(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)
        engine.add_contract(path.replace('.py', '.nef'))

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        engine.add_gas(self.OTHER_ACCOUNT_1, add_amount)

        # mint
        token = self.run_smart_contract(engine, path, 'mint',
                                        self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                        signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual('\x01', token)

        # the smart contract will abort if any address calls the NEP11 onPayment method
        with self.assertRaisesRegex(TestExecutionException, self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'onNEP11Payment',
                                    self.OTHER_ACCOUNT_1, 1, token, None,
                                    signer_accounts=[self.OTHER_ACCOUNT_1])

    def test_nep11_balance_of(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        engine.add_gas(self.OTHER_ACCOUNT_1, add_amount)

        # mint
        token = self.run_smart_contract(engine, path, 'mint',
                                        self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                        signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual('\x01', token)

        # balance should be one
        amount_of_tokens = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(1, amount_of_tokens)

        # minting another token
        token = self.run_smart_contract(engine, path, 'mint',
                                        self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                        signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual('\x02', token)

        # balance should increase again
        amount_of_tokens = self.run_smart_contract(engine, path, 'balanceOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(2, amount_of_tokens)

    def test_nep11_tokens_of(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        engine = TestEngine()
        self.deploy_contract(engine, path)

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        engine.add_gas(self.OTHER_ACCOUNT_1, add_amount)

        tokens = []

        # initial tokensOf is an empty iterator
        account_tokens = self.run_smart_contract(engine, path, 'tokensOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(tokens, account_tokens)

        # mint
        token = self.run_smart_contract(engine, path, 'mint',
                                        self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                        signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual('\x01', token)

        tokens.append('\x01')

        # tokensOf should return ['\x01']
        account_tokens = self.run_smart_contract(engine, path, 'tokensOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(tokens, account_tokens)

        # minting another token
        token = self.run_smart_contract(engine, path, 'mint',
                                        self.OTHER_ACCOUNT_1, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES,
                                        signer_accounts=[self.OTHER_ACCOUNT_1])
        self.assertEqual('\x02', token)

        tokens.append('\x02')

        # tokens should increase again
        account_tokens = self.run_smart_contract(engine, path, 'tokensOf', self.OTHER_ACCOUNT_1)
        self.assertEqual(tokens, account_tokens)
