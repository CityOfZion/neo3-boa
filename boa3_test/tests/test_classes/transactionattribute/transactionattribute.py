from __future__ import annotations

import abc
from typing import Any, Dict

from boa3_test.tests.test_classes import transactionattribute


class TransactionAttribute(abc.ABC):

    def __init__(self, _type: transactionattribute.TransactionAttributeType):
        self._type: transactionattribute.TransactionAttributeType = _type

    def to_json(self) -> Dict[str, Any]:
        return {
            'type': self._type.name
        }

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> TransactionAttribute:
        tx_type = json['type']
        pass

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and self._type == other._type
