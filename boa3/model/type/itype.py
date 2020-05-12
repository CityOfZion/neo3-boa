from boa3.model.symbol import ISymbol
from boa3.neo.vm.type.AbiType import AbiType


class IType(ISymbol):
    """
    An interface used to represent types

    :ivar identifier: the name identifier of the type
    """
    def __init__(self, identifier: str):
        self.identifier: str = identifier

    @property
    def abi_type(self) -> AbiType:
        """
        Get the type representation for the abi

        :return: the representation for the abi. Any by default.
        """
        return AbiType.Any
