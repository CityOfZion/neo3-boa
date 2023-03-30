from __future__ import annotations

from typing import Any, Dict

from boa3.internal.model.builtin.interop.nativecontract import ContractManagement
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class ContractManagementClass(INativeContractClass):
    """
    A class used to represent ContractManagement native contract
    """

    def __init__(self):
        super().__init__('ContractManagement', ContractManagement)

    @property
    def class_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            from boa3.internal.model.builtin.native.contract_management import HasMethod

            self._class_methods = {
                'get_minimum_deployment_fee': Interop.GetMinimumDeploymentFee,
                'get_contract': Interop.GetContract,
                'has_method': HasMethod(),
                'deploy': Interop.CreateContract,
                'update': Interop.UpdateContract,
                'destroy': Interop.DestroyContract
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> ContractManagementClass:
        if value is None or cls._is_type_of(value):
            return _ContractManagement

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractManagementClass)


_ContractManagement = ContractManagementClass()
