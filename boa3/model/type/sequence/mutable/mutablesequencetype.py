from abc import ABC
from typing import List, Any

from boa3.model.type.itype import IType
from boa3.model.type.sequence.sequencetype import SequenceType


class MutableSequenceType(SequenceType, ABC):
    """
    An interface used to represent Python sequence type
    """

    def __init__(self, identifier: str, values_type: List[IType]):
        super().__init__(identifier, values_type)

    def is_type_of(self, value: Any) -> bool:
        if self._is_type_of(value):
            if isinstance(value, MutableSequenceType):
                return self.value_type.is_type_of(value.value_type)
            return True
        return False
