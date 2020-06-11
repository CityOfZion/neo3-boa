from typing import Any, List

from boa3.model.type.itype import IType
from boa3.model.type.sequence.sequencetype import SequenceType


class TupleType(SequenceType):
    """
    A class used to represent Python tuple type
    """

    def __init__(self, values_type: List[IType] = None):
        identifier = 'tuple'
        values_type = self.filter_types(values_type)
        super().__init__(identifier, values_type)

    @property
    def default_value(self) -> Any:
        return tuple()

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
        return type(value) is tuple or isinstance(value, TupleType)

    @property
    def can_reassign_values(self) -> bool:
        return False

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.value_type == other.value_type

    def __hash__(self):
        return hash(self.identifier)
