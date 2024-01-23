from typing import Any

from boa3.internal.model.type.collection.mapping.mappingtype import MappingType
from boa3.internal.model.type.itype import IType


class GenericMappingType(MappingType):
    """
    An class used to represent a generic Python sequence type
    """

    def __init__(self, keys_type: set[IType] = None, values_type: set[IType] = None):
        identifier: str = 'mapping'
        keys_type = self.filter_types(keys_type)
        values_type = self.filter_types(values_type)
        super().__init__(identifier, keys_type, values_type)

    def is_valid_key(self, key_type: IType) -> bool:
        return key_type == self.valid_key

    @property
    def is_generic(self) -> bool:
        return True

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, MappingType)

    def __hash__(self):
        return hash(self.identifier)
