from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive import neoxp
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestNeoClass(BoaTest):
    default_folder: str = 'test_sc/native_test/neo'
    NEO_CONTRACT_NAME = 'NeoToken'

    def test_get_hash(self):
        path, _ = self.get_deploy_file_paths('GetHash.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(constants.NEO_SCRIPT)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_symbol(self):
        path, _ = self.get_deploy_file_paths('Symbol.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append('NEO')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_symbol_too_many_parameters(self):
        path = self.get_contract_path('SymbolTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_decimals(self):
        path, _ = self.get_deploy_file_paths('Decimals.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_decimals_too_many_parameters(self):
        path = self.get_contract_path('DecimalsTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_total_supply(self):
        path, _ = self.get_deploy_file_paths('TotalSupply.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(100_000_000)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_total_supply_too_many_parameters(self):
        path = self.get_contract_path('TotalSupplyTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_balance_of(self):
        path, _ = self.get_deploy_file_paths('BalanceOf.py')
        test_account_1 = neoxp.utils.get_account_by_name('testAccount1').script_hash.to_array()
        test_account_2 = neoxp.utils.get_account_by_name('testAccount2').script_hash.to_array()
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', test_account_2))
        expected_results.append(0)

        runner.add_neo(test_account_1, 10)
        invokes.append(runner.call_contract(path, 'main', test_account_1))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_balance_of_too_many_parameters(self):
        path = self.get_contract_path('BalanceOfTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_transfer(self):
        path, _ = self.get_deploy_file_paths('Transfer.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        account = neoxp.utils.get_account_by_name('testAccount1')
        account_1 = account.script_hash.to_array()
        account_2 = neoxp.utils.get_account_by_name('testAccount2').script_hash.to_array()
        amount = 10000

        runner.add_neo(account_1, amount)
        invokes.append(runner.call_contract(path, 'main', account_2, account_1, amount, ['value', 123, False]))
        expected_results.append(False)

        # can't transfer if there is no signature, even with enough GAS
        invokes.append(runner.call_contract(path, 'main', account_1, account_2, amount, ['value', 123, False]))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        # TestRunner doesn't have WitnessScope modifier
        # signing is not enough to pass check witness calling from test contract
        invokes.append(runner.call_contract(path, 'main', account_1, account_2, amount, ['value', 123, False]))
        expected_results.append(False)

        invokes.append(runner.call_contract(self.NEO_CONTRACT_NAME, 'transfer',
                                            account_1, account_2, amount, ['value', 123, False]))
        expected_results.append(True)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_transfer_data_default(self):
        path, _ = self.get_deploy_file_paths('TransferDataDefault.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        account = neoxp.utils.get_account_by_name('testAccount1')
        account_1 = account.script_hash.to_array()
        account_2 = neoxp.utils.get_account_by_name('testAccount2').script_hash.to_array()
        amount = 100

        runner.add_neo(account_1, amount)
        invokes.append(runner.call_contract(path, 'main', account_2, account_1, amount))
        expected_results.append(False)
        runner.update_contracts(export_checkpoint=True)

        # TestRunner doesn't have WitnessScope modifier
        # signing is not enough to pass check witness calling from test contract
        invokes.append(runner.call_contract(path, 'main', account_1, account_2, amount))
        expected_results.append(False)

        invokes.append(runner.call_contract(self.NEO_CONTRACT_NAME, 'transfer', account_1, account_2, amount, None))
        expected_results.append(True)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_transfer_too_many_parameters(self):
        path = self.get_contract_path('TransferTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_transfer_too_few__parameters(self):
        path = self.get_contract_path('TransferTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_get_gas_per_block(self):
        path, _ = self.get_deploy_file_paths('GetGasPerBlock.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(5 * 10 ** 8)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_unclaimed_gas(self):
        path, _ = self.get_deploy_file_paths('UnclaimedGas.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        contract_call = runner.call_contract(path, 'main', bytes(20), 0)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')
        self.assertIsInstance(contract_call.result, int)

    def test_register_candidate(self):
        path, _ = self.get_deploy_file_paths('RegisterCandidate.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        candidate = neoxp.utils.get_account_by_name('testAccount1')
        candidate_pubkey = bytes.fromhex('035F34EF4B4704C68617C427B3A3059BF0AF86E9AF46992588C6605C2B87366F16')
        candidate_script_hash = candidate.script_hash.to_array()
        register_gas_price = 1_000
        runner.add_gas(candidate_script_hash, (register_gas_price + 1) * 10 ** 8)  # +1 to make sure it has enough gas

        invokes.append(runner.call_contract(path, 'main', candidate_pubkey))
        expected_results.append(False)
        runner.update_contracts(export_checkpoint=True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        # TestRunner doesn't have WitnessScope modifier
        # signing is not enough to pass check witness calling from test contract
        invokes.append(runner.call_contract(path, 'main', candidate_pubkey))
        expected_results.append(False)

        runner.execute(account=candidate)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        # cannot test it with a Test Invoke
        runner.call_contract(self.NEO_CONTRACT_NAME, 'registerCandidate', candidate_pubkey)
        # expected_results.append(True)
        invoke = runner.run_contract(self.NEO_CONTRACT_NAME, 'registerCandidate', candidate_pubkey,
                                     account=candidate)

        runner.execute(account=candidate)
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.INSUFFICIENT_GAS)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_tx = runner.get_transaction_result(invoke.tx_id)
        tx_executions = invoke_tx.executions
        self.assertEqual(1, len(tx_executions))
        self.assertEqual(1, len(tx_executions[0].result_stack))
        self.assertEqual(True, invoke_tx.executions[0].result_stack[0])

    def test_unregister_candidate(self):
        path, _ = self.get_deploy_file_paths('UnregisterCandidate.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        candidate = neoxp.utils.get_account_by_name('testAccount1')
        candidate_pubkey = bytes.fromhex('035F34EF4B4704C68617C427B3A3059BF0AF86E9AF46992588C6605C2B87366F16')
        candidate_script_hash = candidate.script_hash.to_array()
        unregister_gas_price = 1_000
        runner.add_gas(candidate_script_hash, (unregister_gas_price + 1) * 10 ** 8)  # +1 to make sure it has enough gas

        invokes.append(runner.call_contract(path, 'main', candidate_pubkey))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        # TestRunner doesn't have WitnessScope modifier
        # signing is not enough to pass check witness calling from test contract
        invokes.append(runner.call_contract(path, 'main', candidate_pubkey))
        expected_results.append(False)

        invokes.append(runner.call_contract(self.NEO_CONTRACT_NAME, 'unregisterCandidate', candidate_pubkey))
        expected_results.append(True)

        runner.execute(account=candidate)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_vote(self):
        path, _ = self.get_deploy_file_paths('Vote.py')
        path_get, _ = self.get_deploy_file_paths('GetCandidates.py')

        runner = BoaTestRunner(runner_id=self.method_name())
        runner.deploy_contract(path_get)

        invokes = []
        expected_results = []

        candidate = neoxp.utils.get_account_by_name('testAccount1')
        candidate_pubkey = bytes.fromhex('035F34EF4B4704C68617C427B3A3059BF0AF86E9AF46992588C6605C2B87366F16')
        candidate_script_hash = candidate.script_hash.to_array()

        n_votes = 100
        account = neoxp.utils.get_account_by_name('testAccount2')
        account_script_hash = account.script_hash.to_array()

        register_gas_price = 1_000
        runner.add_gas(candidate_script_hash, (register_gas_price + 1) * 10 ** 8)  # +1 to make sure it has enough gas

        # will fail check_witness
        invokes.append(runner.call_contract(path, 'main', account_script_hash, candidate_pubkey))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        # NeoAccountState is None and will return false
        invokes.append(runner.call_contract(path, 'main', account_script_hash, candidate_pubkey))
        expected_results.append(False)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        # adding NEO to the account will make NeoAccountState not None
        runner.add_neo(account_script_hash, n_votes)

        # candidate is not registered yet
        invokes.append(runner.call_contract(path, 'main', account_script_hash, candidate_pubkey))
        expected_results.append(False)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        invoke = runner.run_contract(self.NEO_CONTRACT_NAME, 'registerCandidate', candidate_pubkey,
                                     account=candidate)

        # candidate was registered
        # TestRunner doesn't have WitnessScope modifier
        # signing is not enough to pass check witness calling from test contract
        invokes.append(runner.call_contract(path, 'main', account_script_hash, candidate_pubkey))
        expected_results.append(False)

        invokes.append(runner.call_contract(self.NEO_CONTRACT_NAME, 'vote', account_script_hash, candidate_pubkey))
        expected_results.append(True)

        get_candidates_call_1 = runner.call_contract(path_get, 'main')

        # remove votes from candidate
        # TestRunner doesn't have WitnessScope modifier
        # signing is not enough to pass check witness calling from test contract
        invokes.append(runner.call_contract(path, 'un_vote', account_script_hash))
        expected_results.append(False)

        invokes.append(runner.call_contract(self.NEO_CONTRACT_NAME, 'vote', account_script_hash, None))
        expected_results.append(True)

        # candidate has no votes now
        get_candidates_call_2 = runner.call_contract(path_get, 'main')

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_tx = runner.get_transaction_result(invoke.tx_id)
        tx_executions = invoke_tx.executions
        self.assertEqual(1, len(tx_executions))
        self.assertEqual(1, len(tx_executions[0].result_stack))
        self.assertEqual(True, invoke_tx.executions[0].result_stack[0])

        result = get_candidates_call_1.result
        self.assertEqual(1, len(result))
        self.assertEqual(candidate_pubkey, result[0][0])
        self.assertEqual(n_votes, result[0][1])

        result = get_candidates_call_2.result
        self.assertEqual(1, len(result))
        self.assertEqual(candidate_pubkey, result[0][0])
        self.assertEqual(0, result[0][1])

    def test_un_vote_too_many_parameters(self):
        path = self.get_contract_path('UnVoteTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_un_vote_too_few_parameters(self):
        path = self.get_contract_path('UnVoteTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_get_all_candidates(self):
        path = self.get_contract_path('GetAllCandidates.py')
        self.compile_and_save(path)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        # no candidate was registered
        invoke = runner.call_contract(path, 'main')

        runner.execute()  # getting result of multiple iterators is failing
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        result = invoke.result
        self.assertEqual(0, len(result))

        candidate = neoxp.utils.get_account_by_name('testAccount1')
        candidate_pubkey = bytes.fromhex('035F34EF4B4704C68617C427B3A3059BF0AF86E9AF46992588C6605C2B87366F16')
        candidate_script_hash = candidate.script_hash.to_array()
        register_gas_price = 1_000
        runner.add_gas(candidate_script_hash, (register_gas_price + 1) * 10 ** 8)  # +1 to make sure it has enough gas

        runner.run_contract(self.NEO_CONTRACT_NAME, 'registerCandidate', candidate_pubkey,
                            account=candidate)

        # after registering one
        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        result = invoke.result
        self.assertEqual(1, len(result))
        self.assertEqual(candidate_pubkey, result[0][0])
        self.assertEqual(0, result[0][1])

    def test_get_candidates(self):
        path, _ = self.get_deploy_file_paths('GetCandidates.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        # no candidate was registered
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        candidate = neoxp.utils.get_account_by_name('testAccount1')
        candidate_pubkey = bytes.fromhex('035F34EF4B4704C68617C427B3A3059BF0AF86E9AF46992588C6605C2B87366F16')
        candidate_script_hash = candidate.script_hash.to_array()
        register_gas_price = 1_000
        runner.add_gas(candidate_script_hash, (register_gas_price + 1) * 10 ** 8)  # +1 to make sure it has enough gas

        register_invoke = runner.run_contract(self.NEO_CONTRACT_NAME, 'registerCandidate', candidate_pubkey,
                                              account=candidate)

        # after registering one
        invoke = runner.call_contract(path, 'main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_tx = runner.get_transaction_result(register_invoke.tx_id)
        tx_executions = invoke_tx.executions
        self.assertEqual(1, len(tx_executions))
        self.assertEqual(1, len(tx_executions[0].result_stack))
        self.assertEqual(True, invoke_tx.executions[0].result_stack[0])

        result = invoke.result
        self.assertEqual(1, len(result))
        self.assertEqual(candidate_pubkey, result[0][0])
        self.assertEqual(0, result[0][1])

    def test_get_candidate_vote(self):
        path, _ = self.get_deploy_file_paths('GetCandidateVote.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        candidate = neoxp.utils.get_account_by_name('testAccount1')
        candidate_pubkey = bytes.fromhex('035F34EF4B4704C68617C427B3A3059BF0AF86E9AF46992588C6605C2B87366F16')
        candidate_script_hash = candidate.script_hash.to_array()

        n_votes = 100
        account = neoxp.utils.get_account_by_name('testAccount2')
        account_script_hash = account.script_hash.to_array()

        register_gas_price = 1_000
        runner.add_gas(candidate_script_hash, (register_gas_price + 1) * 10 ** 8)  # +1 to make sure it has enough gas

        # will fail check_witness
        invokes.append(runner.call_contract(path, 'main', candidate_pubkey))
        expected_results.append(-1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        runner.add_neo(account_script_hash, n_votes)

        invoke = runner.run_contract(self.NEO_CONTRACT_NAME, 'registerCandidate', candidate_pubkey,
                                     account=candidate)

        # candidate was registered
        invokes.append(runner.call_contract(self.NEO_CONTRACT_NAME, 'vote', account_script_hash, candidate_pubkey))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', candidate_pubkey))
        expected_results.append(n_votes)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_tx = runner.get_transaction_result(invoke.tx_id)
        tx_executions = invoke_tx.executions
        self.assertEqual(1, len(tx_executions))
        self.assertEqual(1, len(tx_executions[0].result_stack))
        self.assertEqual(True, invoke_tx.executions[0].result_stack[0])

    def test_get_committee(self):
        path, _ = self.get_deploy_file_paths('GetCommittee.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        default_committee = neoxp.utils.get_account_by_name('node1')
        default_council = [
            # default_committee.public_key,  # not implemented
            bytes.fromhex('027C84B056C26A7B2458471E6DCF6752EDD96B96887D783334E351DDFE13C4BCA2'),
        ]

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        result = invoke.result
        is_committee_member = True
        for pubkey in default_council:
            if pubkey not in result:
                is_committee_member = False
        self.assertEqual(True, is_committee_member)

    def test_get_next_block_validators(self):
        path, _ = self.get_deploy_file_paths('GetNextBlockValidators.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        default_committee = neoxp.utils.get_account_by_name('node1')
        consensus_nodes = [
            # default_committee.public_key,  # not implemented
            bytes.fromhex('027C84B056C26A7B2458471E6DCF6752EDD96B96887D783334E351DDFE13C4BCA2'),
        ]

        invoke = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        result = invoke.result
        is_consensus_node = True
        for pubkey in consensus_nodes:
            if pubkey not in result:
                is_consensus_node = False
        self.assertEqual(True, is_consensus_node)

    def test_get_account_state(self):
        path, _ = self.get_deploy_file_paths('GetAccountState.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        account = neoxp.utils.get_account_by_name('testAccount1')
        account_script_hash = account.script_hash.to_array()

        invokes.append(runner.call_contract(path, 'main', account_script_hash))
        expected_results.append(None)

        # adding votes
        votes = 10000
        runner.add_neo(account_script_hash, votes)
        invoke = runner.call_contract(path, 'main', account_script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        result = invoke.result
        self.assertEqual(3, len(result))
        # number of votes in the account
        self.assertEqual(votes, result[0])
        # balance was changed at height 0
        self.assertEqual(2, result[1])
        # who the account is voting for
        self.assertIsNone(result[2])

        runner.increase_block(10)
        other_account = neoxp.utils.get_account_by_name('testAccount2')
        other_account_script_hash = other_account.script_hash.to_array()

        runner.call_contract(self.NEO_CONTRACT_NAME, 'transfer',
                             account_script_hash, other_account_script_hash, 1, None)
        votes = votes - 1

        invoke = runner.call_contract(path, 'main', account_script_hash)

        runner.execute(account=account)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=f'{runner.error}\n{runner.cli_log}')

        result = invoke.result
        self.assertEqual(3, len(result))
        self.assertEqual(votes, result[0])
        self.assertEqual(2, result[1])
        self.assertIsNone(result[2])
