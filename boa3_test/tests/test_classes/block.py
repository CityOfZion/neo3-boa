from typing import Any, Dict, List

from boa3_test.tests.test_classes.transaction import Transaction


class Block:
    def __init__(self, index: int):
        import time
        self._index: int = index
        # time() returns timestamp in seconds and Neo uses timestamp in milliseconds
        self._timestamp: int = int(time.time() * 1000)
        self._transactions: List[Transaction] = []

    @property
    def index(self) -> int:
        return self._index

    @property
    def timestamp(self) -> int:
        return self._timestamp

    def add_transaction(self, tx: Transaction):
        self._transactions.append(tx)

    def to_json(self) -> Dict[str, Any]:
        return {
            'index': self._index,
            'timestamp': self._timestamp,
            'transactions': [tx.to_json() for tx in self._transactions]
        }
