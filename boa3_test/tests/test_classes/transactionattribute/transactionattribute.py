import abc
from typing import Any, Self

from boa3_test.tests.test_classes.transactionattribute import transactionattributetype


class TransactionAttribute(abc.ABC):

    def __init__(self, _type: transactionattributetype.TransactionAttributeType):
        self._type: transactionattributetype.TransactionAttributeType = _type

    def to_json(self) -> dict[str, Any]:
        return {
            'type': self._type.name
        }

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        tx_type = json['type']
        pass

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and self._type == other._type
