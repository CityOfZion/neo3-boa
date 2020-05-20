from typing import Any

from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class StrType(IType):
    """
    A class used to represent Python str type
    """
    def __init__(self):
        identifier = 'str'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.String

    @classmethod
    def build(cls, value: Any):
        if cls.is_type_of(value):
            from boa3.model.type.type import Type
            return Type.str

    @classmethod
    def is_type_of(cls, value: Any):
        return type(value) == str
