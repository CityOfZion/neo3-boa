from typing import Any, Dict

from boa3.builtin.type import UInt160


class Contract:
    def __init__(self):
        self.id: int = 0
        self.update_counter: int = 0
        self.hash: UInt160 = UInt160()
        self.nef: bytes = bytes()
        self.manifest: Dict[str, Any] = {}
