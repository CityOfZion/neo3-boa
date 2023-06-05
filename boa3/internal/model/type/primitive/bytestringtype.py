from typing import Any

from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType


class ByteStringType(IByteStringType):
    """
    A class used to represent ByteString type interface
    """

    def __init__(self):
        identifier = 'ByteString'
        values_type = [self]
        super().__init__(identifier, values_type)

    @classmethod
    def _is_type_of(cls, value: Any) -> bool:
        from boa3.internal.model.type.type import Type
        return (Type.str.is_type_of(value)
                or Type.bytes.is_type_of(value))

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _ByteString


_ByteString = ByteStringType()
