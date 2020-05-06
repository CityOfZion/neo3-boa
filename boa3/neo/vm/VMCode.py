from typing import Optional

from boa3.neo.vm.Opcode import Opcode


class VMCode:
    def __init__(self, opcode: Opcode, address: int, data: bytes = None):
        self.opcode: Opcode = opcode
        self.address: int = address
        self.data: Optional[bytes] = data
