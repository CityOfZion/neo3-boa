from typing import Any

from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.itype import IType


class RangeType(SequenceType):
    """
    A class used to represent Python range type
    """

    def __init__(self, values_type: IType):
        identifier = 'range'
        values_type = self.filter_types(values_type)
        super().__init__(identifier, values_type)

    @property
    def default_value(self) -> Any:
        return range(0)

    @property
    def identifier(self) -> str:
        return self._identifier

    def is_valid_key(self, key_type: IType) -> bool:
        return key_type == self.valid_key

    @property
    def valid_key(self) -> IType:
        from boa3.internal.model.type.type import Type
        return Type.int

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.type.type import Type
            return cls(Type.int)

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) is range or isinstance(value, RangeType)

    @property
    def can_reassign_values(self) -> bool:
        return False

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.value_type == other.value_type

    def __hash__(self):
        return hash(self.identifier)
