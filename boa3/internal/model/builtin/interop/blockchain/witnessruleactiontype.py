from typing import Any, Self

from boa3.internal.model.type.enum.intenumtype import IntEnumType
from boa3.internal.neo3.network.payloads.verification import WitnessRuleAction


class WitnessRuleActionType(IntEnumType):
    """
    A class used to represent Neo interop WitnessRuleAction type
    """

    def __init__(self):
        super().__init__(WitnessRuleAction)
        self._identifier = 'WitnessRuleAction'

    @property
    def default_value(self) -> Any:
        return WitnessRuleAction.DENY

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _WitnessRuleAction

    @classmethod
    def _is_type_of(cls, value: Any = None):
        return isinstance(value, (WitnessRuleAction, WitnessRuleActionType))

_WitnessRuleAction = WitnessRuleActionType()
