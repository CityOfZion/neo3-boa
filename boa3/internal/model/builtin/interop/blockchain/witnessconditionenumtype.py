from typing import Any, Self

from boa3.internal.model.type.enum.intenumtype import IntEnumType
from boa3.internal.neo3.network.payloads.verification import WitnessConditionType as WitnessCondition


class WitnessConditionTypeType(IntEnumType):
    """
    A class used to represent Neo interop WitnessConditionType type
    """

    def __init__(self):
        super().__init__(WitnessCondition)
        self._identifier = 'WitnessConditionType'

    @property
    def default_value(self) -> Any:
        return WitnessCondition.BOOLEAN

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _WitnessConditionType

    @classmethod
    def _is_type_of(cls, value: Any = None):
        return isinstance(value, (WitnessCondition, WitnessConditionTypeType))


_WitnessConditionType = WitnessConditionTypeType()
