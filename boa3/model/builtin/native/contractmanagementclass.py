from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classarraytype import ClassArrayType
from boa3.model.variable import Variable


class ContractManagementClass(ClassArrayType):
    """
    A class used to represent ContractManagement native contract
    """

    def __init__(self):
        super().__init__('ContractManagement')

        self._variables: Dict[str, Variable] = {}
        self._class_methods: Dict[str, Method] = {}
        self._constructor: Method = None

    @property
    def instance_variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        from boa3.model.builtin.interop.blockchain import GetContractMethod
        from boa3.model.builtin.interop.contract import (CreateMethod, DestroyMethod, GetMinimumDeploymentFeeMethod,
                                                         UpdateMethod)
        from boa3.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            self._class_methods = {
                'get_minimum_deployment_fee': GetMinimumDeploymentFeeMethod(),
                'get_contract': GetContractMethod(Interop.ContractType),
                'deploy': CreateMethod(Interop.ContractType),
                'update': UpdateMethod(),
                'destroy': DestroyMethod()
            }
        return self._class_methods

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> ContractManagementClass:
        if value is None or cls._is_type_of(value):
            return _ContractManagement

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractManagementClass)


_ContractManagement = ContractManagementClass()
