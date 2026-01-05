import time
from typing import Any, Self

from boa3.internal.neo3.core.types import UInt256
from boa3_test.tests.test_classes.transaction import Transaction


class Block:
    def __init__(self, index: int):
        self._index: int = 0
        self._timestamp: int = 0
        self._hash: UInt256 | None = None
        self._transactions: list[Transaction] = []

        # time() returns timestamp in nanoseconds and Neo uses timestamp in milliseconds
        self._timestamp: int = int(time.time_ns() / 1_000_000)
        self._index: int = index

    @property
    def index(self) -> int:
        return self._index

    @property
    def timestamp(self) -> int:
        return self._timestamp

    def get_transactions(self) -> list[Transaction]:
        """
        Gets a list of the block transactions. Changes in those transactions don't affect the ones inside the block.

        :return: the block transactions
        :rtype: list[Transaction]
        """
        return [tx.copy() for tx in self._transactions]

    def add_transaction(self, tx: Transaction):
        if all(block_tx != tx for block_tx in self._transactions):
            self._transactions.append(tx)

    @property
    def hash(self) -> bytes | None:
        if self._hash is None:
            return None
        else:
            return self._hash.to_array()

    def to_json(self) -> dict[str, Any]:
        json_block = {
            'index': self._index,
            'timestamp': self._timestamp,
            'transactions': [tx.to_json() for tx in self._transactions]
        }

        if self._hash is not None:
            json_block['hash'] = str(self._hash)

        return json_block

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        block = object.__new__(cls)

        if 'index' in json:
            block._index = int(json['index'])
        else:
            block._index = 0

        if 'timestamp' in json:
            block._timestamp = int(json['timestamp'])
        else:
            block._timestamp = 0

        if 'transactions' in json:
            tx_json = json['transactions']
            if not isinstance(tx_json, list):
                tx_json = [tx_json]
        else:
            tx_json = []
        block._transactions = [Transaction.from_json(js) for js in tx_json]

        if 'hash' in json and isinstance(json['hash'], str):
            block._hash = UInt256.from_string(json['hash'])
        else:
            block._hash = None

        # 'index' and 'timestamp' fields are required
        block._index = int(json['index'])
        block._timestamp = int(json['timestamp'])

        return block

    def __repr__(self) -> str:
        return str(self._hash) if self._hash is not None else str(self._index)
