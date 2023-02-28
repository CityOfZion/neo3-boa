from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classstructtype import ClassStructType
from boa3.internal.model.variable import Variable


class ContractParameterDefinitionType(ClassStructType):
    """
    A class used to represent Neo ContractParameterDefinition class
    """

    def __init__(self):
        super().__init__('ContractParameterDefinition')
        from boa3.internal.model.builtin.interop.contract.contractmanifest.contractparametertype import ContractParameterType
        from boa3.internal.model.type.type import Type

        self._variables: Dict[str, Variable] = {
            'name': Variable(Type.str),
            'type': Variable(ContractParameterType.build())
        }
        self._constructor: Method = None

    @property
    def class_variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def instance_variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> ContractParameterDefinitionType:
        if value is None or cls._is_type_of(value):
            return _ContractParameterDefinition

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractParameterDefinitionType)


_ContractParameterDefinition = ContractParameterDefinitionType()
