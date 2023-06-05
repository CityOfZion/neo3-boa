__all__ = [
    'Contract',
]

from boa3.builtin.interop.contract.contractmanifest import ContractManifest
from boa3.builtin.type import UInt160


class Contract:
    """
    Represents a contract that can be invoked.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/glossary#smart-contract>`__ to learn about
    Smart Contracts.

    :ivar id: the serial number of the contract
    :vartype id: int
    :ivar update_counter: the number of times the contract was updated
    :vartype update_counter: int
    :ivar hash: the hash of the contract
    :vartype hash: UInt160
    :ivar nef: the serialized Neo Executable Format (NEF) object holding of the smart contract code and compiler
        information
    :vartype nef: bytes
    :ivar manifest: the manifest of the contract
    :vartype manifest: ContractManifest
    """

    def __init__(self):
        self.id: int = 0
        self.update_counter: int = 0
        self.hash: UInt160 = UInt160()
        self.nef: bytes = bytes()
        self.manifest: ContractManifest = ContractManifest()
