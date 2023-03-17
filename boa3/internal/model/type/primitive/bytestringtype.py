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
                or Type.bytes.is_type_of(value)
                or isinstance(value, ByteStringType))

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.internal.model.builtin.builtin import Builtin

        instance_methods = [Builtin.ConvertToBytes,
                            Builtin.ConvertToBool,
                            Builtin.ConvertToInt,
                            Builtin.ConvertToStr,
                            ]

        for instance_method in instance_methods:
            self._instance_methods[instance_method.raw_identifier] = instance_method.build(self)

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _ByteString


_ByteString = ByteStringType()
