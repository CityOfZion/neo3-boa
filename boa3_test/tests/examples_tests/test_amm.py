from boa3.boa3 import Boa3
from boa3.constants import NEO_SCRIPT, GAS_SCRIPT
from boa3.neo import to_script_hash
from boa3.neo.cryptography import hash160
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTemplate(BoaTest):

    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = bytes(range(20))

    def test_amm_compile(self):
        path = self.get_contract_path('amm.py')
        Boa3.compile(path)

    def test_amm_deploy(self):
        path = self.get_contract_path('amm.py')
        engine = TestEngine()

        # needs the owner signature
        result = self.run_smart_contract(engine, path, method='deploy',
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should return false if the signature isn't from the owner
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # must always return false after first execution
        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

    def test_amm_set_address(self):
        path = self.get_contract_path('amm.py')
        path_zneo = self.get_contract_path('wrapped_neo.py')
        path_zgas = self.get_contract_path('wrapped_gas.py')
        engine = TestEngine()

        engine.add_contract(path_zneo.replace('.py', '.nef'))
        engine.add_contract(path_zgas.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path_zneo)
        zneo_address = hash160(output)

        output, manifest = self.compile_and_save(path_zgas)
        zgas_address = hash160(output)

        # won't work because the contract must have been deployed before
        result = self.run_smart_contract(engine, path, 'set_address', zneo_address, zgas_address,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # won't work because it needs the owner signature
        result = self.run_smart_contract(engine, path, 'set_address', zneo_address, zgas_address,
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # it will work now
        result = self.run_smart_contract(engine, path, 'set_address', zneo_address, zgas_address,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # initialize will work once
        result = self.run_smart_contract(engine, path, 'set_address', zneo_address, zgas_address,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

    def test_amm_symbol(self):
        path = self.get_contract_path('amm.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'symbol')
        self.assertEqual('AMM', result)

    def test_amm_decimals(self):
        path = self.get_contract_path('amm.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'decimals')
        self.assertEqual(8, result)

    def test_amm_total_supply(self):
        path = self.get_contract_path('amm.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'totalSupply')
        self.assertEqual(0, result)

    def test_amm_total_balance_of(self):
        path = self.get_contract_path('amm.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'balanceOf', self.OWNER_SCRIPT_HASH)
        self.assertEqual(0, result)

        # should fail when the script length is not 20
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(10))
        with self.assertRaises(TestExecutionException, msg=self.ASSERT_RESULTED_FALSE_MSG):
            self.run_smart_contract(engine, path, 'balanceOf', bytes(30))

    def test_amm_quote(self):
        path = self.get_contract_path('amm.py')
        engine = TestEngine()
        amount_zneo = 1 * 10 ** 8
        reserve_zneo = 100 * 10 ** 8
        reserve_zgas = 1100 * 10 ** 8
        result = self.run_smart_contract(engine, path, 'quote', amount_zneo, reserve_zneo, reserve_zgas)
        amount_zgas = amount_zneo * reserve_zgas // reserve_zneo
        self.assertEqual(amount_zgas, result)

    def test_amm_onNEP17Payment(self):
        transferred_amount = 10 * 10 ** 8

        path = self.get_contract_path('amm.py')
        path_aux = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')
        path_zneo = self.get_contract_path('wrapped_neo.py')
        path_zgas = self.get_contract_path('wrapped_gas.py')
        engine = TestEngine()

        engine.add_contract(path.replace('.py', '.nef'))
        engine.add_contract(path_zneo.replace('.py', '.nef'))
        engine.add_contract(path_zgas.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        amm_address = hash160(output)

        output, manifest = self.compile_and_save(path_aux)
        aux_address = hash160(output)

        output, manifest = self.compile_and_save(path_zneo)
        zneo_address = hash160(output)

        output, manifest = self.compile_and_save(path_zgas)
        zgas_address = hash160(output)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'set_address', zneo_address, zgas_address,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # the smart contract will abort if some address other than zNEO or zGAS calls the onPayment method
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'onNEP17Payment', aux_address, transferred_amount, None,
                                    signer_accounts=[aux_address])

        engine.add_neo(aux_address, transferred_amount)

        # adding the transferred_amount into the aux_address
        result = self.run_smart_contract(engine, path_aux, 'calling_transfer',
                                         NEO_SCRIPT, aux_address, zneo_address, transferred_amount, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # the AMM will accept this transaction, but there is no reason to send tokens directly to the smart contract.
        # to send tokens to the AMM you should use the add_liquidity function
        result = self.run_smart_contract(engine, path_aux, 'calling_transfer',
                                         zneo_address, aux_address, amm_address, transferred_amount, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

    def test_amm_add_liquidity(self):
        transferred_amount_zneo = 10 * 10 ** 8
        transferred_amount_zgas = 110 * 10 ** 8

        path = self.get_contract_path('amm.py')
        path_zneo = self.get_contract_path('wrapped_neo.py')
        path_zgas = self.get_contract_path('wrapped_gas.py')
        path_aux = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')
        engine = TestEngine()

        engine.add_contract(path.replace('.py', '.nef'))
        engine.add_contract(path_zneo.replace('.py', '.nef'))
        engine.add_contract(path_zgas.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        amm_address = hash160(output)

        output, manifest = self.compile_and_save(path_zneo)
        zneo_address = hash160(output)

        output, manifest = self.compile_and_save(path_zgas)
        zgas_address = hash160(output)

        output, manifest = self.compile_and_save(path_aux)
        aux_address = hash160(output)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'set_address', zneo_address, zgas_address,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        engine.add_neo(aux_address, 10_000_000 * 10 ** 8)
        # minting zNEO to this auxiliary smart contract is needed, because the test engine has some limitations
        result = self.run_smart_contract(engine, path_aux, 'calling_transfer',
                                         NEO_SCRIPT, aux_address, zneo_address, 10_000_000 * 10 ** 8, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        engine.add_gas(aux_address, 10_000_000 * 10 ** 8)
        # minting zGAS to this auxiliary smart contract is needed, because the test engine has some limitations
        result = self.run_smart_contract(engine, path_aux, 'calling_transfer',
                                         GAS_SCRIPT, aux_address, zgas_address, 10_000_000 * 10 ** 8, None,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # won't work, because the user did not allow the amm to transfer zNEO and zGAS
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'add_liquidity', transferred_amount_zneo, transferred_amount_zgas, 0,
                                    0, aux_address,
                                    signer_accounts=[aux_address])

        # approving the AMM contract, so that it will be able to transfer zNEO from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zneo_address, amm_address, transferred_amount_zneo,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zgas_address, amm_address, transferred_amount_zgas,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # saving data to demonstrate that the value will change later
        total_supply_before = self.run_smart_contract(engine, path, 'totalSupply')
        balance_user_amm_before = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        reserves_before = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)
        # adding liquidity to the pool will give you AMM tokens in return
        result = self.run_smart_contract(engine, path, 'add_liquidity',
                                         transferred_amount_zneo, transferred_amount_zgas, 0, 0, aux_address,
                                         signer_accounts=[aux_address])
        import math
        liquidity = int(math.sqrt(transferred_amount_zneo * transferred_amount_zgas))
        self.assertEqual(3, len(result))
        self.assertEqual(transferred_amount_zneo, result[0])
        self.assertEqual(transferred_amount_zgas, result[1])
        self.assertEqual(liquidity, result[2])

        transfer_events = engine.get_events('Transfer', origin=amm_address)
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(3, len(transfer_events[0].arguments))

        sender, receiver, amount = transfer_events[0].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(aux_address, receiver)
        self.assertEqual(liquidity, amount)

        sync_events = engine.get_events('Sync', origin=amm_address)
        self.assertEqual(1, len(sync_events))
        self.assertEqual(2, len(sync_events[0].arguments))

        balance_zneo, balance_zgas = sync_events[0].arguments
        self.assertEqual(transferred_amount_zneo, balance_zneo)
        self.assertEqual(transferred_amount_zgas, balance_zgas)

        mint_events = engine.get_events('Mint', origin=amm_address)
        self.assertEqual(1, len(mint_events))
        self.assertEqual(3, len(mint_events[0].arguments))

        address, amount_zneo, amount_zgas = mint_events[0].arguments
        if isinstance(address, str):
            address = String(address).to_bytes()
        self.assertEqual(aux_address, address)
        self.assertEqual(transferred_amount_zneo, amount_zneo)
        self.assertEqual(transferred_amount_zgas, amount_zgas)

        # data that will be compared with the previously saved data
        total_supply_after = self.run_smart_contract(engine, path, 'totalSupply')
        balance_user_amm_after = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        reserves_after = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)

        self.assertEqual(total_supply_before + liquidity, total_supply_after)
        self.assertEqual(balance_user_amm_before + liquidity, balance_user_amm_after)
        self.assertEqual(reserves_before[0] + transferred_amount_zneo, reserves_after[0])
        self.assertEqual(reserves_before[1] + transferred_amount_zgas, reserves_after[1])
        self.assertEqual(balance_user_zneo_before - transferred_amount_zneo, balance_user_zneo_after)
        self.assertEqual(balance_user_zgas_before - transferred_amount_zgas, balance_user_zgas_after)
        self.assertEqual(reserves_before[0], balance_amm_zneo_before)
        self.assertEqual(reserves_before[1], balance_amm_zgas_before)
        self.assertEqual(reserves_after[0], balance_amm_zneo_after)
        self.assertEqual(reserves_after[1], balance_amm_zgas_after)

        transferred_amount_zneo = 2 * 10 ** 8
        transferred_amount_zgas = 23 * 10 ** 8

        # approving the AMM contract, so that it will be able to transfer zNEO from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zneo_address, amm_address, transferred_amount_zneo,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zgas_address, amm_address, transferred_amount_zgas,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # saving data to demonstrate that the value will change later
        total_supply_before = self.run_smart_contract(engine, path, 'totalSupply')
        balance_user_before = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        reserves_before = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)
        # adding liquidity to the pool will give you AMM tokens in return
        result = self.run_smart_contract(engine, path, 'add_liquidity',
                                         transferred_amount_zneo, transferred_amount_zgas, 0, 0, aux_address,
                                         signer_accounts=[aux_address])
        # zGAS will be quoted to keep the same ratio between zNEO and zGAS, the current ratio is 1 NEO to 11 GAS,
        # therefore, if 2 NEO are being added to the AMM, 22 GAS will be added instead of 23
        transferred_amount_zgas_quoted = transferred_amount_zneo * reserves_before[1] // reserves_before[0]
        # since there are tokens in the pool already, liquidity will be calculated as follows
        liquidity = min(transferred_amount_zneo * total_supply_before // reserves_before[0],
                        transferred_amount_zgas_quoted * total_supply_before // reserves_before[1])
        self.assertEqual(3, len(result))
        self.assertEqual(transferred_amount_zneo, result[0])
        self.assertEqual(transferred_amount_zgas_quoted, result[1])
        self.assertEqual(liquidity, result[2])

        transfer_events = engine.get_events('Transfer', origin=amm_address)
        self.assertEqual(2, len(transfer_events))
        self.assertEqual(3, len(transfer_events[1].arguments))

        sender, receiver, amount = transfer_events[1].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(None, sender)
        self.assertEqual(aux_address, receiver)
        self.assertEqual(liquidity, amount)

        sync_events = engine.get_events('Sync', origin=amm_address)
        self.assertEqual(2, len(sync_events))
        self.assertEqual(2, len(sync_events[1].arguments))

        balance_zneo, balance_zgas = sync_events[1].arguments
        self.assertEqual(reserves_before[0] + transferred_amount_zneo, balance_zneo)
        self.assertEqual(reserves_before[1] + transferred_amount_zgas_quoted, balance_zgas)

        mint_events = engine.get_events('Mint', origin=amm_address)
        self.assertEqual(2, len(mint_events))
        self.assertEqual(3, len(mint_events[1].arguments))

        address, amount_zneo, amount_zgas = mint_events[1].arguments
        if isinstance(address, str):
            address = String(address).to_bytes()
        self.assertEqual(aux_address, address)
        self.assertEqual(transferred_amount_zneo, amount_zneo)
        self.assertEqual(transferred_amount_zgas_quoted, amount_zgas)

        # data that will be compared with the previously saved data
        total_supply_after = self.run_smart_contract(engine, path, 'totalSupply')
        balance_user_after = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        reserves_after = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)

        self.assertEqual(total_supply_before + liquidity, total_supply_after)
        self.assertEqual(balance_user_before + liquidity, balance_user_after)
        self.assertEqual(reserves_before[0] + transferred_amount_zneo, reserves_after[0])
        self.assertEqual(reserves_before[1] + transferred_amount_zgas_quoted, reserves_after[1])
        self.assertEqual(balance_user_zneo_before - transferred_amount_zneo, balance_user_zneo_after)
        self.assertEqual(balance_user_zgas_before - transferred_amount_zgas_quoted, balance_user_zgas_after)
        self.assertEqual(reserves_before[0], balance_amm_zneo_before)
        self.assertEqual(reserves_before[1], balance_amm_zgas_before)
        self.assertEqual(reserves_after[0], balance_amm_zneo_after)
        self.assertEqual(reserves_after[1], balance_amm_zgas_after)

    def test_amm_remove_liquidity(self):
        transferred_amount_zneo = 10 * 10 ** 8
        transferred_amount_zgas = 110 * 10 ** 8

        path = self.get_contract_path('amm.py')
        path_zneo = self.get_contract_path('wrapped_neo.py')
        path_zgas = self.get_contract_path('wrapped_gas.py')
        path_aux = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')
        engine = TestEngine()

        engine.add_contract(path.replace('.py', '.nef'))
        engine.add_contract(path_zneo.replace('.py', '.nef'))
        engine.add_contract(path_zgas.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        amm_address = hash160(output)

        output, manifest = self.compile_and_save(path_zneo)
        zneo_address = hash160(output)

        output, manifest = self.compile_and_save(path_zgas)
        zgas_address = hash160(output)

        output, manifest = self.compile_and_save(path_aux)
        aux_address = hash160(output)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'set_address', zneo_address, zgas_address,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # can't remove liquidity, because the user doesn't have any
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'remove_liquidity', 10000, 0, 0, aux_address,
                                    signer_accounts=[self.OWNER_SCRIPT_HASH])

        # deploying the wrapped_neo smart contract will give 10_000_000 zNEOs to the OWNER
        result = self.run_smart_contract(engine, path_zneo, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # transferring zNEO to this auxiliary smart contract is needed, because the test engine has some limitations
        result = self.run_smart_contract(engine, path_zneo, 'transfer', self.OWNER_SCRIPT_HASH, aux_address,
                                         10_000_000 * 10 ** 8, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # deploying the wrapped_gas smart contract will give 10_000_000 zGASs to the OWNER
        result = self.run_smart_contract(engine, path_zgas, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # transferring zGAS to this auxiliary smart contract is needed, because the test engine has some limitations
        result = self.run_smart_contract(engine, path_zgas, 'transfer', self.OWNER_SCRIPT_HASH, aux_address,
                                         10_000_000 * 10 ** 8, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zNEO from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zneo_address, amm_address, transferred_amount_zneo,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zgas_address, amm_address, transferred_amount_zgas,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # adding liquidity to the pool will give you AMM tokens in return
        result = self.run_smart_contract(engine, path, 'add_liquidity',
                                         transferred_amount_zneo, transferred_amount_zgas, 0, 0, aux_address,
                                         signer_accounts=[aux_address])
        import math
        liquidity = int(math.sqrt(transferred_amount_zneo * transferred_amount_zgas))
        self.assertEqual(3, len(result))
        self.assertEqual(transferred_amount_zneo, result[0])
        self.assertEqual(transferred_amount_zgas, result[1])
        self.assertEqual(liquidity, result[2])

        # saving data to demonstrate that the value will change later
        total_supply_before = self.run_smart_contract(engine, path, 'totalSupply')
        balance_user_before = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        reserves_before = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)
        # removing liquidity from the pool will return the equivalent zNEO and zGAS that were used to fund the pool
        result = self.run_smart_contract(engine, path, 'remove_liquidity', liquidity, 0, 0, aux_address,
                                         signer_accounts=[aux_address])
        self.assertEqual(2, len(result))
        self.assertEqual(transferred_amount_zneo, result[0])
        self.assertEqual(transferred_amount_zgas, result[1])

        transfer_events = engine.get_events('Transfer', origin=amm_address)
        # add_liquidity sent a Transfer event and remove_liquidity sent another
        self.assertEqual(2, len(transfer_events))
        self.assertEqual(3, len(transfer_events[1].arguments))

        sender, receiver, amount = transfer_events[1].arguments
        if isinstance(sender, str):
            sender = String(sender).to_bytes()
        if isinstance(receiver, str):
            receiver = String(receiver).to_bytes()
        self.assertEqual(aux_address, sender)
        self.assertEqual(None, receiver)
        self.assertEqual(liquidity, amount)

        sync_events = engine.get_events('Sync', origin=amm_address)
        self.assertEqual(2, len(sync_events))
        self.assertEqual(2, len(sync_events[1].arguments))

        balance_zneo, balance_zgas = sync_events[1].arguments
        self.assertEqual(reserves_before[0] - transferred_amount_zneo, balance_zneo)
        self.assertEqual(reserves_before[1] - transferred_amount_zgas, balance_zgas)

        burn_events = engine.get_events('Burn', origin=amm_address)
        self.assertEqual(1, len(burn_events))
        self.assertEqual(3, len(burn_events[0].arguments))

        address, amount_zneo, amount_zgas = burn_events[0].arguments
        if isinstance(address, str):
            address = String(address).to_bytes()
        self.assertEqual(aux_address, address)
        self.assertEqual(transferred_amount_zneo, amount_zneo)
        self.assertEqual(transferred_amount_zgas, amount_zgas)

        # data that will be compared with the previously saved data
        total_supply_after = self.run_smart_contract(engine, path, 'totalSupply')
        balance_user_after = self.run_smart_contract(engine, path, 'balanceOf', aux_address)
        reserves_after = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)

        self.assertEqual(total_supply_before - liquidity, total_supply_after)
        self.assertEqual(balance_user_before - liquidity, balance_user_after)
        self.assertEqual(reserves_before[0] - transferred_amount_zneo, reserves_after[0])
        self.assertEqual(reserves_before[1] - transferred_amount_zgas, reserves_after[1])
        self.assertEqual(balance_user_zneo_before + transferred_amount_zneo, balance_user_zneo_after)
        self.assertEqual(balance_user_zgas_before + transferred_amount_zgas, balance_user_zgas_after)
        self.assertEqual(reserves_before[0], balance_amm_zneo_before)
        self.assertEqual(reserves_before[1], balance_amm_zgas_before)
        self.assertEqual(reserves_after[0], balance_amm_zneo_after)
        self.assertEqual(reserves_after[1], balance_amm_zgas_after)

    def test_amm_swap_zneo_to_zgas(self):
        transferred_amount_zneo = 10 * 10 ** 8
        transferred_amount_zgas = 110 * 10 ** 8

        path = self.get_contract_path('amm.py')
        path_zneo = self.get_contract_path('wrapped_neo.py')
        path_zgas = self.get_contract_path('wrapped_gas.py')
        path_aux = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')
        engine = TestEngine()

        engine.add_contract(path.replace('.py', '.nef'))
        engine.add_contract(path_zneo.replace('.py', '.nef'))
        engine.add_contract(path_zgas.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        amm_address = hash160(output)

        output, manifest = self.compile_and_save(path_zneo)
        zneo_address = hash160(output)

        output, manifest = self.compile_and_save(path_zgas)
        zgas_address = hash160(output)

        output, manifest = self.compile_and_save(path_aux)
        aux_address = hash160(output)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'set_address', zneo_address, zgas_address,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # deploying the wrapped_neo smart contract will give 10_000_000 zNEOs to the OWNER
        result = self.run_smart_contract(engine, path_zneo, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # transferring zNEO to this auxiliary smart contract is needed, because the test engine has some limitations
        result = self.run_smart_contract(engine, path_zneo, 'transfer', self.OWNER_SCRIPT_HASH, aux_address,
                                         10_000_000 * 10 ** 8, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # deploying the wrapped_gas smart contract will give 10_000_000 zGASs to the OWNER
        result = self.run_smart_contract(engine, path_zgas, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # transferring zGAS to this auxiliary smart contract is needed, because the test engine has some limitations
        result = self.run_smart_contract(engine, path_zgas, 'transfer', self.OWNER_SCRIPT_HASH, aux_address,
                                         10_000_000 * 10 ** 8, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zNEO from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zneo_address, amm_address, transferred_amount_zneo,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zgas_address, amm_address, transferred_amount_zgas,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # adding liquidity to the pool will give you AMM tokens in return
        result = self.run_smart_contract(engine, path, 'add_liquidity',
                                         transferred_amount_zneo, transferred_amount_zgas, 0, 0, aux_address,
                                         signer_accounts=[aux_address])
        import math
        liquidity = int(math.sqrt(transferred_amount_zneo * transferred_amount_zgas))
        self.assertEqual(3, len(result))
        self.assertEqual(transferred_amount_zneo, result[0])
        self.assertEqual(transferred_amount_zgas, result[1])
        self.assertEqual(liquidity, result[2])

        swapped_zneo = 1 * 10 ** 8
        # won't work, because user did not enough zNEO tokens
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'swap_tokens',
                                    swapped_zneo, 0, zneo_address, aux_address,
                                    signer_accounts=[aux_address])

        # approving the AMM contract, so that it will be able to transfer zNEO from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zneo_address, amm_address, swapped_zneo,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # saving data to demonstrate that the value will change later
        total_supply_before = self.run_smart_contract(engine, path, 'totalSupply')
        reserves_before = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)
        # swapping zneo for zgas
        result = self.run_smart_contract(engine, path, 'swap_tokens',
                                         swapped_zneo, 0, zneo_address, aux_address,
                                         signer_accounts=[aux_address], rollback_on_fault=False)
        # there is a 0.3% fee when doing a swap
        swapped_zneo_with_fee = swapped_zneo * (1000 - 3)
        swapped_zgas = swapped_zneo_with_fee * reserves_before[1] // (reserves_before[0] * 1000 + swapped_zneo_with_fee)
        self.assertEqual(swapped_zgas, result)

        # add_liquidity sent a Sync before
        transfer_events = engine.get_events('Sync')
        self.assertEqual(2, len(transfer_events))
        self.assertEqual(2, len(transfer_events[1].arguments))

        balance_zneo, balance_zgas = transfer_events[1].arguments
        self.assertEqual(reserves_before[0] + swapped_zneo, balance_zneo)
        self.assertEqual(reserves_before[1] - swapped_zgas, balance_zgas)

        transfer_events = engine.get_events('Swap')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(5, len(transfer_events[0].arguments))

        address, amount_zneo_in, amount_zgas_in, amount_zneo_out, amount_zgas_out = transfer_events[0].arguments
        if isinstance(address, str):
            address = String(address).to_bytes()
        self.assertEqual(aux_address, address)
        self.assertEqual(swapped_zneo, amount_zneo_in)
        self.assertEqual(0, amount_zgas_in)
        self.assertEqual(0, amount_zneo_out)
        self.assertEqual(swapped_zgas, amount_zgas_out)

        # data that will be compared with the previously saved data
        total_supply_after = self.run_smart_contract(engine, path, 'totalSupply')
        reserves_after = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)

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

    def test_amm_swap_zgas_to_zneo(self):
        transferred_amount_zneo = 10 * 10 ** 8
        transferred_amount_zgas = 110 * 10 ** 8

        path = self.get_contract_path('amm.py')
        path_zneo = self.get_contract_path('wrapped_neo.py')
        path_zgas = self.get_contract_path('wrapped_gas.py')
        path_aux = self.get_contract_path('examples/test_native', 'auxiliary_contract.py')
        engine = TestEngine()

        engine.add_contract(path.replace('.py', '.nef'))
        engine.add_contract(path_zneo.replace('.py', '.nef'))
        engine.add_contract(path_zgas.replace('.py', '.nef'))

        output, manifest = self.compile_and_save(path)
        amm_address = hash160(output)

        output, manifest = self.compile_and_save(path_zneo)
        zneo_address = hash160(output)

        output, manifest = self.compile_and_save(path_zgas)
        zgas_address = hash160(output)

        output, manifest = self.compile_and_save(path_aux)
        aux_address = hash160(output)

        result = self.run_smart_contract(engine, path, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'set_address', zneo_address, zgas_address,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # deploying the wrapped_neo smart contract will give 10_000_000 zNEOs to the OWNER
        result = self.run_smart_contract(engine, path_zneo, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # transferring zNEO to this auxiliary smart contract is needed, because the test engine has some limitations
        result = self.run_smart_contract(engine, path_zneo, 'transfer', self.OWNER_SCRIPT_HASH, aux_address,
                                         10_000_000 * 10 ** 8, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # deploying the wrapped_gas smart contract will give 10_000_000 zGASs to the OWNER
        result = self.run_smart_contract(engine, path_zgas, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # transferring zGAS to this auxiliary smart contract is needed, because the test engine has some limitations
        result = self.run_smart_contract(engine, path_zgas, 'transfer', self.OWNER_SCRIPT_HASH, aux_address,
                                         10_000_000 * 10 ** 8, None,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zNEO from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zneo_address, amm_address, transferred_amount_zneo,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # approving the AMM contract, so that it will be able to transfer zGAS from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zgas_address, amm_address, transferred_amount_zgas,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # adding liquidity to the pool will give you AMM tokens in return
        result = self.run_smart_contract(engine, path, 'add_liquidity',
                                         transferred_amount_zneo, transferred_amount_zgas, 0, 0, aux_address,
                                         signer_accounts=[aux_address])
        import math
        liquidity = int(math.sqrt(transferred_amount_zneo * transferred_amount_zgas))
        self.assertEqual(3, len(result))
        self.assertEqual(transferred_amount_zneo, result[0])
        self.assertEqual(transferred_amount_zgas, result[1])
        self.assertEqual(liquidity, result[2])

        swapped_zgas = 11 * 10 ** 8
        # won't work, because user did not enough zNEO tokens
        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'swap_tokens',
                                    swapped_zgas, 0, zgas_address, aux_address,
                                    signer_accounts=[aux_address])

        # approving the AMM contract, so that it will be able to transfer zNEO from test_address
        result = self.run_smart_contract(engine, path_aux, 'calling_approve',
                                         zgas_address, amm_address, swapped_zgas,
                                         signer_accounts=[aux_address],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # saving data to demonstrate that the value will change later
        total_supply_before = self.run_smart_contract(engine, path, 'totalSupply')
        reserves_before = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_before = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_before = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)
        # swapping zgas for zneo
        result = self.run_smart_contract(engine, path, 'swap_tokens',
                                         swapped_zgas, 0, zgas_address, aux_address,
                                         signer_accounts=[aux_address])
        # there is a 0.3% fee when doing a swap
        swapped_zgas_with_fee = swapped_zgas * (1000 - 3)
        swapped_zneo = swapped_zgas_with_fee * reserves_before[0] // (reserves_before[1] * 1000 + swapped_zgas_with_fee)
        self.assertEqual(swapped_zneo, result)

        # add_liquidity sent a Sync before
        transfer_events = engine.get_events('Sync')
        self.assertEqual(2, len(transfer_events))
        self.assertEqual(2, len(transfer_events[1].arguments))

        balance_zneo, balance_zgas = transfer_events[1].arguments
        self.assertEqual(reserves_before[0] - swapped_zneo, balance_zneo)
        self.assertEqual(reserves_before[1] + swapped_zgas, balance_zgas)

        transfer_events = engine.get_events('Swap')
        self.assertEqual(1, len(transfer_events))
        self.assertEqual(5, len(transfer_events[0].arguments))

        address, amount_zneo_in, amount_zgas_in, amount_zneo_out, amount_zgas_out = transfer_events[0].arguments
        if isinstance(address, str):
            address = String(address).to_bytes()
        self.assertEqual(aux_address, address)
        self.assertEqual(0, amount_zneo_in)
        self.assertEqual(swapped_zgas, amount_zgas_in)
        self.assertEqual(swapped_zneo, amount_zneo_out)
        self.assertEqual(0, amount_zgas_out)

        # data that will be compared with the previously saved data
        total_supply_after = self.run_smart_contract(engine, path, 'totalSupply')
        reserves_after = self.run_smart_contract(engine, path, 'get_reserves')
        balance_user_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', aux_address)
        balance_user_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', aux_address)
        balance_amm_zneo_after = self.run_smart_contract(engine, path_zneo, 'balanceOf', amm_address)
        balance_amm_zgas_after = self.run_smart_contract(engine, path_zgas, 'balanceOf', amm_address)

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
