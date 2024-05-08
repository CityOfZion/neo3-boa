from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, Self

from boa3.internal.model.type.annotation.uniontype import UnionType
from boa3.internal.model.type.classes.pythonclass import PythonClass
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.primitivetype import PrimitiveType


class ICollectionType(PythonClass, ABC):
    """
    An interface used to represent Python mapping type
    """

    def __init__(self, identifier: str, keys_type: set[IType] = None, values_type: set[IType] = None):
        if keys_type is None:
            keys_type = set()
        self.key_type: IType = self._get_collection_type(keys_type)

        if values_type is None:
            values_type = set()
        self.item_type: IType = self._get_collection_type(values_type)
        super().__init__(identifier)

    @property
    def identifier(self) -> str:
        return '{0}[{1}]'.format(self._identifier, self.item_type.identifier)

    def is_type_of(self, value: Any) -> bool:
        if self._is_type_of(value):
            if isinstance(value, ICollectionType):
                return self.item_type.is_type_of(value.item_type)
            return True
        return False

    @abstractmethod
    def is_valid_key(self, key_type: IType) -> bool:
        """
        Verifies if the given type is valid to retrieve values

        :param key_type: type to validate.
        :return: A boolean value that represents if the value is valid.
        """
        return False

    @property
    def can_reassign_values(self) -> bool:
        return False

    @property
    @abstractmethod
    def valid_key(self) -> IType:
        pass

    def _get_collection_type(self, values_type: set[IType]):
        if len(values_type) == 0:
            from boa3.internal.model.type.anytype import anyType
            val_type: IType = anyType
        elif len(values_type) == 1:
            val_type: IType = list(values_type)[0]
        else:
            val_type: IType = UnionType.build(values_type)

        return val_type

    @classmethod
    def get_types(cls, value: Any) -> set[IType]:
        from boa3.internal.model.type.type import Type
        if isinstance(value, IType):
            return {value}

        if not isinstance(value, Iterable):
            value = {value}

        types: set[IType] = {val if isinstance(val, IType) else Type.get_type(val) for val in value}
        return cls.filter_types(types)

    def get_item_type(self, index: tuple):
        return self.item_type

    @classmethod
    def filter_types(cls, values_type) -> set[IType]:
        if values_type is None:
            values_type = set()
        elif not isinstance(values_type, set):
            if isinstance(values_type, Iterable):
                values_type = set(values_type)
            else:
                values_type = {values_type}

        if len(values_type) > 1:
            from boa3.internal.model.type.type import Type
            if any(t is Type.any or t is Type.none for t in values_type):
                return {Type.any}

            if Type.ellipsis in values_type:
                values_type.remove(Type.ellipsis)
                if len(values_type) == 1:
                    return values_type

            actual_types = list(values_type)[:1]
            for value in list(values_type)[1:]:
                other = next((x for x in actual_types
                              if x.is_type_of(value) or value.is_type_of(x)), None)

                if other is not None and value.is_type_of(other):
                    actual_types.remove(other)
                    other = None

                if other is None:
                    actual_types.append(value)
            values_type = set(actual_types)

            if any(not isinstance(x, ICollectionType) for x in values_type):
                return values_type
            if all(isinstance(x, PrimitiveType) for x in values_type):
                return values_type
            # verifies if all the types are the same collection with different arguments
            if not all(isinstance(x, ICollectionType) for x in values_type):
                return {Type.get_generic_type(*values_type)}
            else:
                first_item: ICollectionType = list(values_type)[0]
                collection_type = type(first_item)  # first sequence type
                value_type = type(first_item.item_type)  # first sequence values type

            if all(isinstance(x, collection_type) for x in values_type):
                # if all the types are the same sequence type, build this sequence with any as parameters
                types = set(value.item_type for value in values_type)
                values_type = {collection_type.build(types)}
            else:
                generic_type: IType = Type.get_generic_type(*values_type)
                if (isinstance(generic_type, ICollectionType)
                        and all(isinstance(x.item_type, value_type) for x in values_type)):
                    # the collections doesn't have the same type but the value type is the same
                    # for example: tuple[int] and list[int]
                    values_type = {generic_type.build_collection(first_item.item_type)}
                else:
                    # otherwise, built a generic sequence with any as parameters
                    values_type = {generic_type}

        return values_type

    @classmethod
    def build_collection(cls, *value_type: IType | Iterable) -> Self:
        """
        Creates a collection type instance with the given value

        :param value_type: value to build the type
        :type value_type: IType or Iterable
        :return: The built collection type.
        :rtype: IType or None
        """
        from inspect import signature
        # if the number of params is different than the constructor args (except self arg)
        # returns an object with the default values
        if len(value_type) != len(signature(cls.__init__).parameters) - 1:
            return cls()

        params = []
        for arg in value_type:
            if isinstance(arg, Iterable):
                argument = set(arg)
            else:
                argument = {arg}
            params.append(argument)

        return cls(*params)
