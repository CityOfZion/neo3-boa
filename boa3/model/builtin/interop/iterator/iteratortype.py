from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classtype import ClassType
from boa3.model.type.collection.icollection import ICollectionType
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class IteratorType(ClassType, ICollectionType):
    """
    A class used to represent Neo Iterator class
    """

    def __init__(self, collection: ICollectionType = None):
        super().__init__('Iterator')

        if collection is None:
            from boa3.model.type.type import Type
            collection = Type.collection

        self._constructor: Method = None
        self._origin_collection: ICollectionType = collection

        self._methods = None
        self._properties = None

        self.key_type = self._origin_collection.valid_key
        self.item_type = self._origin_collection.item_type

    @property
    def identifier(self) -> str:
        return '{0}[{1}, {2}]'.format(self._identifier, self.valid_key.identifier, self.item_type.identifier)

    @property
    def variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def properties(self) -> Dict[str, Property]:
        if self._properties is None:
            from boa3.model.builtin.interop.iterator.getiteratorvalue import IteratorValueProperty
            self._properties = {
                'value': IteratorValueProperty(self)
            }

        return self._properties.copy()

    @property
    def class_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> Dict[str, Method]:
        if self._methods is None:
            from boa3.model.builtin.interop.iterator.iteratornextmethod import IteratorNextMethod

            self._methods = {
                'next': IteratorNextMethod()
            }
        return self._methods.copy()

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @property
    def value_type(self) -> IType:
        return self._origin_collection.item_type

    @property
    def valid_key(self) -> IType:
        return self._origin_collection.valid_key

    def is_valid_key(self, key_type: IType) -> bool:
        return self._origin_collection.is_valid_key(key_type)

    @classmethod
    def build(cls, value: Any = None) -> IteratorType:
        if isinstance(value, ICollectionType):
            return IteratorType(value)
        else:
            return _Iterator

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, IteratorType)

    def __eq__(self, other) -> bool:
        if not isinstance(other, IteratorType):
            return False
        return self.valid_key == other.valid_key and self.value_type == other.value_type

    def __hash__(self) -> int:
        return self._origin_collection.__hash__()


_Iterator = IteratorType()
