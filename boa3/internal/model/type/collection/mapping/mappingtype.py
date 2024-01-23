from abc import ABC
from collections.abc import Iterable, Sized
from typing import Any

from boa3.internal.model.type.collection.icollection import ICollectionType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class MappingType(ICollectionType, ABC):
    """
    An interface used to represent Python mapping type
    """

    def __init__(self, identifier: str, keys_type: set[IType], values_type: set[IType]):
        super().__init__(identifier, keys_type=keys_type, values_type=values_type)

    @property
    def identifier(self) -> str:
        return '{0}[{1}, {2}]'.format(self._identifier, self.key_type.identifier, self.value_type.identifier)

    @property
    def value_type(self) -> IType:
        return self.item_type

    @property
    def default_value(self) -> Any:
        return {}

    def is_type_of(self, value: Any) -> bool:
        if self._is_type_of(value):
            if isinstance(value, MappingType):
                return (self.key_type.is_type_of(value.key_type)
                        and self.value_type.is_type_of(value.value_type))
            return True
        return False

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Map

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.Map

    def is_valid_key(self, key_type: IType) -> bool:
        return self.valid_key.is_type_of(key_type)

    @property
    def valid_key(self) -> IType:
        return self.key_type

    @classmethod
    def filter_types(cls, values_type) -> set[IType]:
        if values_type is None:
            values_type = set()
        elif not isinstance(values_type, set):
            if isinstance(values_type, Iterable):
                values_type = set(values_type)
            else:
                values_type = {values_type}

        if len(values_type) > 1 and all(isinstance(x, MappingType) for x in values_type):
            first_item: MappingType = list(values_type)[0]
            mapping_type = type(first_item)  # first mapping type

            k_types = set(value.key_type for value in values_type)
            v_types = set(value.value_type for value in values_type)

            if all(isinstance(x, mapping_type) for x in values_type):
                values_type = {mapping_type(keys_type=k_types, values_type=v_types)}
            else:
                from boa3.internal.model.type.type import Type
                generic_type: IType = Type.get_generic_type(*values_type)
                if isinstance(generic_type, MappingType):
                    values_type = {generic_type.build_collection(k_types, v_types)}

            return values_type

        # if any value is not a map, call the collection filter
        return super().filter_types(values_type)

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            # value is an instance of mapping
            if isinstance(value, dict):
                keys = list(value.keys())
                values = list(value.values())
            else:
                keys = value.key_type
                values = value.value_type

            keys_types: set[IType] = cls.get_types(keys)
            values_types: set[IType] = cls.get_types(values)
            return cls(keys_types, values_types)

        elif isinstance(value, Sized) and len(value) == 2:
            # value is a tuple with two lists of types for contructing the map
            keys_type, values_type = value

            if not isinstance(keys_type, Iterable):
                keys_type = {keys_type}
            else:
                keys_type = set(keys_type)

            if not isinstance(values_type, Iterable):
                values_types = {values_type}
            else:
                values_types = set(values_type)

            if all(isinstance(k, IType) for k in keys_type) and all(isinstance(v, IType) for v in values_types):
                return cls(keys_type, values_type)

        return super(MappingType, cls).build(value)
