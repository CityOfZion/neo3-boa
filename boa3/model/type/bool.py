from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class Bool(IType):
    """
    A class used to represent Python bool type
    """
    def __init__(self):
        identifier = 'bool'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Boolean
