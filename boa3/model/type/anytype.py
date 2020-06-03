from typing import Any

from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class __AnyType(IType):
    """
    A class used to represent Python bool type
    """

    def __init__(self):
        identifier = 'any'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Any

    @classmethod
    def build(cls, value: Any):
        from boa3.model.type.type import Type
        return Type.any

    @classmethod
    def _is_type_of(cls, value: Any):
        return True


anyType: IType = __AnyType()
