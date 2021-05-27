from typing import Any, Dict

from boa3.builtin.type import UInt160


class Contract:
    """
    Represents a contract that can be invoked.

    :var id: the serial number of the contract
    :vartype id: int
    :var update_counter: the number of times the contract was updated
    :vartype update_counter: int
    :var hash: the hash of the contract
    :vartype hash: UInt160
    :var nef: the nef of the contract
    :vartype nef: bytes
    :var manifest: the manifest of the contract
    :vartype manifest: Dict[str, Any]
    """
    def __init__(self):
        self.id: int = 0
        self.update_counter: int = 0
        self.hash: UInt160 = UInt160()
        self.nef: bytes = bytes()
        self.manifest: Dict[str, Any] = {}
