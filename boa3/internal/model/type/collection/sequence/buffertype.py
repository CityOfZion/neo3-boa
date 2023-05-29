from typing import Any

from boa3.internal.model.type.primitive.strtype import StrType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class BufferType(StrType):
    """
    A class used to represent Neo internal Buffer type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'buffer'

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.Buffer

    @classmethod
    def _is_type_of(cls, value: Any) -> bool:
        if super()._is_type_of(value):
            return True
        return isinstance(value, BufferType)


Buffer = BufferType()
