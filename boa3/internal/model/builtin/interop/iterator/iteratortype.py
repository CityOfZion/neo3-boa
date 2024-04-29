from typing import Any, Self

from boa3.internal.model.builtin.interop.interopinterfacetype import InteropInterfaceType
from boa3.internal.model.method import Method
from boa3.internal.model.type.collection.icollection import ICollectionType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class IteratorType(InteropInterfaceType, ICollectionType):
    """
    A class used to represent Neo Iterator class
    """

    def __init__(self, collection: ICollectionType = None):
        super().__init__('Iterator')

        if collection is None:
            from boa3.internal.model.type.type import Type
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

    def constructor_method(self) -> Method | None:
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
    def build(cls, value: Any = None) -> Self:
        if isinstance(value, ICollectionType):
            return IteratorType(value)
        else:
            return _Iterator

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, IteratorType)

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.internal.model.builtin.interop.iterator.iteratornextmethod import IteratorNextMethod
        from boa3.internal.model.builtin.interop.iterator.getiteratorvalue import IteratorValueProperty

        self._instance_methods['next'] = IteratorNextMethod()

        self._properties['value'] = IteratorValueProperty(self)

    def is_instance_opcodes(self) -> list[tuple[Opcode, bytes]]:
        from boa3.internal.model.type.classes.pythonclass import PythonClass
        return super(PythonClass, self).is_instance_opcodes()

    def generate_is_instance_type_check(self, code_generator):
        from boa3.internal.model.type.classes.pythonclass import PythonClass
        return super(PythonClass, self).generate_is_instance_type_check(code_generator)

    def __eq__(self, other) -> bool:
        if not isinstance(other, IteratorType):
            return False
        return self.valid_key == other.valid_key and self.value_type == other.value_type

    def __hash__(self) -> int:
        return self._origin_collection.__hash__()


_Iterator = IteratorType()
