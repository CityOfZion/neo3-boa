from typing import Any

from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.itype import IType
from boa3.model.type.primitive.primitivetype import PrimitiveType
from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.StackItem import StackItemType


class StrType(SequenceType, PrimitiveType):
    """
    A class used to represent Python str type
    """

    def __init__(self):
        identifier = 'str'
        super().__init__(identifier, [self])

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def default_value(self) -> Any:
        return str()

    @property
    def abi_type(self) -> AbiType:
        return AbiType.String

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.ByteString

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.model.type.type import Type
            return Type.str

    @classmethod
    def build_collection(cls, value_type: IType):
        from boa3.model.type.type import Type
        return Type.str

    @classmethod
    def _is_type_of(cls, value: Any) -> bool:
        return type(value) in [str, StrType]

    def is_type_of(self, value: Any) -> bool:
        return self._is_type_of(value)

    def is_valid_key(self, key_type: IType) -> bool:
        return key_type == self.valid_key

    @property
    def valid_key(self) -> IType:
        from boa3.model.type.type import Type
        return Type.int

    @property
    def can_reassign_values(self) -> bool:
        return False
