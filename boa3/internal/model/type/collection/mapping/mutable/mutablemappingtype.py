from abc import ABC
from typing import Any

from boa3.internal.model.type.collection.mapping.mappingtype import MappingType
from boa3.internal.model.type.itype import IType


class MutableMappingType(MappingType, ABC):
    """
    An interface used to represent Python mutable mapping type
    """

    def __init__(self, identifier: str, keys_type: set[IType], values_type: set[IType]):
        super().__init__(identifier, keys_type, values_type)

    def is_type_of(self, value: Any) -> bool:
        if self._is_type_of(value):
            if isinstance(value, MutableMappingType):
                return self.value_type.is_type_of(value.value_type)
            return True
        return False

    @property
    def can_reassign_values(self) -> bool:
        return True
