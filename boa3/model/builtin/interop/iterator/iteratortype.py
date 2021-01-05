from typing import Any, Dict

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

    @property
    def identifier(self) -> str:
        return '{0}[{1}, {2}]'.format(self._identifier, self.key_type.identifier, self.item_type.identifier)

    @property
    def variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

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

    def constructor_method(self) -> Method:
        # was having a problem with recursive import
        if self._constructor is None:
            from boa3.model.builtin.interop.iterator.iteratorinitmethod import IteratorMethod
            self._constructor: Method = IteratorMethod(self)
        return self._constructor

    @property
    def valid_key(self) -> IType:
        return self._origin_collection.valid_key

    def is_valid_key(self, key_type: IType) -> bool:
        return self._origin_collection.is_valid_key(key_type)

    @classmethod
    def build(cls, value: Any = None):
        if value is None or cls._is_type_of(value):
            return _Iterator

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, IteratorType)


_Iterator = IteratorType()
