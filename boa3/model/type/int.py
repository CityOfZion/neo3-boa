from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class Int(IType):
    """
    A class used to represent Python int type
    """
    def __init__(self):
        identifier = 'int'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Integer
