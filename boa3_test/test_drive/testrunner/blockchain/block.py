from typing import Any, Self

from boa3.internal.neo3.core.types import UInt256
from boa3_test.test_drive.model.network.payloads.testblock import TestBlock
from boa3_test.test_drive.model.network.payloads.witness import Witness
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp import utils
from boa3_test.test_drive.testrunner.blockchain.transaction import TestRunnerTransaction


class TestRunnerBlock(TestBlock):
    def __init__(self):
        self._transactions: list[TestRunnerTransaction] = []
        super().__init__()
        self._hash: UInt256 = UInt256.zero()
        self._size = 0
        self._version = 0
        self._previous_block_hash = UInt256.zero()
        self._merkle_root = UInt256.zero()
        self._nonce = 0
        self._primary_index = 0
        self._next_consensus: Account = None
        self._witnesses: list[Witness] = []

    @property
    def hash(self) -> UInt256:
        return self._hash

    @property
    def size(self) -> int:
        return self._size

    @property
    def version(self) -> int:
        return self._version

    @property
    def previous_block_hash(self) -> UInt256:
        return self._previous_block_hash

    @property
    def merkle_root(self) -> UInt256:
        return self._merkle_root

    @property
    def nonce(self) -> int:
        return self._nonce

    @property
    def primary_index(self) -> int:
        return self._primary_index

    @property
    def next_consensus(self) -> Account:
        return self._next_consensus

    @property
    def witnesses(self) -> list[Witness]:
        return self._witnesses.copy()

    @property
    def transactions(self) -> list[TestRunnerTransaction]:
        return self._transactions.copy()

    def to_json(self) -> dict[str, Any]:
        json_block = super().to_json()

        # timestamp in this implementation is exported as time
        time = json_block.pop('timestamp')
        json_block['time'] = time

        return json_block

    @classmethod
    def from_json(cls, json: dict[str, Any], *args, **kwargs) -> Self:
        from boa3.internal.neo import from_hex_str

        block: Self = super().from_json(json)

        if 'neoxp_config' in kwargs:
            neoxp_config = kwargs['neoxp_config']
        elif len(args) > 0:
            neoxp_config = args[0]
        else:
            neoxp_config = None

        block._size = int(json['size'])
        block._version = int(json['version'])
        block._previous_block_hash = UInt256(from_hex_str(json['previousblockhash']))
        block._merkle_root = UInt256(from_hex_str(json['merkleroot']))
        block._timestamp = int(json['time'])
        block._nonce = int(json['nonce'], base=16)
        block._primary_index = int(json['primary'])
        next_consensus = json['nextconsensus']
        block._next_consensus = (utils.get_account_from_script_hash_or_id(neoxp_config, next_consensus)
                                 if neoxp_config is not None
                                 else next_consensus
                                 )
        block._witnesses = [Witness.from_json(js) for js in json['witnesses']]
        block._transactions = [TestRunnerTransaction.from_json(js, *args, **kwargs) for js in json['tx']]

        return block
