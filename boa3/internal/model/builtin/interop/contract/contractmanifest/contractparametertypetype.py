from typing import Any

from boa3.internal.model.type.enum.intenumtype import IntEnumType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType as ContractParameter


class ContractParameterTypeType(IntEnumType):
    """
    A class used to represent Neo interop ContractParameterType type
    """

    def __init__(self):
        super().__init__(ContractParameter)
        self._identifier = 'ContractParameterType'

    @property
    def default_value(self) -> Any:
        return ContractParameter.ALL

    @classmethod
    def build(cls, value: Any = None) -> IType:
        if value is None or cls._is_type_of(value):
            return _ContractParameterType

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (ContractParameter, ContractParameterTypeType))


_ContractParameterType = ContractParameterTypeType()
