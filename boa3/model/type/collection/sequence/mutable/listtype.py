from typing import Any, Set

from boa3 import constants
from boa3.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.model.type.itype import IType


class ListType(MutableSequenceType):
    """
    A class used to represent Python list type
    """

    def __init__(self, values_type: Set[IType] = None):
        identifier = 'list'
        values_type = self.filter_types(values_type)
        super().__init__(identifier, values_type)

    @property
    def default_value(self) -> Any:
        return list()

    def is_valid_key(self, key_type: IType) -> bool:
        return key_type == self.valid_key

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.model.builtin.builtin import Builtin

        self._instance_methods[constants.INIT_METHOD_ID] = Builtin.ListGeneric

    @property
    def valid_key(self) -> IType:
        from boa3.model.type.type import Type
        return Type.int

    @classmethod
    def build(cls, value: Any) -> IType:
        values_types: Set[IType] = cls.get_types(value)
        return cls(values_types)

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) in [list, ListType]

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.value_type == other.value_type

    def __hash__(self):
        return hash(self.identifier)
