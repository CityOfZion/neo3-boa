from __future__ import annotations

from typing import Any, Dict, List, Optional

from boa3.neo import from_hex_str
from boa3.neo3.core.types import UInt256
from boa3_test.tests.test_classes.transaction import Transaction


class Block:
    def __init__(self, index: int):
        import time
        self._index: int = index
        # time() returns timestamp in nanoseconds and Neo uses timestamp in milliseconds
        self._timestamp: int = int(time.time_ns() / 1_000_000)
        self._hash: Optional[UInt256] = None
        self._transactions: List[Transaction] = []

    @property
    def index(self) -> int:
        return self._index

    @property
    def timestamp(self) -> int:
        return self._timestamp

    def get_transactions(self) -> List[Transaction]:
        """
        Gets a list of the block transactions. Changes in those transactions don't affect the ones inside the block.

        :return: the block transactions
        :rtype: List[Transaction]
        """
        return [tx.copy() for tx in self._transactions]

    def add_transaction(self, tx: Transaction):
        if all(block_tx != tx for block_tx in self._transactions):
            self._transactions.append(tx)

    @property
    def hash(self) -> Optional[bytes]:
        if self._hash is None:
            return None
        else:
            return self._hash.to_array()

    def to_json(self) -> Dict[str, Any]:
        return {
            'index': self._index,
            'timestamp': self._timestamp,
            'transactions': [tx.to_json() for tx in self._transactions]
        }

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> Block:
        # 'index' and 'timestamp' fields are required
        block = cls(int(json['index']))
        block._timestamp = int(json['timestamp'])

        if 'transactions' in json:
            tx_json = json['transactions']
            if not isinstance(tx_json, list):
                tx_json = [tx_json]
            block._transactions = [Transaction.from_json(js) for js in tx_json]

        if 'hash' in json and isinstance(json['hash'], str):
            block._hash = UInt256(from_hex_str(json['hash']))

        return block
