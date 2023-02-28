from typing import Any

from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
from boa3.internal.model.type.itype import IType


class TransactionIdType(UInt256Type):
    """
    A class used to indicate that a parameter or return on the manifest is a TransactionId.
    It's a subclass of UInt256Type.
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'TransactionId'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _TransactionId


_TransactionId = TransactionIdType()
