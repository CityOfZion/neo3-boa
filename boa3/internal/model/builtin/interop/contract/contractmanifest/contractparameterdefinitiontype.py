from typing import Any, Self

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

        self._variables: dict[str, Variable] = {
            'name': Variable(Type.str),
            'type': Variable(ContractParameterType.build())
        }
        self._constructor: Method = None

    @property
    def class_variables(self) -> dict[str, Variable]:
        return {}

    @property
    def instance_variables(self) -> dict[str, Variable]:
        return self._variables.copy()

    @property
    def properties(self) -> dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> dict[str, Method]:
        return {}

    def constructor_method(self) -> Method | None:
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _ContractParameterDefinition

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractParameterDefinitionType)


_ContractParameterDefinition = ContractParameterDefinitionType()
