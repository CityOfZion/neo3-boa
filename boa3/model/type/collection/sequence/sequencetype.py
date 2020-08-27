from abc import ABC
from typing import Any, Set

from boa3.model.type.collection.icollection import ICollectionType
from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.StackItemType import StackItemType


class SequenceType(ICollectionType, ABC):
    """
    An interface used to represent Python sequence type
    """

    def __init__(self, identifier: str, values_type: Set[IType]):
        super().__init__(identifier, values_type=values_type)
        self.value_type: IType = self.item_type

    @property
    def default_value(self) -> Any:
        return []

    def is_type_of(self, value: Any) -> bool:
        if self._is_type_of(value):
            if isinstance(value, SequenceType):
                return self.value_type.is_type_of(value.value_type)
            return True
        return False

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Array

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.Array
