from typing import Any

from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.bytestype import BytesType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class ByteArrayType(BytesType, MutableSequenceType):
    """
    A class used to represent Python list type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'bytearray'

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.Buffer

    @property
    def default_value(self) -> Any:
        return bytearray()

    @classmethod
    def build(cls, value: Any) -> IType:
        from boa3.internal.model.type.type import Type
        return Type.bytearray

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) in [bytearray, ByteArrayType]

    @property
    def can_reassign_values(self) -> bool:
        return True
