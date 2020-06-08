from typing import List, Any

from boa3.model.type.itype import IType
from boa3.model.type.sequence.sequencetype import SequenceType


class GenericSequenceType(SequenceType):
    """
    An class used to represent a generic Python sequence type
    """

    def __init__(self, values_type: List[IType] = None):
        identifier: str = 'sequence'
        values_type = self.filter_types(values_type)
        super().__init__(identifier, values_type)

    def is_valid_key(self, value_type: IType) -> bool:
        return value_type == self.valid_key

    @property
    def valid_key(self) -> IType:
        from boa3.model.type.type import Type
        return Type.int

    @classmethod
    def build(cls, value: Any):
        if cls._is_type_of(value):
            values_types: List[IType] = cls.get_types(value)
            return cls(values_types)

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, SequenceType)

    def __hash__(self):
        return hash(self.identifier)
