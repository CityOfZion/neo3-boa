from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class NoneType(IType):
    """
    A class used to represent Python None value
    """
    def __init__(self):
        identifier = 'none'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Void
