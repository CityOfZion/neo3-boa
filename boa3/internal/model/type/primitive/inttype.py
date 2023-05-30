from typing import Any

from boa3.internal import constants
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.primitivetype import PrimitiveType
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.StackItem import StackItemType


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

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.internal.model.builtin.builtin import Builtin

        self._instance_methods[constants.INIT_METHOD_ID] = Builtin.IntInt

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.type.type import Type
            return Type.int

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) is int or isinstance(value, IntType)
