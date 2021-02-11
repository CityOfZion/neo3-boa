from typing import Any

from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.itype import IType
from boa3.model.type.primitive.primitivetype import PrimitiveType
from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.StackItem import StackItemType


class BytesType(SequenceType, PrimitiveType):
    """
    A class used to represent Python bytes type
    """

    def __init__(self):
        identifier = 'bytes'
        from boa3.model.type.primitive.inttype import IntType
        values_type = [IntType()]
        super().__init__(identifier, values_type)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def abi_type(self) -> AbiType:
        return AbiType.ByteArray

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.ByteString

    @property
    def default_value(self) -> Any:
        return bytes()

    def is_valid_key(self, key_type: IType) -> bool:
        return key_type == self.valid_key

    @property
    def valid_key(self) -> IType:
        from boa3.model.type.type import Type
        return Type.int

    @classmethod
    def build(cls, value: Any) -> IType:
        from boa3.model.type.type import Type
        return Type.bytes

    @classmethod
    def build_collection(cls, *value_type: IType):
        return cls.build(value_type)

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) is bytes or isinstance(value, BytesType)

    @property
    def can_reassign_values(self) -> bool:
        return False
