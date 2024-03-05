from typing import Any

from boa3.internal import constants
from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.type.itype import IType


class ListType(MutableSequenceType):
    """
    A class used to represent Python list type
    """

    def __init__(self, values_type: set[IType] = None):
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

        from boa3.internal.model.builtin.builtin import Builtin

        instance_methods = [Builtin.Copy,
                            Builtin.ListSort
                            ]

        for instance_method in instance_methods:
            self._instance_methods[instance_method.raw_identifier] = instance_method.build(self)

        self._instance_methods[constants.INIT_METHOD_ID] = Builtin.ListGeneric

    @property
    def valid_key(self) -> IType:
        from boa3.internal.model.type.type import Type
        return Type.int

    @classmethod
    def build(cls, value: Any) -> IType:
        values_types: set[IType] = cls.get_types(value)
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
