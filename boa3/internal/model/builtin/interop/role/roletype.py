from typing import Any

from boa3.internal.model.type.enum.intenumtype import IntEnumType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo3.contracts.native import Role


class RoleType(IntEnumType):
    """
    A class used to represent Neo's Role type.
    """

    def __init__(self):
        super().__init__(Role)
        self._identifier = 'Role'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _Role

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (Role, RoleType))


_Role = RoleType()
