from typing import Any

from boa3.internal.model.type.enum.intflagtype import IntFlagType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo3.contracts.findoptions import FindOptions


class FindOptionsType(IntFlagType):
    """
    A class used to represent Neo interop FindOptions type
    """

    def __init__(self):
        super().__init__(FindOptions)
        self._identifier = 'FindOptions'

    @property
    def default_value(self) -> Any:
        return FindOptions.NONE

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if cls._is_type_of(value) or value is None:
            from boa3.internal.model.builtin.interop.interop import Interop
            return Interop.FindOptionsType

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (FindOptions, FindOptionsType))
