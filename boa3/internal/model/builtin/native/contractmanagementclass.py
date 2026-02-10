from typing import Any, Self

from boa3.internal.model.builtin.interop.nativecontract import ContractManagement
from boa3.internal.model.builtin.native import contract_management as cm
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class ContractManagementClass(INativeContractClass):
    """
    A class used to represent ContractManagement native contract
    """

    def __init__(self):
        super().__init__('ContractManagement', ContractManagement)

    @property
    def class_methods(self) -> dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            self._class_methods = {
                'get_minimum_deployment_fee': cm.GetMinimumDeploymentFeeMethod(),
                'get_contract': cm.GetContractMethod(Interop.ContractType),
                'get_contract_by_id': cm.GetContractByIdMethod(Interop.ContractType),
                'has_method': cm.HasMethod(),
                'deploy': cm.CreateMethod(Interop.ContractType),
                'update': cm.UpdateMethod(),
                'destroy': cm.DestroyMethod()
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _ContractManagement

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractManagementClass)


_ContractManagement = ContractManagementClass()
