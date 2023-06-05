from abc import ABC
from typing import Any, Set

from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.itype import IType


class MutableSequenceType(SequenceType, ABC):
    """
    An interface used to represent Python mutable sequence type
    """

    def __init__(self, identifier: str, values_type: Set[IType]):
        super().__init__(identifier, values_type)

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.internal.model.builtin.builtin import Builtin

        instance_methods = [Builtin.SequenceAppend,
                            Builtin.SequenceClear,
                            Builtin.SequenceInsert,
                            Builtin.SequenceExtend,
                            Builtin.SequencePop,
                            Builtin.SequenceReverse,
                            Builtin.SequenceRemove,
                            ]

        for instance_method in instance_methods:
            self._instance_methods[instance_method.raw_identifier] = instance_method.build(self)

    def is_type_of(self, value: Any) -> bool:
        if self._is_type_of(value):
            if isinstance(value, MutableSequenceType):
                return self.value_type.is_type_of(value.value_type)
            return True
        return False

    @property
    def can_reassign_values(self) -> bool:
        return True
