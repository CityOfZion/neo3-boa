from typing import Any

from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType
from boa3.internal.neo.vm.type.AbiType import AbiType


class BytesType(IByteStringType):
    """
    A class used to represent Python bytes type
    """

    def __init__(self):
        identifier = 'bytes'
        from boa3.internal.model.type.primitive.inttype import IntType
        values_type = [IntType()]
        super().__init__(identifier, values_type)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.ByteArray

    @property
    def default_value(self) -> Any:
        return bytes()

    @classmethod
    def build(cls, value: Any) -> IType:
        from boa3.internal.model.type.type import Type
        return Type.bytes

    @classmethod
    def build_collection(cls, *value_type: IType):
        return cls.build(value_type)

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) is bytes or isinstance(value, BytesType)
