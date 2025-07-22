from typing import Any

from boa3.internal.model.type.enum.intflagtype import IntFlagType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo3.contracts import TriggerType as Trigger


class TriggerTypeType(IntFlagType):
    """
    A class used to represent Neo interop TriggerType type
    """

    def __init__(self):
        super().__init__(Trigger)
        self._identifier = 'TriggerType'

    @property
    def default_value(self) -> Any:
        return Trigger.ALL

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.builtin.interop.interop import Interop
            return Interop.TriggerType

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (Trigger, TriggerTypeType))
