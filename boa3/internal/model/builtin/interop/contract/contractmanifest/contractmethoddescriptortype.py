from typing import Any, Self

from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classstructtype import ClassStructType
from boa3.internal.model.variable import Variable


class ContractMethodDescriptorType(ClassStructType):
    """
    A class used to represent Neo ContractMethodDescriptor class
    """

    def __init__(self):
        super().__init__('ContractMethodDescriptor')
        from boa3.internal.model.builtin.interop.contract.contractmanifest.contractparameterdefinitiontype import \
            ContractParameterDefinitionType
        from boa3.internal.model.builtin.interop.contract.contractmanifest.contractparametertypetype import \
            ContractParameterTypeType
        from boa3.internal.model.type.type import Type

        self._variables: dict[str, Variable] = {
            'name': Variable(Type.str),
            'parameters': Variable(Type.list.build_collection(ContractParameterDefinitionType.build())),
            'return_type': Variable(ContractParameterTypeType.build()),
            'offset': Variable(Type.int),
            'safe': Variable(Type.bool)
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
            return _ContractMethodDescriptor

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractMethodDescriptorType)


_ContractMethodDescriptor = ContractMethodDescriptorType()
