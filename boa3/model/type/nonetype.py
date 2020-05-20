from typing import Any

from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class NoneType(IType):
    """
    A class used to represent Python None value
    """
    def __init__(self):
        identifier = 'none'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Void

    @classmethod
    def build(cls, value: Any):
        if cls.is_type_of(value):
            from boa3.model.type.type import Type
            return Type.none

    @classmethod
    def is_type_of(cls, value: Any):
        return value is None
