from typing import Any, Set

from boa3.model.type.collection.mapping.mutable.mutablemappingtype import MutableMappingType
from boa3.model.type.itype import IType


class DictType(MutableMappingType):
    """
    A class used to represent Python dict type
    """

    def __init__(self, keys_type: Set[IType] = None, values_type: Set[IType] = None):
        identifier = 'dict'
        keys_type = self.filter_types(keys_type)
        values_type = self.filter_types(values_type)
        super().__init__(identifier, keys_type, values_type)

    @property
    def default_value(self) -> Any:
        return dict()

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) in [dict, DictType]

    def __hash__(self):
        return hash(self.identifier)
