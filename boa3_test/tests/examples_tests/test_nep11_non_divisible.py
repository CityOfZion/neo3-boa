import json

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestNEP11Template(BoaTest):
    default_folder: str = 'examples'

    OWNER = neoxp.utils.get_account_by_name('owner')
    OTHER_ACCOUNT_1 = neoxp.utils.get_account_by_name('testAccount1')
    OTHER_ACCOUNT_2 = neoxp.utils.get_account_by_name('testAccount2')
    GAS_TO_DEPLOY = 100 * 10 ** 8

    TOKEN_META = bytes(
        '{ "name": "NEP11", "description": "Some description", "image": "{some image URI}", "tokenURI": "{some URI}" }',
        'utf-8')
    TOKEN_LOCKED = bytes('lockedContent', 'utf-8')
    ROYALTIES = bytes(
        '[{"address": "NZcuGiwRu1QscpmCyxj5XwQBUf6sk7dJJN", "value": 2000}, '
        '{"address": "NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB", "value": 3000}]',
        'utf-8')

    def test_nep11_compile(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-11', manifest['supportedstandards'])

    def test_nep11_symbol(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invoke = runner.call_contract(path, 'symbol')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual('EXMP', invoke.result)

    def test_nep11_decimals(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invoke = runner.call_contract(path, 'decimals')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(0, invoke.result)

    def test_nep11_balance_of(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        runner.add_gas(self.OTHER_ACCOUNT_1.address, add_amount)
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        # mint
        token_1 = '\x01'
        invokes.append(runner.call_contract(path, 'mint',
                                            other_account_script_hash, self.TOKEN_META,
                                            self.TOKEN_LOCKED, self.ROYALTIES))
        expected_results.append(token_1)

        # balance should be one
        invokes.append(runner.call_contract(path, 'balanceOf', other_account_script_hash))
        expected_results.append(1)

        # minting another token
        token_2 = '\x02'
        invokes.append(runner.call_contract(path, 'mint',
                                            other_account_script_hash, self.TOKEN_META,
                                            self.TOKEN_LOCKED, self.ROYALTIES))
        expected_results.append(token_2)

        # balance should increase again
        invokes.append(runner.call_contract(path, 'balanceOf', other_account_script_hash))
        expected_results.append(2)

        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_nep11_tokens_of(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        runner.add_gas(self.OTHER_ACCOUNT_1.address, add_amount)
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        tokens = []
        expected_minted_token_1 = '\x01'
        expected_minted_token_2 = '\x02'

        # initial tokensOf is an empty iterator
        invokes.append(runner.call_contract(path, 'tokensOf', other_account_script_hash))
        expected_results.append(tokens.copy())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # mint
        runner.run_contract(path, 'mint',
                            other_account_script_hash, self.TOKEN_META,
                            self.TOKEN_LOCKED, self.ROYALTIES, account=self.OTHER_ACCOUNT_1)
        tokens.append(expected_minted_token_1)

        # tokensOf should return ['\x01']
        invokes.append(runner.call_contract(path, 'tokensOf', other_account_script_hash))
        expected_results.append(tokens.copy())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # minting another token
        runner.run_contract(path, 'mint',
                            other_account_script_hash, self.TOKEN_META,
                            self.TOKEN_LOCKED, self.ROYALTIES, account=self.OTHER_ACCOUNT_1)
        tokens.append(expected_minted_token_2)

        # tokens should increase again
        invokes.append(runner.call_contract(path, 'tokensOf', other_account_script_hash))
        expected_results.append(tokens)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_nep11_total_supply(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        # smart contract deploys with zero tokens minted
        total_supply = 0

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invoke = runner.call_contract(path, 'totalSupply')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(total_supply, invoke.result)

    def test_nep11_transfer(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        runner.add_gas(self.OTHER_ACCOUNT_1.address, add_amount)
        other_account_1_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()
        other_account_2_script_hash = self.OTHER_ACCOUNT_2.script_hash.to_array()

        # mint
        token = '\x01'
        invokes.append(runner.call_contract(path, 'mint',
                                            other_account_1_script_hash, self.TOKEN_META,
                                            self.TOKEN_LOCKED, self.ROYALTIES))
        expected_results.append(token)

        # check owner before
        invokes.append(runner.call_contract(path, 'ownerOf', token))
        expected_results.append(other_account_1_script_hash)

        # transfer
        invokes.append(runner.call_contract(path, 'transfer',
                                            other_account_2_script_hash, token, None,
                                            expected_result_type=bool))
        expected_results.append(True)

        # check owner after
        invokes.append(runner.call_contract(path, 'ownerOf', token))
        expected_results.append(other_account_2_script_hash)

        # check balances after
        invokes.append(runner.call_contract(path, 'balanceOf', other_account_1_script_hash))
        expected_results.append(0)
        invokes.append(runner.call_contract(path, 'totalSupply'))
        expected_results.append(1)

        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'transfer', other_account_2_script_hash, b'thisisanonexistingtoken', None)
        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_nep11_onNEP11Payment(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        runner.add_gas(self.OTHER_ACCOUNT_1.address, add_amount)
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        # mint
        token = '\x01'
        runner.run_contract(path, 'mint',
                            other_account_script_hash, self.TOKEN_META,
                            self.TOKEN_LOCKED, self.ROYALTIES,
                            account=self.OTHER_ACCOUNT_1)

        # the smart contract will abort if any address calls the NEP11 onPayment method
        runner.call_contract(path, 'onNEP11Payment',
                             other_account_script_hash, 1, token, None)
        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ABORTED_CONTRACT_MSG)

    def test_nep11_deploy(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        contract = runner.deploy_contract(path, account=self.OWNER)
        runner.update_contracts(export_checkpoint=True)

        tx_id = contract.tx_id
        self.assertIsNotNone(tx_id)

        tx = runner.get_transaction_result(tx_id)
        self.assertIsInstance(tx.executions, list)
        self.assertEqual(1, len(tx.executions))
        tx_result = tx.executions[0]

        # contract was deployed only once
        self.assertEqual(1, len([notification for notification in tx_result.notifications if notification.name == "Deploy"]))

    def test_nep11_update(self):
        path = self.get_contract_path('nep11_non_divisible.py')
        new_nef, new_manifest = self.get_bytes_output(path)
        arg_manifest = String(json.dumps(new_manifest, separators=(',', ':'))).to_bytes()

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # update contract
        invoke = runner.call_contract(path, 'update',
                                      new_nef, arg_manifest)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertIsNone(invoke.result)

    def test_nep11_destroy(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # destroy contract
        invoke = runner.call_contract(path, 'destroy')
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertIsNone(invoke.result)

        runner.run_contract(path, 'destroy', account=self.OWNER)

        # should not exist anymore
        runner.call_contract(path, 'symbol')
        runner.execute(account=self.OWNER)
        self.assertNotEqual(VMState.HALT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.CONTRACT_NOT_FOUND_MSG_REGEX)

    def test_nep11_verify(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        invokes.append(runner.call_contract(path, 'getAuthorizedAddress',
                                            expected_result_type=list))
        expected_results.append([self.OWNER.script_hash.to_array()])

        invokes.append(runner.call_contract(path, 'verify',
                                            expected_result_type=bool))
        expected_results.append(True)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'verify',
                                            expected_result_type=bool))
        expected_results.append(False)

        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'verify',
                                            expected_result_type=bool))
        expected_results.append(False)

        runner.execute(account=self.OTHER_ACCOUNT_2)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_nep11_authorize(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()
        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        runner.call_contract(path, 'setAuthorizedAddress', other_account_script_hash, True)

        # now deauthorize the address
        runner.call_contract(path, 'setAuthorizedAddress', other_account_script_hash, False)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        auth_events = runner.get_events('Authorized')
        self.assertEqual(2, len(auth_events))

        authorize_event = auth_events[0]
        deauthorize_event = auth_events[1]

        # check if the event was triggered and the address was authorized
        self.assertEqual(0, authorize_event.arguments[1])
        self.assertEqual(1, authorize_event.arguments[2])

        # check if the event was triggered and the address was authorized
        self.assertEqual(0, deauthorize_event.arguments[1])
        self.assertEqual(0, deauthorize_event.arguments[2])

    def test_nep11_pause(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        runner.add_gas(self.OTHER_ACCOUNT_1.address, add_amount)
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        # pause contract
        invokes.append(runner.call_contract(path, 'updatePause', True,
                                            expected_result_type=bool))
        expected_results.append(True)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        runner.run_contract(path, 'updatePause', True, account=self.OWNER)

        # should fail because contract is paused
        runner.call_contract(path, 'mint',
                             other_account_script_hash, self.TOKEN_META, self.TOKEN_LOCKED, self.ROYALTIES)
        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # unpause contract
        invokes.append(runner.call_contract(path, 'updatePause', False,
                                            expected_result_type=bool))
        expected_results.append(False)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        runner.run_contract(path, 'updatePause', False, account=self.OWNER)

        # mint
        invokes.append(runner.call_contract(path, 'mint',
                                            other_account_script_hash, self.TOKEN_META,
                                            self.TOKEN_LOCKED, self.ROYALTIES))
        expected_results.append('\x01')

        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_nep11_mint(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        runner.add_gas(self.OTHER_ACCOUNT_1.address, add_amount)
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        # should succeed now that account has enough fees
        mint = runner.call_contract(path, 'mint',
                                    other_account_script_hash, self.TOKEN_META,
                                    self.TOKEN_LOCKED, self.ROYALTIES)

        runner.execute(account=self.OTHER_ACCOUNT_1, add_invokes_to_batch=True)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        token = mint.result
        invokes.append(runner.call_contract(path, 'properties', token, expected_result_type=dict))
        token_property = json.loads(self.TOKEN_META.decode('utf-8').replace("'", "\""))
        expected_results.append(token_property)

        invokes.append(runner.call_contract(path, 'getRoyalties', token, expected_result_type=str))
        expected_results.append(self.ROYALTIES.decode('utf-8'))

        # check balances after
        invokes.append(runner.call_contract(path, 'balanceOf', other_account_script_hash))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'totalSupply'))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'properties', b'thisisanonexistingtoken')
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_nep11_burn(self):
        path, _ = self.get_deploy_file_paths('nep11_non_divisible.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)

        # add some gas for fees
        add_amount = 10 * 10 ** 8
        runner.add_gas(self.OTHER_ACCOUNT_1.address, add_amount)
        other_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        # mint
        token = '\x01'
        invokes.append(runner.call_contract(path, 'mint',
                                            other_account_script_hash, self.TOKEN_META,
                                            self.TOKEN_LOCKED, self.ROYALTIES))
        expected_results.append(token)

        # burn
        invokes.append(runner.call_contract(path, 'burn', token,
                                            expected_result_type=bool))
        expected_results.append(True)

        # check balances after
        invokes.append(runner.call_contract(path, 'balanceOf', other_account_script_hash))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'totalSupply'))
        expected_results.append(0)

        runner.execute(account=self.OTHER_ACCOUNT_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
