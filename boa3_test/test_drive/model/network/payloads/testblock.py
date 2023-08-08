from __future__ import annotations

from typing import Optional, List, Dict, Any

from boa3.internal.neo import from_hex_str
from boa3.internal.neo3.core.types import UInt256
from boa3_test.test_drive.model.network.payloads.testtransaction import TestTransaction


class TestBlock:
    def __init__(self):
        self._index: int = 0
        self._timestamp: int = 0
        self._hash: Optional[UInt256] = None
        self._transactions: List[TestTransaction] = []

    @property
    def index(self) -> int:
        return self._index

    @property
    def timestamp(self) -> int:
        return self._timestamp

    def to_json(self) -> Dict[str, Any]:
        json_block = {
            'index': self._index,
            'timestamp': self._timestamp,
            'transactions': [tx.to_json() for tx in self._transactions]
        }

        if self._hash is not None:
            json_block['hash'] = str(self._hash)

        return json_block

    @classmethod
    def from_json(cls, json: Dict[str, Any], *args, **kwargs) -> TestBlock:
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
        block._transactions = [TestTransaction.from_json(js) for js in tx_json]

        if 'hash' in json and isinstance(json['hash'], str):
            block._hash = UInt256(from_hex_str(json['hash']))
        else:
            block._hash = None

        return block

    def __repr__(self) -> str:
        return str(self._hash) if self._hash is not None else str(self._index)
