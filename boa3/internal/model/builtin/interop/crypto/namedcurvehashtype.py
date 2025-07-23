from typing import Any

from boa3.internal.model.type.enum.intenumtype import IntEnumType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo3.contracts.namedcurvehash import NamedCurveHash


class NamedCurveHashType(IntEnumType):
    """
    A class used to represent Neo NamedCurveHash type
    """

    def __init__(self):
        super().__init__(NamedCurveHash)
        self._identifier = 'NamedCurveHash'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _NamedCurve

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (NamedCurveHash, NamedCurveHashType))


_NamedCurve = NamedCurveHashType()
