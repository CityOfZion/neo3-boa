from typing import Any

from boa3.internal.model.type.enum.intenumtype import IntEnumType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo3.network.payloads import OracleResponseCode


class OracleResponseCodeType(IntEnumType):
    """
    A class used to represent Neo's OracleResponseCode.
    """

    def __init__(self):
        super().__init__(OracleResponseCode)
        self._identifier = 'OracleResponseCode'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _OracleResponseCode

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (OracleResponseCode, OracleResponseCodeType))


_OracleResponseCode = OracleResponseCodeType()
