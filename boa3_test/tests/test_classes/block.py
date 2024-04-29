from typing import Any, Self

from boa3_test.test_drive.model.network.payloads.testblock import TestBlock
from boa3_test.tests.test_classes.transaction import Transaction


class Block(TestBlock):
    def __init__(self, index: int):
        self._transactions: list[Transaction] = []
        super().__init__()

        import time
        # time() returns timestamp in nanoseconds and Neo uses timestamp in milliseconds
        self._timestamp: int = int(time.time_ns() / 1_000_000)
        self._index: int = index

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
        json_block = super().to_json()

        if self._hash is not None:
            json_block['hash'] = str(self._hash)

        return json_block

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        block: Self = super().from_json(json)

        # 'index' and 'timestamp' fields are required
        block._index = int(json['index'])
        block._timestamp = int(json['timestamp'])

        return block
