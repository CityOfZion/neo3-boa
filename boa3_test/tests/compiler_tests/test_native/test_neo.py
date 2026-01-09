from dataclasses import dataclass
from typing import Self

from neo3.api import noderpc
from neo3.api.wrappers import NeoToken
from neo3.contracts.contract import CONTRACT_HASHES
from neo3.core import types
from neo3.core.cryptography import ECPoint
from neo3.network.payloads import verification
from neo3.wallet import account

from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests import annotation, boatestcase


@dataclass
class CandidateStateChangedEvent(boatestcase.BoaTestEvent):
    pubkey: ECPoint
    registered: bool
    votes: int

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


class TestNeoClass(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/native_test/neo'

    account1: account.Account
    account2: account.Account
    account_get_account_state: account.Account
    candidate_register: account.Account
    candidate_unregister: account.Account
    candidate_vote: account.Account
    candidate_get_candidates: account.Account
    candidate_get_candidate_vote: account.Account
    balance_test: account.Account
    balance_test_amount = 10

    @classmethod
    def setupTestCase(cls):
        cls.account1 = cls.node.wallet.account_new(label='test1')
        cls.account2 = cls.node.wallet.account_new(label='test2')
        cls.account_get_account_state = cls.node.wallet.account_new(label='test8')
        cls.candidate_register = cls.node.wallet.account_new(label='test3')
        cls.candidate_unregister = cls.node.wallet.account_new(label='test4')
        cls.candidate_vote = cls.node.wallet.account_new(label='test5')
        cls.candidate_get_candidates = cls.node.wallet.account_new(label='test6')
        cls.candidate_get_candidate_vote = cls.node.wallet.account_new(label='test7')
        cls.balance_test = cls.node.wallet.account_new(label='balanceTestAccount')

        super().setupTestCase()

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()

        await cls.transfer(CONTRACT_HASHES.NEO_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 1_000, 0)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.account1.script_hash, 10, 8)
        await cls.transfer(CONTRACT_HASHES.NEO_TOKEN, cls.genesis.script_hash,
                           cls.account_get_account_state.script_hash, 10, 0)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash,
                           cls.account_get_account_state.script_hash, 10, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.candidate_register.script_hash, 1010,
                           8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.candidate_unregister.script_hash,
                           3010, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.candidate_vote.script_hash, 4010, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash, cls.candidate_get_candidates.script_hash,
                           1010, 8)
        await cls.transfer(CONTRACT_HASHES.GAS_TOKEN, cls.genesis.script_hash,
                           cls.candidate_get_candidate_vote.script_hash, 1010, 8)
        await cls.transfer(CONTRACT_HASHES.NEO_TOKEN, cls.genesis.script_hash, cls.balance_test.script_hash,
                           cls.balance_test_amount, 0)

    @classmethod
    async def get_gas_per_block(cls) -> int:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host):
            receipt = await cls.node.facade.test_invoke(NeoToken().get_gas_per_block())
            return receipt.result

    @classmethod
    async def get_register_price(cls) -> int:
        async with noderpc.NeoRpcClient(cls.node.facade.rpc_host):
            receipt = await cls.node.facade.test_invoke(NeoToken().candidate_registration_price())
            return receipt.result

    async def test_get_hash(self):
        await self.set_up_contract('GetHash.py')

        expected = types.UInt160(constants.NEO_SCRIPT)
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(expected, result)

    async def test_symbol(self):
        await self.set_up_contract('Symbol.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('NEO', result)

    def test_symbol_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'SymbolTooManyArguments.py')

    async def test_decimals(self):
        await self.set_up_contract('Decimals.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(0, result)

    def test_decimals_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'DecimalsTooManyArguments.py')

    async def test_total_supply(self):
        await self.set_up_contract('TotalSupply.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(100_000_000, result)

    def test_total_supply_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'TotalSupplyTooManyArguments.py')

    async def test_balance_of(self):
        await self.set_up_contract('BalanceOf.py')

        no_balance = types.UInt160.zero()
        result, _ = await self.call('main', [no_balance], return_type=int)
        self.assertEqual(0, result)

        result, _ = await self.call('main', [self.balance_test.script_hash], return_type=int)
        self.assertEqual(self.balance_test_amount, result)

    def test_balance_of_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'BalanceOfTooManyArguments.py')

    async def test_transfer(self):
        await self.set_up_contract('Transfer.py')

        no_balance = types.UInt160.zero()
        account_1 = self.account1.script_hash
        account_2 = self.account2.script_hash
        amount = 10
        data = ['value', 123, False]

        result, _ = await self.call('main', [no_balance, account_1, amount, data], return_type=bool)
        self.assertEqual(False, result)

        # can't transfer if there is no signature, even with enough NEO
        result, _ = await self.call('main', [account_1, account_2, amount, data], return_type=bool)
        self.assertEqual(False, result)

        # signing_accounts doesn't modify WitnessScope
        # signing is not enough to pass check witness calling from test contract
        result, _ = await self.call('main',
                                    [account_1, account_2, amount, data],
                                    return_type=bool,
                                    signing_accounts=[self.account1]
                                    )

        self.assertEqual(False, result)

        signer = verification.Signer(
            account_1,
            verification.WitnessScope.CUSTOM_CONTRACTS,
            allowed_contracts=[types.UInt160(constants.NEO_SCRIPT)]
        )
        result, notifications = await self.call('main',
                                                [account_1, account_2, amount, data],
                                                return_type=bool,
                                                signers=[signer]
                                                )
        self.assertEqual(True, result)

        transfers = self.filter_events(notifications,
                                       origin=CONTRACT_HASHES.NEO_TOKEN,
                                       event_name='Transfer',
                                       notification_type=boatestcase.Nep17TransferEvent
                                       )
        self.assertEqual(1, len(transfers))
        self.assertEqual(account_1, transfers[0].source)
        self.assertEqual(account_2, transfers[0].destination)
        self.assertEqual(amount, transfers[0].amount)

    async def test_transfer_data_default(self):
        await self.set_up_contract('TransferDataDefault.py')

        no_balance = types.UInt160.zero()
        account_1 = self.account1.script_hash
        account_2 = self.account2.script_hash
        amount = 100

        result, _ = await self.call('main', [no_balance, account_1, amount], return_type=bool)
        self.assertEqual(False, result)

        # signing_accounts doesn't modify WitnessScope
        # it is not enough to pass check witness calling from test contract
        result, _ = await self.call('main',
                                    [account_1, account_2, amount],
                                    return_type=bool,
                                    signing_accounts=[self.account1]
                                    )
        self.assertEqual(False, result)

        signer = verification.Signer(
            account_1,
            verification.WitnessScope.CUSTOM_CONTRACTS,
            allowed_contracts=[types.UInt160(constants.NEO_SCRIPT)]
        )

        result, notifications = await self.call('main',
                                                [account_1, account_2, amount],
                                                return_type=bool,
                                                signers=[signer]
                                                )
        self.assertEqual(True, result)

        transfers = self.filter_events(notifications,
                                       origin=CONTRACT_HASHES.NEO_TOKEN,
                                       event_name='Transfer',
                                       notification_type=boatestcase.Nep17TransferEvent
                                       )
        self.assertEqual(1, len(transfers))
        self.assertEqual(account_1, transfers[0].source)
        self.assertEqual(account_2, transfers[0].destination)
        self.assertEqual(amount, transfers[0].amount)

    def test_transfer_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'TransferTooManyArguments.py')

    def test_transfer_too_few__parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'TransferTooFewArguments.py')

    async def test_get_gas_per_block(self):
        await self.set_up_contract('GetGasPerBlock.py')

        expected = await self.get_gas_per_block()
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(expected, result)

    async def test_unclaimed_gas(self):
        await self.set_up_contract('UnclaimedGas.py')

        latest_block = await self.get_latest_block()
        result, _ = await self.call('main',
                                    [self.account1.script_hash, latest_block.index + 1],
                                    signing_accounts=[self.account1],
                                    return_type=int,
                                    )
        self.assertGreaterEqual(result, 0)

    async def test_register_candidate(self):
        await self.set_up_contract('RegisterCandidate.py')

        candidate = self.candidate_register.script_hash
        candidate_pubkey = self.candidate_register.public_key

        signer = verification.Signer(
            candidate,
            verification.WitnessScope.CUSTOM_CONTRACTS,
            allowed_contracts=[types.UInt160(constants.NEO_SCRIPT)]
        )

        # cannot test it with a Test Invoke
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main',
                            [candidate_pubkey],
                            return_type=bool,
                            signers=[signer]
                            )
        self.assertRegex(str(context.exception), f'insufficient gas')

        result, notifications = await self.call('main',
                                    [candidate_pubkey],
                                    return_type=bool,
                                    signing_accounts=[self.candidate_register],
                                    signers=[signer]
                                    )
        self.assertEqual(True, result)

        candidate_state_changed = self.filter_events(notifications,
                                                     origin=CONTRACT_HASHES.NEO_TOKEN,
                                                     event_name='CandidateStateChanged',
                                                     notification_type=CandidateStateChangedEvent
                                                     )
        self.assertEqual(1, len(candidate_state_changed))
        event = candidate_state_changed[0]
        self.assertEqual(candidate_pubkey, event.pubkey)
        self.assertEqual(True, event.registered)
        self.assertEqual(0, event.votes)

    async def test_unregister_candidate(self):
        await self.set_up_contract('UnregisterCandidate.py')

        candidate = self.candidate_unregister.script_hash
        candidate_pubkey = self.candidate_unregister.public_key

        result, _ = await self.call('main', [candidate_pubkey], return_type=bool)
        self.assertEqual(False, result)

        # signing_accounts doesn't modify WitnessScope
        # signing with call_by_entry is not enough to pass check witness calling from test contract
        result, _ = await self.call('main',
                                    [candidate_pubkey],
                                    return_type=bool,
                                    signing_accounts=[self.candidate_unregister]
                                    )
        self.assertEqual(False, result)

        # if candidate was not registered, then it will return True
        signer = verification.Signer(
            candidate,
            verification.WitnessScope.CUSTOM_CONTRACTS,
            allowed_contracts=[types.UInt160(constants.NEO_SCRIPT)]
        )
        result, notifications = await self.call('main',
                                                [candidate_pubkey],
                                                return_type=bool,
                                                signers=[signer]
                                                )
        self.assertEqual(True, result)
        self.assertEqual(0, len(notifications))

        # registering candidate, to unregister it
        result, _ = await self.call('registerCandidate',
                                    [candidate_pubkey],
                                    return_type=bool,
                                    signing_accounts=[self.candidate_unregister],
                                    target_contract=constants.NEO_SCRIPT
                                    )
        self.assertEqual(True, result)

        signer = verification.Signer(
            candidate,
            verification.WitnessScope.CUSTOM_CONTRACTS,
            allowed_contracts=[types.UInt160(constants.NEO_SCRIPT)]
        )
        result, notifications = await self.call('main',
                                                [candidate_pubkey],
                                                return_type=bool,
                                                signers=[signer]
                                                )
        self.assertEqual(True, result)
        self.assertGreater(result, 0)

        candidate_state_changed = self.filter_events(notifications,
                                                     origin=CONTRACT_HASHES.NEO_TOKEN,
                                                     event_name='CandidateStateChanged',
                                                     notification_type=CandidateStateChangedEvent
                                                     )
        self.assertEqual(1, len(candidate_state_changed))
        event = candidate_state_changed[0]
        self.assertEqual(candidate_pubkey, event.pubkey)
        self.assertEqual(False, event.registered)
        self.assertEqual(0, event.votes)

    async def test_vote(self):
        await self.set_up_contract('Vote.py')

        candidate_pubkey = self.candidate_vote.public_key
        no_balance = self.account2.script_hash
        account_1 = self.account1.script_hash
        n_votes, _ = await self.call('balanceOf', [account_1], return_type=int, target_contract=constants.NEO_SCRIPT)

        # will fail check_witness
        result, _ = await self.call('main', [no_balance, candidate_pubkey], return_type=bool)
        self.assertEqual(False, result)

        signer_no_balance = verification.Signer(
            no_balance,
            verification.WitnessScope.CUSTOM_CONTRACTS,
            allowed_contracts=[types.UInt160(constants.NEO_SCRIPT)]
        )

        # NeoAccountState is None and will return false
        result, _ = await self.call('main',
                                    [no_balance, candidate_pubkey],
                                    signers=[signer_no_balance],
                                    return_type=bool
                                    )
        self.assertEqual(False, result)
        # accounts with NEO will make NeoAccountState not None

        signer = verification.Signer(
            account_1,
            verification.WitnessScope.CUSTOM_CONTRACTS,
            allowed_contracts=[types.UInt160(constants.NEO_SCRIPT)]
        )

        # candidate is not registered yet
        result, _ = await self.call('main', [account_1, candidate_pubkey], signers=[signer], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('registerCandidate',
                                    [candidate_pubkey],
                                    signing_accounts=[self.candidate_vote],
                                    return_type=bool,
                                    target_contract=constants.NEO_SCRIPT
                                    )
        self.assertEqual(True, result)
        # candidate was registered

        # signing_accounts doesn't modify WitnessScope
        # signing with call_by_entry is not enough to pass check witness calling from test contract
        result, _ = await self.call('main',
                                    [account_1, candidate_pubkey],
                                    signers=[signer],
                                    signing_accounts=[self.account1],
                                    return_type=bool
                                    )
        self.assertEqual(True, result)

        result, _ = await self.call('getCandidates',
                                    [],
                                    return_type=list[tuple[ECPoint, int]],
                                    target_contract=constants.NEO_SCRIPT
                                    )
        self.assertGreater(len(result), 0)
        self.assertIn((candidate_pubkey, n_votes), result)

        # remove votes from candidate
        result, _ = await self.call('un_vote',
                                    [account_1],
                                    signers=[signer],
                                    signing_accounts=[self.account1],
                                    return_type=bool
                                    )
        self.assertEqual(True, result)

        # candidate has no votes now
        result, _ = await self.call('getCandidates',
                                    [],
                                    return_type=list[tuple[ECPoint, int]],
                                    target_contract=constants.NEO_SCRIPT
                                    )
        self.assertGreater(len(result), 0)
        self.assertIn((candidate_pubkey, 0), result)

    def test_un_vote_too_many_parameters(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'UnVoteTooManyArguments.py')

    def test_un_vote_too_few_parameters(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'UnVoteTooFewArguments.py')

    async def test_get_all_candidates(self):
        await self.set_up_contract('GetAllCandidates.py')

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('main', [], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

    async def test_get_candidates(self):
        await self.set_up_contract('GetCandidates.py')

        candidate_pubkey = self.candidate_get_candidates.public_key
        candidate_and_votes = (candidate_pubkey, 0)

        # no candidate was registered
        result, _ = await self.call('main', [], return_type=list[tuple[ECPoint, int]])
        self.assertNotIn(candidate_and_votes, result)

        # registering candidate
        result, _ = await self.call('registerCandidate',
                                    [candidate_pubkey],
                                    return_type=bool,
                                    signing_accounts=[self.candidate_get_candidates],
                                    target_contract=constants.NEO_SCRIPT
                                    )
        self.assertEqual(True, result)

        # after registering one
        result, _ = await self.call('main', [], return_type=list[tuple[ECPoint, int]])
        self.assertGreater(len(result), 0)
        self.assertIn(candidate_and_votes, result)

    async def test_get_candidate_vote(self):
        await self.set_up_contract('GetCandidateVote.py')

        candidate_pubkey = self.candidate_get_candidate_vote.public_key
        account_1 = self.account1.script_hash
        n_votes, _ = await self.call('balanceOf', [account_1], return_type=int, target_contract=constants.NEO_SCRIPT)

        result, _ = await self.call('main', [candidate_pubkey], return_type=int)
        self.assertEqual(-1, result)

        # registering candidate
        result, _ = await self.call('registerCandidate',
                                    [candidate_pubkey],
                                    return_type=bool,
                                    signing_accounts=[self.candidate_get_candidate_vote],
                                    target_contract=constants.NEO_SCRIPT
                                    )
        self.assertEqual(True, result)

        # candidate was registered
        result, _ = await self.call('vote',
                                    [account_1, candidate_pubkey],
                                    return_type=bool,
                                    signing_accounts=[self.account1],
                                    target_contract=constants.NEO_SCRIPT
                                    )
        self.assertEqual(True, result)

        result, _ = await self.call('main', [candidate_pubkey], return_type=int)
        self.assertEqual(n_votes, result)

    async def test_get_committee(self):
        await self.set_up_contract('GetCommittee.py')

        default_committee = self.genesis

        result, _ = await self.call('main', [], return_type=list[ECPoint])
        self.assertGreater(len(result), 0)
        self.assertIn(default_committee.public_key, result)

    async def test_get_next_block_validators(self):
        await self.set_up_contract('GetNextBlockValidators.py')

        default_committee = self.genesis

        result, _ = await self.call('main', [], return_type=list[ECPoint])
        self.assertGreater(len(result), 0)
        self.assertIn(default_committee.public_key, result)

    async def test_get_account_state(self):
        await self.set_up_contract('GetAccountState.py')

        no_balance = types.UInt160.zero()
        account = self.account_get_account_state.script_hash
        n_votes, _ = await self.call('balanceOf', [account], return_type=int, target_contract=constants.NEO_SCRIPT)

        result, _ = await self.call('main', [no_balance], return_type=None)
        self.assertEqual(None, result)

        # TODO: neo-go in the current version of neo-mamba and boa-test-constructor can't unwrap Structs as list #86drv3zvn
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('main', [account], return_type=annotation.NeoAccountState)
            self.assertEqual(4, len(result))
            # number of votes in the account
            self.assertEqual(n_votes, result[0])
            # balance was changed after height 0
            self.assertGreater(result[1], 0)
            # who the account is voting for
            self.assertIsNone(result[2])
            self.assertGreaterEqual(result[3], 0)
        self.assertRegex(str(context.exception), "item is not of type 'StackItemType.ARRAY' but of type 'StackItemType.STRUCT'")

        # increase some blocks
        for _ in range(10):
            result, _ = await self.call('main', [no_balance], return_type=None)

        result, _ = await self.call('transfer',
                                    [account, self.genesis.script_hash, 1, None],
                                    return_type=bool,
                                    signing_accounts=[self.account_get_account_state],
                                    target_contract=constants.NEO_SCRIPT
                                    )
        self.assertEqual(True, result)
        n_votes = n_votes - 1

        # TODO: neo-go in the current version of neo-mamba and boa-test-constructor can't unwrap Structs as list #86drv3zvn
        with self.assertRaises(ValueError) as context:
            last_block = await self.get_latest_block()
            result, _ = await self.call('main', [account], return_type=annotation.NeoAccountState)
            self.assertEqual(4, len(result))
            self.assertEqual(n_votes, result[0])
            self.assertEqual(last_block.index, result[1])
            self.assertIsNone(result[2])
            self.assertGreaterEqual(result[3], 0)
        self.assertRegex(str(context.exception), "item is not of type 'StackItemType.ARRAY' but of type 'StackItemType.STRUCT'")

    async def test_get_committee_address(self):
        expected_output = (
            Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        output, _ = self.assertCompile('GetCommitteeAddress.py')
        self.assertEqual(expected_output, output)

    async def test_get_register_price(self):
        await self.set_up_contract('GetRegisterPrice.py')

        register_price = await self.get_register_price()
        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(register_price, result)

    def test_overwrite_hash(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'CompilerErrorOverwriteHash.py')
