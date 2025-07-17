from typing import Any, Self

from boa3.internal.model.type.enum.intenumtype import IntEnumType
from boa3.internal.neo3.network.payloads.verification import WitnessScope


class WitnessScopeType(IntEnumType):
    """
    A class used to represent Neo interop WitnessScope type
    """

    def __init__(self):
        super().__init__(WitnessScope)
        self._identifier = 'WitnessScope'

    @property
    def default_value(self) -> Any:
        return WitnessScope.NONE

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _WitnessScope

    @classmethod
    def _is_type_of(cls, value: Any = None):
        return isinstance(value, (WitnessScope, WitnessScopeType))


_WitnessScope = WitnessScopeType()
