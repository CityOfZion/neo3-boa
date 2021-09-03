from boa3.exception import CompilerError
from boa3.neo import from_hex_str
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNeoClass(BoaTest):

    default_folder: str = 'test_sc/native_test/neo'

    def test_symbol(self):
        path = self.get_contract_path('Symbol.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual('NEO', result)

    def test_symbol_too_many_parameters(self):
        path = self.get_contract_path('SymbolTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_decimals(self):
        path = self.get_contract_path('Decimals.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(0, result)

    def test_decimals_too_many_parameters(self):
        path = self.get_contract_path('DecimalsTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_total_supply(self):
        path = self.get_contract_path('TotalSupply.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(100_000_000, result)

    def test_total_supply_too_many_parameters(self):
        path = self.get_contract_path('TotalSupplyTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_balance_of(self):
        path = self.get_contract_path('BalanceOf.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', bytes(range(20)))
        self.assertEqual(0, result)

        engine.add_neo(bytes(range(20)), 10)
        result = self.run_smart_contract(engine, path, 'main', bytes(range(20)))
        self.assertEqual(10, result)

    def test_balance_of_too_many_parameters(self):
        path = self.get_contract_path('BalanceOfTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_transfer(self):
        path = self.get_contract_path('Transfer.py')
        engine = TestEngine()

        account_1 = bytes(range(20))
        account_2 = bytes(range(20)[::-1])
        amount = 10000

        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount, ['value', 123, False])
        self.assertEqual(False, result)

        engine.add_neo(account_1, amount)
        # can't transfer if there is no signature, even with enough GAS
        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount, ['value', 123, False])
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount, ['value', 123, False],
                                         signer_accounts=[account_1])
        self.assertEqual(True, result)

    def test_transfer_data_default(self):
        path = self.get_contract_path('TransferDataDefault.py')
        engine = TestEngine()

        account_1 = bytes(range(20))
        account_2 = bytes(range(20)[::-1])
        amount = 100

        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount)
        self.assertEqual(False, result)

        engine.add_neo(account_1, amount)
        result = self.run_smart_contract(engine, path, 'main', account_1, account_2, amount,
                                         signer_accounts=[account_1])
        self.assertEqual(True, result)

    def test_transfer_too_many_parameters(self):
        path = self.get_contract_path('TransferTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_transfer_too_few__parameters(self):
        path = self.get_contract_path('TransferTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_get_gas_per_block(self):
        path = self.get_contract_path('GetGasPerBlock.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(5 * 10 ** 8, result)

    def test_unclaimed_gas(self):
        path = self.get_contract_path('UnclaimedGas.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', bytes(20), 0)
        self.assertIsInstance(result, int)

    def test_register_candidate(self):
        path = self.get_contract_path('RegisterCandidate.py')
        engine = TestEngine()

        candidate_pubkey = bytes.fromhex('0296852e74830f48185caec9980d21dee5e8bee3da97d712123c19ee01c2d3f3ae')
        candidate_scripthash = from_hex_str('a8de26eb4931c674d31885acf722bd82e6bcd06d')
        result = self.run_smart_contract(engine, path, 'main', candidate_pubkey)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', candidate_pubkey,
                                         signer_accounts=[candidate_scripthash])
        self.assertEqual(True, result)

    def test_unregister_candidate(self):
        path = self.get_contract_path('UnregisterCandidate.py')
        engine = TestEngine()

        candidate_pubkey = bytes.fromhex('0296852e74830f48185caec9980d21dee5e8bee3da97d712123c19ee01c2d3f3ae')
        candidate_scripthash = from_hex_str('a8de26eb4931c674d31885acf722bd82e6bcd06d')
        result = self.run_smart_contract(engine, path, 'main', candidate_pubkey)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', candidate_pubkey, signer_accounts=[candidate_scripthash])
        self.assertEqual(True, result)

    def test_vote(self):
        path = self.get_contract_path('Vote.py')
        engine = TestEngine()

        account = bytes(range(20))
        n_votes = 100
        candidate_pubkey = bytes.fromhex('0296852e74830f48185caec9980d21dee5e8bee3da97d712123c19ee01c2d3f3ae')
        # will fail check_witness
        result = self.run_smart_contract(engine, path, 'main', account, candidate_pubkey)
        self.assertEqual(False, result)

        # NeoAccountState is None and will return false
        result = self.run_smart_contract(engine, path, 'main', account, candidate_pubkey, signer_accounts=[account])
        self.assertEqual(False, result)

        # adding NEO to the account will make NeoAccountState not None
        engine.add_neo(account, n_votes)
        # it's possible to vote for no one
        result = self.run_smart_contract(engine, path, 'main', account, None, signer_accounts=[account])
        self.assertEqual(True, result)

        # candidate is not registered yet
        result = self.run_smart_contract(engine, path, 'main', account, candidate_pubkey, signer_accounts=[account])
        self.assertEqual(False, result)

        path_register = self.get_contract_path('RegisterCandidate.py')
        candidate_pubkey = bytes.fromhex('0296852e74830f48185caec9980d21dee5e8bee3da97d712123c19ee01c2d3f3ae')
        candidate_scripthash = from_hex_str('a8de26eb4931c674d31885acf722bd82e6bcd06d')
        self.run_smart_contract(engine, path_register, 'main', candidate_pubkey,
                                signer_accounts=[candidate_scripthash])

        # candidate was registered
        result = self.run_smart_contract(engine, path, 'main', account, candidate_pubkey, signer_accounts=[account])
        self.assertEqual(True, result)

        path_get = self.get_contract_path('GetCandidates.py')
        result = self.run_smart_contract(engine, path_get, 'main')
        self.assertEqual(1, len(result))
        self.assertEqual(candidate_pubkey, result[0][0])
        self.assertEqual(n_votes, result[0][1])

    def test_get_candidates(self):
        path = self.get_contract_path('GetCandidates.py')
        engine = TestEngine()

        # no candidate was registered
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(0, len(result))

        path_register = self.get_contract_path('RegisterCandidate.py')
        candidate_pubkey = bytes.fromhex('0296852e74830f48185caec9980d21dee5e8bee3da97d712123c19ee01c2d3f3ae')
        candidate_scripthash = from_hex_str('a8de26eb4931c674d31885acf722bd82e6bcd06d')
        self.run_smart_contract(engine, path_register, 'main', candidate_pubkey,
                                signer_accounts=[candidate_scripthash])

        # after registering one
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(1, len(result))
        self.assertEqual(candidate_pubkey, result[0][0])
        self.assertEqual(0, result[0][1])

    def test_get_committee(self):
        path = self.get_contract_path('GetCommittee.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        default_council = [
            bytes.fromhex('03b209fd4f53a7170ea4444e0cb0a6bb6a53c2bd016926989cf85f9b0fba17a70c'),
            bytes.fromhex('02486fd15702c4490a26703112a5cc1d0923fd697a33406bd5a1c00e0013b09a70'),
            bytes.fromhex('02ca0e27697b9c248f6f16e085fd0061e26f44da85b58ee835c110caa5ec3ba554'),
            bytes.fromhex('024c7b7fb6c310fccf1ba33b082519d82964ea93868d676662d4a59ad548df0e7d'),
            bytes.fromhex('03b8d9d5771d8f513aa0869b9cc8d50986403b78c6da36890638c3d46a5adce04a'),
            bytes.fromhex('02df48f60e8f3e01c48ff40b9b7f1310d7a8b2a193188befe1c2e3df740e895093'),
            bytes.fromhex('02aaec38470f6aad0042c6e877cfd8087d2676b0f516fddd362801b9bd3936399e'),
            bytes.fromhex('023a36c72844610b4d34d1968662424011bf783ca9d984efa19a20babf5582f3fe'),
            bytes.fromhex('03708b860c1de5d87f5b151a12c2a99feebd2e8b315ee8e7cf8aa19692a9e18379'),
            bytes.fromhex('03c6aa6e12638b36e88adc1ccdceac4db9929575c3e03576c617c49cce7114a050'),
            bytes.fromhex('03204223f8c86b8cd5c89ef12e4f0dbb314172e9241e30c9ef2293790793537cf0'),
            bytes.fromhex('02a62c915cf19c7f19a50ec217e79fac2439bbaad658493de0c7d8ffa92ab0aa62'),
            bytes.fromhex('03409f31f0d66bdc2f70a9730b66fe186658f84a8018204db01c106edc36553cd0'),
            bytes.fromhex('0288342b141c30dc8ffcde0204929bb46aed5756b41ef4a56778d15ada8f0c6654'),
            bytes.fromhex('020f2887f41474cfeb11fd262e982051c1541418137c02a0f4961af911045de639'),
            bytes.fromhex('0222038884bbd1d8ff109ed3bdef3542e768eef76c1247aea8bc8171f532928c30'),
            bytes.fromhex('03d281b42002647f0113f36c7b8efb30db66078dfaaa9ab3ff76d043a98d512fde'),
            bytes.fromhex('02504acbc1f4b3bdad1d86d6e1a08603771db135a73e61c9d565ae06a1938cd2ad'),
            bytes.fromhex('0226933336f1b75baa42d42b71d9091508b638046d19abd67f4e119bf64a7cfb4d'),
            bytes.fromhex('03cdcea66032b82f5c30450e381e5295cae85c5e6943af716cc6b646352a6067dc'),
            bytes.fromhex('02cd5a5547119e24feaa7c2a0f37b8c9366216bab7054de0065c9be42084003c8a'),
        ]
        is_committee_member = True
        for pubkey in default_council:
            if pubkey not in result:
                is_committee_member = False
        self.assertEqual(True, is_committee_member)

    def test_get_next_block_validators(self):
        path = self.get_contract_path('GetNextBlockValidators.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        consensus_nodes = [
            bytes.fromhex('03b209fd4f53a7170ea4444e0cb0a6bb6a53c2bd016926989cf85f9b0fba17a70c'),
            bytes.fromhex('02486fd15702c4490a26703112a5cc1d0923fd697a33406bd5a1c00e0013b09a70'),
            bytes.fromhex('02ca0e27697b9c248f6f16e085fd0061e26f44da85b58ee835c110caa5ec3ba554'),
            bytes.fromhex('024c7b7fb6c310fccf1ba33b082519d82964ea93868d676662d4a59ad548df0e7d'),
            bytes.fromhex('03b8d9d5771d8f513aa0869b9cc8d50986403b78c6da36890638c3d46a5adce04a'),
            bytes.fromhex('02df48f60e8f3e01c48ff40b9b7f1310d7a8b2a193188befe1c2e3df740e895093'),
            bytes.fromhex('02aaec38470f6aad0042c6e877cfd8087d2676b0f516fddd362801b9bd3936399e'),
        ]
        is_consensus_node = True
        for pubkey in consensus_nodes:
            if pubkey not in result:
                is_consensus_node = False
        self.assertEqual(True, is_consensus_node)

    def test_get_account_state(self):
        path = self.get_contract_path('GetAccountState.py')
        engine = TestEngine()

        account = bytes(range(20))
        result = self.run_smart_contract(engine, path, 'main', account)
        self.assertIsNone(result)

        # adding votes
        votes = 10000
        engine.add_neo(account, votes)
        result = self.run_smart_contract(engine, path, 'main', account)
        self.assertEqual(3, len(result))
        # number of votes in the account
        self.assertEqual(votes, result[0])
        # balance was changed at height 0
        self.assertEqual(0, result[1])
        # who the account is voting for
        self.assertIsNone(result[2])

        engine.increase_block(10)
        other_account = bytes(20)

        path_transfer = self.get_contract_path('Transfer.py')

        self.run_smart_contract(engine, path_transfer, 'main', account, other_account, 1, None,
                                signer_accounts=[account])
        votes = votes - 1

        result = self.run_smart_contract(engine, path, 'main', account)
        self.assertEqual(3, len(result))
        self.assertEqual(votes, result[0])
        self.assertEqual(10, result[1])
        self.assertIsNone(result[2])
