from typing import Any

from boa3.internal.model.type.enum.intenumtype import IntEnumType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo3.network.payloads.transactionattributetype import \
    TransactionAttributeType as TransactionAttribute


class TransactionAttributeTypeType(IntEnumType):
    """
    A class used to represent Neo TransactionAttributeType
    """

    def __init__(self):
        super().__init__(TransactionAttribute)
        self._identifier = 'TransactionAttributeType'

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.builtin.interop.interop import Interop
            return Interop.TransactionAttributeType

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (TransactionAttribute, TransactionAttributeTypeType))
