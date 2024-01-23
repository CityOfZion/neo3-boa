from typing import Any

from boa3.internal.model.type.collection.icollection import ICollectionType
from boa3.internal.model.type.itype import IType


class GenericCollectionType(ICollectionType):
    """
    An class used to represent a generic Python collection type
    """

    def __init__(self, keys_type: set[IType] = None, values_type: set[IType] = None):
        identifier: str = 'collection'
        keys_type = self.filter_types(keys_type)
        values_type = self.filter_types(values_type)
        super().__init__(identifier, keys_type, values_type)

    def is_valid_key(self, key_type: IType) -> bool:
        return key_type == self.valid_key

    @property
    def valid_key(self) -> IType:
        return self.key_type

    @property
    def is_generic(self) -> bool:
        return True

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ICollectionType)

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            if isinstance(value, dict):
                keys = list(value.keys())
                values = list(value.values())
            else:
                keys = value.key_type
                values = value.value_type

            keys_types: set[IType] = cls.get_types(keys)
            values_types: set[IType] = cls.get_types(values)
            return cls(keys_types, values_types)

    def __hash__(self):
        return hash(self.identifier)
