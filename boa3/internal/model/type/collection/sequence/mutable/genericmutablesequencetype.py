from typing import Any, Set

from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.type.itype import IType


class GenericMutableSequenceType(MutableSequenceType):
    """
    An class used to represent a generic Python mutable sequence type
    """

    def __init__(self, values_type: Set[IType] = None):
        identifier: str = 'MutableSequence'
        values_type = self.filter_types(values_type)
        super().__init__(identifier, values_type)

    def is_valid_key(self, key_type: IType) -> bool:
        return key_type == self.valid_key

    @property
    def valid_key(self) -> IType:
        from boa3.internal.model.type.type import Type
        return Type.int

    @property
    def is_generic(self) -> bool:
        return True

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            values_types: Set[IType] = cls.get_types(value)
            return cls(values_types)

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, MutableSequenceType)

    def __hash__(self):
        return hash(self.identifier)
