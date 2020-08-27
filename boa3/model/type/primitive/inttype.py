from typing import Any

from boa3.model.type.primitive.primitivetype import PrimitiveType
from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.StackItemType import StackItemType


class IntType(PrimitiveType):
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

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.Integer

    @classmethod
    def build(cls, value: Any):
        if cls._is_type_of(value):
            from boa3.model.type.type import Type
            return Type.int

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) is int or isinstance(value, IntType)
