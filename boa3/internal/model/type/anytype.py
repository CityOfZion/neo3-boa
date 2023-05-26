from typing import Any

from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.type.AbiType import AbiType


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
    def build(cls, value: Any) -> IType:
        from boa3.internal.model.type.type import Type
        return Type.any

    @classmethod
    def _is_type_of(cls, value: Any):
        return True

    def generate_is_instance_type_check(self, code_generator):
        code_generator.convert_literal(True)  # any is type of everything, so inserts True


anyType: IType = __AnyType()
