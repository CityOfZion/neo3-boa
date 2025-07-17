from typing import Any, Self

from boa3.internal.model.type.enum.intenumtype import IntEnumType
from boa3.internal.neo3.vm import VMState


class VMStateType(IntEnumType):
    """
    A class used to represent Neo interop VMState type
    """

    def __init__(self):
        super().__init__(VMState)
        self._identifier = 'VMState'

    @property
    def default_value(self) -> Any:
        return VMState.NONE

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _VMState

    @classmethod
    def _is_type_of(cls, value: Any = None):
        return isinstance(value, (VMState, VMStateType))

_VMState = VMStateType()
