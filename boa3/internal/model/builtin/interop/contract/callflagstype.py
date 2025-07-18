from typing import Any

from boa3.internal.model.type.enum.intflagtype import IntFlagType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo3.contracts import CallFlags


class CallFlagsType(IntFlagType):
    """
    A class used to represent Neo interop CallFlags type
    """

    def __init__(self):
        super().__init__(CallFlags)
        self._identifier = 'CallFlags'

    @property
    def default_value(self) -> Any:
        return CallFlags.ALL

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _CallFlags

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (CallFlags, CallFlagsType))

_CallFlags = CallFlagsType()
