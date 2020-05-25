from typing import Any

from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class BoolType(IType):
    """
    A class used to represent Python bool type
    """

    def __init__(self):
        identifier = 'bool'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Boolean

    @classmethod
    def build(cls, value: Any):
        if cls.is_type_of(value):
            from boa3.model.type.type import Type
            return Type.bool

    @classmethod
    def is_type_of(cls, value: Any):
        return type(value) == bool
