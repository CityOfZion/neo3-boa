from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestAMMTemplate(BoaTest):
    default_folder: str = 'examples'

    OWNER = neoxp.utils.get_account_by_name('owner')
    OTHER_ACCOUNT_1 = neoxp.utils.get_account_by_name('testAccount1')
    OTHER_ACCOUNT_2 = neoxp.utils.get_account_by_name('testAccount2')
    GAS_TO_DEPLOY = 1000 * 10 ** 8

    def test_amm_compile(self):
        path = self.get_contract_path('amm.py')
        self.compile(path)

    def test_amm_set_address(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        path_zneo, _ = self.get_deploy_file_paths('wrapped_neo.py')
        path_zgas, _ = self.get_deploy_file_paths('wrapped_gas.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.deploy_contract(path, account=self.OWNER)
        zneo_contract = runner.deploy_contract(path_zneo)
        zgas_contract = runner.deploy_contract(path_zgas)
        runner.update_contracts(export_checkpoint=True)

        zneo_address = zneo_contract.script_hash
        zgas_address = zgas_contract.script_hash
        self.assertIsNotNone(zneo_address)
        self.assertIsNotNone(zgas_address)

        # won't work because it needs the owner signature
        invokes.append(runner.call_contract(path, 'set_address', zneo_address, zgas_address))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # it will work now
        invokes.append(runner.call_contract(path, 'set_address', zneo_address, zgas_address))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'get_token_a', expected_result_type=bytes))
        expected_results.append(zneo_address)

        invokes.append(runner.call_contract(path, 'get_token_b', expected_result_type=bytes))
        expected_results.append(zgas_address)

        # initialize will work once
        invokes.append(runner.call_contract(path, 'set_address', zneo_address, zgas_address))
        expected_results.append(False)

        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_amm_symbol(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'symbol')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual('AMM', invoke.result)

    def test_amm_decimals(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'decimals')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(8, invoke.result)

    def test_amm_total_supply(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'totalSupply')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(0, invoke.result)

    def test_amm_total_balance_of(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'balanceOf', self.OWNER.script_hash.to_array())
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(0, invoke.result)

        # should fail when the script length is not 20
        runner.call_contract(path, 'balanceOf', bytes(10))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.call_contract(path, 'balanceOf', bytes(30))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

    def test_amm_quote(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        amount_zneo = 1
        reserve_zneo = 100
        reserve_zgas = 1100 * 10 ** 8

        invoke = runner.call_contract(path, 'quote', amount_zneo, reserve_zneo, reserve_zgas)
        amount_zgas = amount_zneo * reserve_zgas // reserve_zneo

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertEqual(amount_zgas, invoke.result)

    def test_amm_on_nep17_payment(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        path_zneo, _ = self.get_deploy_file_paths('wrapped_neo.py')
        path_zgas, _ = self.get_deploy_file_paths('wrapped_gas.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        transferred_amount = 10

        test_account = self.OTHER_ACCOUNT_1
        test_account_script_hash = test_account.script_hash.to_array()

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_neo(test_account.address, transferred_amount)
        runner.add_gas(test_account.address, 2 * 10 ** 8)  # gas to invoke

        amm_contract = runner.deploy_contract(path, account=self.OWNER)
        zneo_contract = runner.deploy_contract(path_zneo)
        zgas_contract = runner.deploy_contract(path_zgas)
        runner.update_contracts(export_checkpoint=True)

        amm_address = amm_contract.script_hash
        zneo_address = zneo_contract.script_hash
        zgas_address = zgas_contract.script_hash
        self.assertIsNotNone(amm_address)
        self.assertIsNotNone(zneo_address)
        self.assertIsNotNone(zgas_address)

        runner.run_contract(path, 'set_address', zneo_address, zgas_address, account=self.OWNER)

        # adding the transferred_amount into test_account
        invokes.append(runner.call_contract(constants.NEO_SCRIPT, 'transfer',
                                            test_account_script_hash, zneo_address, transferred_amount, None))
        expected_results.append(True)

        # the AMM will accept this transaction, but there is no reason to send tokens directly to the smart contract.
        # to send tokens to the AMM you should use the add_liquidity function
        invokes.append(runner.call_contract(path_zneo, 'transfer',
                                            test_account_script_hash, amm_address, transferred_amount, None))
        expected_results.append(True)

        runner.execute(account=test_account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # the smart contract will abort if some address other than zNEO or zGAS calls the onPayment method
        runner.call_contract(path, 'onNEP17Payment', test_account_script_hash, transferred_amount, None)
        runner.execute(account=test_account)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ABORTED_CONTRACT_MSG)

    def test_amm_add_liquidity(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        path_zneo, _ = self.get_deploy_file_paths('wrapped_neo.py')
        path_zgas, _ = self.get_deploy_file_paths('wrapped_gas.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_balance_zneo = 10_000_000
        test_balance_zgas = 10_000_000 * 10 ** 8
        transferred_amount_zneo = 10
        transferred_amount_zgas = 110 * 10 ** 8

        test_account = self.OTHER_ACCOUNT_1
        test_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_gas(test_account.address, 2 * 10 ** 8)  # gas to invoke

        amm_contract = runner.deploy_contract(path, account=self.OWNER)
        zneo_contract = runner.deploy_contract(path_zneo)
        zgas_contract = runner.deploy_contract(path_zgas)
        runner.update_contracts(export_checkpoint=True)

        amm_address = amm_contract.script_hash
        zneo_address = zneo_contract.script_hash
        zgas_address = zgas_contract.script_hash
        self.assertIsNotNone(amm_address)
        self.assertIsNotNone(zneo_address)
        self.assertIsNotNone(zgas_address)

        runner.run_contract(path, 'set_address', zneo_address, zgas_address,
                            account=self.OWNER)

        runner.add_neo(test_account.address, test_balance_zneo)
        runner.add_gas(test_account.address, test_balance_zgas)

        # minting zNEO to test_account
        runner.run_contract(constants.NEO_SCRIPT, 'transfer',
                            test_account_script_hash, zneo_address, test_balance_zneo, None,
                            account=test_account)

        # minting zGAS to test_account
        runner.run_contract(constants.GAS_SCRIPT, 'transfer',
                            test_account_script_hash, zgas_address, test_balance_zgas, None,
                            account=test_account)

        # won't work, because the user did not allow the amm to transfer zNEO and zGAS
        runner.call_contract(path, 'add_liquidity',
                             transferred_amount_zneo, transferred_amount_zgas, 0, 0, test_account_script_hash)
        runner.execute(account=test_account)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # approving the AMM contract, so that it will be able to transfer zNEO from test_account
        invokes.append(runner.call_contract(path_zneo, 'approve',
                                            test_account_script_hash, amm_address, test_balance_zneo))
        expected_results.append(True)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_account
        invokes.append(runner.call_contract(path_zgas, 'approve',
                                            test_account_script_hash, amm_address, test_balance_zgas))
        expected_results.append(True)

        # saving data to demonstrate that the value will change later
        total_supply_before = runner.call_contract(path, 'totalSupply')
        balance_user_amm_before = runner.call_contract(path, 'balanceOf', test_account_script_hash)
        reserves_before = runner.call_contract(path, 'get_reserves')
        balance_user_zneo_before = runner.call_contract(path_zneo, 'balanceOf', test_account_script_hash)
        balance_user_zgas_before = runner.call_contract(path_zgas, 'balanceOf', test_account_script_hash)
        balance_amm_zneo_before = runner.call_contract(path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_before = runner.call_contract(path_zgas, 'balanceOf', amm_address)

        import math
        liquidity = int(math.sqrt(transferred_amount_zneo * transferred_amount_zgas))

        # adding liquidity to the pool will give you AMM tokens in return
        invokes.append(runner.call_contract(path, 'add_liquidity',
                                            transferred_amount_zneo, transferred_amount_zgas, 0, 0,
                                            test_account_script_hash))
        expected_results.append([transferred_amount_zneo, transferred_amount_zgas, liquidity])

        # data that will be compared with the previously saved data
        total_supply_after = runner.call_contract(path, 'totalSupply')
        balance_user_amm_after = runner.call_contract(path, 'balanceOf', test_account_script_hash)
        reserves_after = runner.call_contract(path, 'get_reserves')
        balance_user_zneo_after = runner.call_contract(path_zneo, 'balanceOf', test_account_script_hash)
        balance_user_zgas_after = runner.call_contract(path_zgas, 'balanceOf', test_account_script_hash)
        balance_amm_zneo_after = runner.call_contract(path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_after = runner.call_contract(path_zgas, 'balanceOf', amm_address)

        runner.execute(account=test_account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        transfer_events = runner.get_events('Transfer', origin=amm_address)
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(None, sender)
        self.assertEqual(test_account_script_hash, receiver)
        self.assertEqual(liquidity, amount)

        sync_events = runner.get_events('Sync', origin=amm_address)
        self.assertEqual(1, len(sync_events))
        self.assertEqual(2, len(sync_events[0].arguments))

        balance_zneo, balance_zgas = sync_events[0].arguments
        self.assertEqual(transferred_amount_zneo, balance_zneo)
        self.assertEqual(transferred_amount_zgas, balance_zgas)

        mint_events = runner.get_events('Mint', origin=amm_address)
        self.assertEqual(1, len(mint_events))
        self.assertEqual(3, len(mint_events[0].arguments))

        address, amount_zneo, amount_zgas = mint_events[0].arguments
        self.assertEqual(test_account_script_hash, address)
        self.assertEqual(transferred_amount_zneo, amount_zneo)
        self.assertEqual(transferred_amount_zgas, amount_zgas)

        self.assertEqual(total_supply_before.result + liquidity, total_supply_after.result)
        self.assertEqual(balance_user_amm_before.result + liquidity, balance_user_amm_after.result)
        self.assertEqual(reserves_before.result[0] + transferred_amount_zneo, reserves_after.result[0])
        self.assertEqual(reserves_before.result[1] + transferred_amount_zgas, reserves_after.result[1])
        self.assertEqual(balance_user_zneo_before.result - transferred_amount_zneo, balance_user_zneo_after.result)
        self.assertEqual(balance_user_zgas_before.result - transferred_amount_zgas, balance_user_zgas_after.result)
        self.assertEqual(reserves_before.result[0], balance_amm_zneo_before.result)
        self.assertEqual(reserves_before.result[1], balance_amm_zgas_before.result)
        self.assertEqual(reserves_after.result[0], balance_amm_zneo_after.result)
        self.assertEqual(reserves_after.result[1], balance_amm_zgas_after.result)

        runner.call_contract(path_zneo, 'approve',
                             test_account_script_hash, amm_address, test_balance_zneo)
        runner.call_contract(path_zgas, 'approve',
                             test_account_script_hash, amm_address, test_balance_zgas)
        runner.call_contract(path, 'add_liquidity',
                             transferred_amount_zneo, transferred_amount_zgas, 0, 0,
                             test_account_script_hash)

        transferred_amount_zneo = 2
        transferred_amount_zgas = 23 * 10 ** 8

        # approving the AMM contract, so that it will be able to transfer zNEO from test_account
        invokes.append(runner.call_contract(path_zneo, 'approve',
                                            test_account_script_hash, amm_address, transferred_amount_zneo))
        expected_results.append(True)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_account
        invokes.append(runner.call_contract(path_zgas, 'approve',
                                            test_account_script_hash, amm_address, transferred_amount_zgas))
        expected_results.append(True)

        # saving data to demonstrate that the value will change later
        total_supply_before = runner.call_contract(path, 'totalSupply')
        reserves_before = runner.call_contract(path, 'get_reserves')

        # adding liquidity to the pool will give you AMM tokens in return
        invokes.append(runner.call_contract(path, 'add_liquidity',
                                            transferred_amount_zneo, transferred_amount_zgas, 0, 0,
                                            test_account_script_hash))

        runner.execute(account=test_account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # zGAS will be quoted to keep the same ratio between zNEO and zGAS, the current ratio is 1 NEO to 11 GAS,
        # therefore, if 2 NEO are being added to the AMM, 22 GAS will be added instead of 23
        transferred_amount_zgas_quoted = transferred_amount_zneo * reserves_before.result[1] // reserves_before.result[0]

        # since there are tokens in the pool already, liquidity will be calculated as follows
        liquidity = min(transferred_amount_zneo * total_supply_before.result // reserves_before.result[0],
                        transferred_amount_zgas_quoted * total_supply_before.result // reserves_before.result[1])
        expected_results.append([transferred_amount_zneo, transferred_amount_zgas_quoted, liquidity])

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        transfer_events = runner.get_events('Transfer', origin=amm_address)
        self.assertEqual(2, len(transfer_events))
        self.assertEqual(3, len(transfer_events[1].arguments))

        sender, receiver, amount = transfer_events[1].arguments
        self.assertEqual(None, sender)
        self.assertEqual(test_account_script_hash, receiver)
        self.assertEqual(liquidity, amount)

        sync_events = runner.get_events('Sync', origin=amm_address)
        self.assertEqual(2, len(sync_events))
        self.assertEqual(2, len(sync_events[1].arguments))

        balance_zneo, balance_zgas = sync_events[1].arguments
        self.assertEqual(reserves_before.result[0] + transferred_amount_zneo, balance_zneo)
        self.assertEqual(reserves_before.result[1] + transferred_amount_zgas_quoted, balance_zgas)

        mint_events = runner.get_events('Mint', origin=amm_address)
        self.assertEqual(2, len(mint_events))
        self.assertEqual(3, len(mint_events[1].arguments))

        address, amount_zneo, amount_zgas = mint_events[1].arguments
        self.assertEqual(test_account_script_hash, address)
        self.assertEqual(transferred_amount_zneo, amount_zneo)
        self.assertEqual(transferred_amount_zgas_quoted, amount_zgas)

    def test_amm_remove_liquidity(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        path_zneo, _ = self.get_deploy_file_paths('wrapped_neo.py')
        path_zgas, _ = self.get_deploy_file_paths('wrapped_gas.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_balance_zneo = 10_000_000
        test_balance_zgas = 10_000_000 * 10 ** 8
        transferred_amount_zneo = 10
        transferred_amount_zgas = 110 * 10 ** 8

        test_account = self.OTHER_ACCOUNT_1
        test_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_gas(test_account.address, 7 * 10 ** 8)  # gas to invoke

        amm_contract = runner.deploy_contract(path, account=self.OWNER)
        zneo_contract = runner.deploy_contract(path_zneo)
        zgas_contract = runner.deploy_contract(path_zgas)
        runner.update_contracts(export_checkpoint=True)

        amm_address = amm_contract.script_hash
        zneo_address = zneo_contract.script_hash
        zgas_address = zgas_contract.script_hash
        self.assertIsNotNone(amm_address)
        self.assertIsNotNone(zneo_address)
        self.assertIsNotNone(zgas_address)

        runner.run_contract(path, 'set_address', zneo_address, zgas_address,
                            account=self.OWNER)

        # can't remove liquidity, because the user doesn't have any
        runner.call_contract(path, 'remove_liquidity', 10000, 0, 0, test_account_script_hash)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.add_neo(test_account.address, test_balance_zneo)
        runner.add_gas(test_account.address, test_balance_zgas)

        # minting zNEO to test_account
        runner.run_contract(constants.NEO_SCRIPT, 'transfer',
                            test_account_script_hash, zneo_address, test_balance_zneo, None,
                            account=test_account)

        # minting zGAS to test_account
        runner.run_contract(constants.GAS_SCRIPT, 'transfer',
                            test_account_script_hash, zgas_address, test_balance_zgas, None,
                            account=test_account)

        # approving the AMM contract, so that it will be able to transfer zNEO from test_account
        runner.run_contract(path_zneo, 'approve',
                            test_account_script_hash, amm_address, transferred_amount_zneo,
                            account=test_account)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_account
        runner.run_contract(path_zgas, 'approve',
                            test_account_script_hash, amm_address, transferred_amount_zgas,
                            account=test_account)

        # adding liquidity to the pool will give you AMM tokens in return
        runner.run_contract(path, 'add_liquidity',
                            transferred_amount_zneo, transferred_amount_zgas, 0, 0, test_account_script_hash,
                            account=test_account)
        import math
        liquidity = int(math.sqrt(transferred_amount_zneo * transferred_amount_zgas))

        # saving data to demonstrate that the value will change later
        total_supply_before = runner.call_contract(path, 'totalSupply')
        balance_user_before = runner.call_contract(path, 'balanceOf', test_account_script_hash)
        reserves_before = runner.call_contract(path, 'get_reserves')
        balance_user_zneo_before = runner.call_contract(path_zneo, 'balanceOf', test_account_script_hash)
        balance_user_zgas_before = runner.call_contract(path_zgas, 'balanceOf', test_account_script_hash)
        balance_amm_zneo_before = runner.call_contract(path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_before = runner.call_contract(path_zgas, 'balanceOf', amm_address)

        # removing liquidity from the pool will return the equivalent zNEO and zGAS that were used to fund the pool
        invokes.append(runner.call_contract(path, 'remove_liquidity',
                                            liquidity, 0, 0, test_account_script_hash))
        expected_results.append([transferred_amount_zneo, transferred_amount_zgas])

        # data that will be compared with the previously saved data
        total_supply_after = runner.call_contract(path, 'totalSupply')
        balance_user_after = runner.call_contract(path, 'balanceOf', test_account_script_hash)
        reserves_after = runner.call_contract(path, 'get_reserves')
        balance_user_zneo_after = runner.call_contract(path_zneo, 'balanceOf', test_account_script_hash)
        balance_user_zgas_after = runner.call_contract(path_zgas, 'balanceOf', test_account_script_hash)
        balance_amm_zneo_after = runner.call_contract(path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_after = runner.call_contract(path_zgas, 'balanceOf', amm_address)

        runner.execute(account=test_account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        transfer_events = runner.get_events('Transfer', origin=amm_address)
        # add_liquidity sent a Transfer event and remove_liquidity sent another
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        self.assertEqual(test_account_script_hash, sender)
        self.assertEqual(None, receiver)
        self.assertEqual(liquidity, amount)

        sync_events = runner.get_events('Sync', origin=amm_address)
        self.assertEqual(1, len(sync_events))
        self.assertEqual(2, len(sync_events[0].arguments))

        balance_zneo, balance_zgas = sync_events[0].arguments
        self.assertEqual(reserves_before.result[0] - transferred_amount_zneo, balance_zneo)
        self.assertEqual(reserves_before.result[1] - transferred_amount_zgas, balance_zgas)

        burn_events = runner.get_events('Burn', origin=amm_address)
        self.assertEqual(1, len(burn_events))
        self.assertEqual(3, len(burn_events[0].arguments))

        address, amount_zneo, amount_zgas = burn_events[0].arguments
        if isinstance(address, str):
            address = String(address).to_bytes()
        self.assertEqual(test_account_script_hash, address)
        self.assertEqual(transferred_amount_zneo, amount_zneo)
        self.assertEqual(transferred_amount_zgas, amount_zgas)

        self.assertEqual(total_supply_before.result - liquidity, total_supply_after.result)
        self.assertEqual(balance_user_before.result - liquidity, balance_user_after.result)
        self.assertEqual(reserves_before.result[0] - transferred_amount_zneo, reserves_after.result[0])
        self.assertEqual(reserves_before.result[1] - transferred_amount_zgas, reserves_after.result[1])
        self.assertEqual(balance_user_zneo_before.result + transferred_amount_zneo, balance_user_zneo_after.result)
        self.assertEqual(balance_user_zgas_before.result + transferred_amount_zgas, balance_user_zgas_after.result)
        self.assertEqual(reserves_before.result[0], balance_amm_zneo_before.result)
        self.assertEqual(reserves_before.result[1], balance_amm_zgas_before.result)
        self.assertEqual(reserves_after.result[0], balance_amm_zneo_after.result)
        self.assertEqual(reserves_after.result[1], balance_amm_zgas_after.result)

    def test_amm_swap_zneo_to_zgas(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        path_zneo, _ = self.get_deploy_file_paths('wrapped_neo.py')
        path_zgas, _ = self.get_deploy_file_paths('wrapped_gas.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_balance_zneo = 10_000_000
        test_balance_zgas = 10_000_000 * 10 ** 8
        transferred_amount_zneo = 10
        transferred_amount_zgas = 110 * 10 ** 8

        test_account = self.OTHER_ACCOUNT_1
        test_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_gas(test_account.address, 7 * 10 ** 8)  # gas to invoke

        amm_contract = runner.deploy_contract(path, account=self.OWNER)
        zneo_contract = runner.deploy_contract(path_zneo)
        zgas_contract = runner.deploy_contract(path_zgas)
        runner.update_contracts(export_checkpoint=True)

        amm_address = amm_contract.script_hash
        zneo_address = zneo_contract.script_hash
        zgas_address = zgas_contract.script_hash
        self.assertIsNotNone(amm_address)
        self.assertIsNotNone(zneo_address)
        self.assertIsNotNone(zgas_address)

        runner.run_contract(path, 'set_address', zneo_address, zgas_address,
                            account=self.OWNER)

        # can't remove liquidity, because the user doesn't have any
        runner.call_contract(path, 'remove_liquidity', 10000, 0, 0, test_account_script_hash)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.add_neo(test_account.address, test_balance_zneo)
        runner.add_gas(test_account.address, test_balance_zgas)

        # minting zNEO to test_account
        runner.run_contract(constants.NEO_SCRIPT, 'transfer',
                            test_account_script_hash, zneo_address, test_balance_zneo, None,
                            account=test_account)

        # minting zGAS to test_account
        runner.run_contract(constants.GAS_SCRIPT, 'transfer',
                            test_account_script_hash, zgas_address, test_balance_zgas, None,
                            account=test_account)

        # approving the AMM contract, so that it will be able to transfer zNEO from test_account
        runner.run_contract(path_zneo, 'approve',
                            test_account_script_hash, amm_address, transferred_amount_zneo,
                            account=test_account)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_account
        runner.run_contract(path_zgas, 'approve',
                            test_account_script_hash, amm_address, transferred_amount_zgas,
                            account=test_account)

        # adding liquidity to the pool will give you AMM tokens in return
        runner.run_contract(path, 'add_liquidity',
                            transferred_amount_zneo, transferred_amount_zgas, 0, 0, test_account_script_hash,
                            account=test_account)

        swapped_zneo = 1

        # won't work, because user did not have enough zNEO tokens
        runner.call_contract(path, 'swap_tokens',
                             swapped_zneo, 0, zneo_address, test_account_script_hash)
        runner.execute(account=test_account)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # approving the AMM contract, so that it will be able to transfer zNEO from test_account
        invokes.append(runner.call_contract(path_zneo, 'approve',
                                            test_account_script_hash, amm_address, swapped_zneo))
        expected_results.append(True)

        # saving data to demonstrate that the value will change later
        total_supply_before = runner.call_contract(path, 'totalSupply')
        reserves_before = runner.call_contract(path, 'get_reserves')
        balance_user_zneo_before = runner.call_contract(path_zneo, 'balanceOf', test_account_script_hash)
        balance_user_zgas_before = runner.call_contract(path_zgas, 'balanceOf', test_account_script_hash)
        balance_amm_zneo_before = runner.call_contract(path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_before = runner.call_contract(path_zgas, 'balanceOf', amm_address)

        # swapping zneo for zgas
        invokes.append(runner.call_contract(path, 'swap_tokens',
                                            swapped_zneo, 0, zneo_address, test_account_script_hash))

        # data that will be compared with the previously saved data
        total_supply_after = runner.call_contract(path, 'totalSupply')
        reserves_after = runner.call_contract(path, 'get_reserves')
        balance_user_zneo_after = runner.call_contract(path_zneo, 'balanceOf', test_account_script_hash)
        balance_user_zgas_after = runner.call_contract(path_zgas, 'balanceOf', test_account_script_hash)
        balance_amm_zneo_after = runner.call_contract(path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_after = runner.call_contract(path_zgas, 'balanceOf', amm_address)

        runner.execute(account=test_account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # there is a 0.3% fee when doing a swap
        swapped_zneo_with_fee = swapped_zneo * (1000 - 3)
        swapped_zgas = swapped_zneo_with_fee * reserves_before.result[1] // (reserves_before.result[0] * 1000 + swapped_zneo_with_fee)
        expected_results.append(swapped_zgas)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # add_liquidity sent a Sync before
        transfer_events = runner.get_events('Sync')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(2, len(transfer_events[0].arguments))

        balance_zneo, balance_zgas = transfer_events[0].arguments
        self.assertEqual(reserves_before.result[0] + swapped_zneo, balance_zneo)
        self.assertEqual(reserves_before.result[1] - swapped_zgas, balance_zgas)

        transfer_events = runner.get_events('Swap')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(5, len(transfer_events[0].arguments))

        address, amount_zneo_in, amount_zgas_in, amount_zneo_out, amount_zgas_out = transfer_events[0].arguments
        self.assertEqual(test_account_script_hash, address)
        self.assertEqual(swapped_zneo, amount_zneo_in)
        self.assertEqual(0, amount_zgas_in)
        self.assertEqual(0, amount_zneo_out)
        self.assertEqual(swapped_zgas, amount_zgas_out)

        self.assertEqual(total_supply_before.result, total_supply_after.result)
        self.assertEqual(reserves_before.result[0] + swapped_zneo, reserves_after.result[0])
        self.assertEqual(reserves_before.result[1] - swapped_zgas, reserves_after.result[1])
        self.assertEqual(balance_user_zneo_before.result - swapped_zneo, balance_user_zneo_after.result)
        self.assertEqual(balance_user_zgas_before.result + swapped_zgas, balance_user_zgas_after.result)
        self.assertEqual(reserves_before.result[0], balance_amm_zneo_before.result)
        self.assertEqual(reserves_before.result[1], balance_amm_zgas_before.result)
        self.assertEqual(reserves_after.result[0], balance_amm_zneo_after.result)
        self.assertEqual(reserves_after.result[1], balance_amm_zgas_after.result)
        self.assertEqual(reserves_before.result[0] + swapped_zneo, reserves_after.result[0])
        self.assertEqual(reserves_before.result[1] - swapped_zgas, reserves_after.result[1])

    def test_amm_swap_zgas_to_zneo(self):
        path, _ = self.get_deploy_file_paths('amm.py')
        path_zneo, _ = self.get_deploy_file_paths('wrapped_neo.py')
        path_zgas, _ = self.get_deploy_file_paths('wrapped_gas.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        test_balance_zneo = 10_000_000
        test_balance_zgas = 10_000_000 * 10 ** 8
        transferred_amount_zneo = 100
        transferred_amount_zgas = 110 * 10 ** 8

        test_account = self.OTHER_ACCOUNT_1
        test_account_script_hash = self.OTHER_ACCOUNT_1.script_hash.to_array()

        runner.add_gas(self.OWNER.address, self.GAS_TO_DEPLOY)
        runner.add_gas(test_account.address, 7 * 10 ** 8)  # gas to invoke

        amm_contract = runner.deploy_contract(path, account=self.OWNER)
        zneo_contract = runner.deploy_contract(path_zneo)
        zgas_contract = runner.deploy_contract(path_zgas)
        runner.update_contracts(export_checkpoint=True)

        amm_address = amm_contract.script_hash
        zneo_address = zneo_contract.script_hash
        zgas_address = zgas_contract.script_hash
        self.assertIsNotNone(amm_address)
        self.assertIsNotNone(zneo_address)
        self.assertIsNotNone(zgas_address)

        runner.run_contract(path, 'set_address', zneo_address, zgas_address,
                            account=self.OWNER)

        # can't remove liquidity, because the user doesn't have any
        runner.call_contract(path, 'remove_liquidity', 10000, 0, 0, test_account_script_hash)
        runner.execute(account=self.OWNER)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        runner.add_neo(test_account.address, test_balance_zneo)
        runner.add_gas(test_account.address, test_balance_zgas)

        # minting zNEO to test_account
        runner.run_contract(constants.NEO_SCRIPT, 'transfer',
                            test_account_script_hash, zneo_address, test_balance_zneo, None,
                            account=test_account)

        # minting zGAS to test_account
        runner.run_contract(constants.GAS_SCRIPT, 'transfer',
                            test_account_script_hash, zgas_address, test_balance_zgas, None,
                            account=test_account)

        # approving the AMM contract, so that it will be able to transfer zNEO from test_account
        runner.run_contract(path_zneo, 'approve',
                            test_account_script_hash, amm_address, transferred_amount_zneo,
                            account=test_account)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_account
        runner.run_contract(path_zgas, 'approve',
                            test_account_script_hash, amm_address, transferred_amount_zgas,
                            account=test_account)

        # adding liquidity to the pool will give you AMM tokens in return
        runner.run_contract(path, 'add_liquidity',
                            transferred_amount_zneo, transferred_amount_zgas, 0, 0, test_account_script_hash,
                            account=test_account)

        swapped_zgas = 11 * 10 ** 8
        # won't work, because user did not enough zGAS tokens
        runner.call_contract(path, 'swap_tokens',
                             swapped_zgas, 0, zgas_address, test_account_script_hash)
        runner.execute(account=test_account)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ASSERT_RESULTED_FALSE_MSG)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_account
        invokes.append(runner.call_contract(path_zgas, 'approve',
                                            test_account_script_hash, amm_address, swapped_zgas))
        expected_results.append(True)

        # saving data to demonstrate that the value will change later
        total_supply_before = runner.call_contract(path, 'totalSupply')
        reserves_before = runner.call_contract(path, 'get_reserves')
        balance_user_zneo_before = runner.call_contract(path_zneo, 'balanceOf', test_account_script_hash)
        balance_user_zgas_before = runner.call_contract(path_zgas, 'balanceOf', test_account_script_hash)
        balance_amm_zneo_before = runner.call_contract(path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_before = runner.call_contract(path_zgas, 'balanceOf', amm_address)

        # swapping zgas for zneo
        invokes.append(runner.call_contract(path, 'swap_tokens',
                                            swapped_zgas, 0, zgas_address, test_account_script_hash))

        # data that will be compared with the previously saved data
        total_supply_after = runner.call_contract(path, 'totalSupply')
        reserves_after = runner.call_contract(path, 'get_reserves')
        balance_user_zneo_after = runner.call_contract(path_zneo, 'balanceOf', test_account_script_hash)
        balance_user_zgas_after = runner.call_contract(path_zgas, 'balanceOf', test_account_script_hash)
        balance_amm_zneo_after = runner.call_contract(path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_after = runner.call_contract(path_zgas, 'balanceOf', amm_address)

        runner.execute(account=test_account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        # there is a 0.3% fee when doing a swap
        swapped_zgas_with_fee = swapped_zgas * (1000 - 3)
        swapped_zneo = swapped_zgas_with_fee * reserves_before.result[0] // (reserves_before.result[1] * 1000 + swapped_zgas_with_fee)
        expected_results.append(swapped_zneo)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # add_liquidity sent a Sync before
        transfer_events = runner.get_events('Sync')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(2, len(transfer_events[0].arguments))

        balance_zneo, balance_zgas = transfer_events[0].arguments
        self.assertEqual(reserves_before.result[0] - swapped_zneo, balance_zneo)
        self.assertEqual(reserves_before.result[1] + swapped_zgas, balance_zgas)

        transfer_events = runner.get_events('Swap')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(5, len(transfer_events[0].arguments))

        address, amount_zneo_in, amount_zgas_in, amount_zneo_out, amount_zgas_out = transfer_events[0].arguments
        self.assertEqual(test_account_script_hash, address)
        self.assertEqual(0, amount_zneo_in)
        self.assertEqual(swapped_zgas, amount_zgas_in)
        self.assertEqual(swapped_zneo, amount_zneo_out)
        self.assertEqual(0, amount_zgas_out)

        self.assertEqual(total_supply_before.result, total_supply_after.result)
        self.assertEqual(reserves_before.result[0] - swapped_zneo, reserves_after.result[0])
        self.assertEqual(reserves_before.result[1] + swapped_zgas, reserves_after.result[1])
        self.assertEqual(balance_user_zneo_before.result + swapped_zneo, balance_user_zneo_after.result)
        self.assertEqual(balance_user_zgas_before.result - swapped_zgas, balance_user_zgas_after.result)
        self.assertEqual(reserves_before.result[0], balance_amm_zneo_before.result)
        self.assertEqual(reserves_before.result[1], balance_amm_zgas_before.result)
        self.assertEqual(reserves_after.result[0], balance_amm_zneo_after.result)
        self.assertEqual(reserves_after.result[1], balance_amm_zgas_after.result)
        self.assertEqual(reserves_before.result[0] - swapped_zneo, reserves_after.result[0])
        self.assertEqual(reserves_before.result[1] + swapped_zgas, reserves_after.result[1])
