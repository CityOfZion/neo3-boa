from typing import Any

from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class IntType(IType):
    """
    A class used to represent Python int type
    """

    def __init__(self):
        identifier = 'int'
        super().__init__(identifier)

    @property
    def default_value(self) -> Any:
        return int()

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Integer

    @classmethod
    def build(cls, value: Any):
        if cls._is_type_of(value):
            from boa3.model.type.type import Type
            return Type.int

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) in [int, IntType]
