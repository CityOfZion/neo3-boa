from abc import ABC
from typing import Any

from boa3.internal.model.type.collection.icollection import ICollectionType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class SequenceType(ICollectionType, ABC):
    """
    An interface used to represent Python sequence type
    """

    def __init__(self, identifier: str, values_type: set[IType]):
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

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.internal.model.builtin.builtin import Builtin

        instance_methods = [Builtin.CountSequenceGeneric,
                            Builtin.SequenceIndex,
                            ]

        for instance_method in instance_methods:
            self._instance_methods[instance_method.raw_identifier] = instance_method.build([self, self.value_type])
