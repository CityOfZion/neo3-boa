from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class Str(IType):
    """
    A class used to represent Python str type
    """
    def __init__(self):
        identifier = 'str'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.String
