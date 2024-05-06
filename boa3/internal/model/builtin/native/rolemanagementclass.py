from typing import Any, Self

from boa3.internal.model.builtin.interop.nativecontract import RoleManagement
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class RoleManagementClass(INativeContractClass):
    """
    A class used to represent RoleManagement native contract
    """

    def __init__(self):
        super().__init__('RoleManagement', RoleManagement)

    @property
    def class_methods(self) -> dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            self._class_methods = {
                'get_designated_by_role': Interop.GetDesignatedByRole
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _RoleManagement

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, RoleManagementClass)


_RoleManagement = RoleManagementClass()
