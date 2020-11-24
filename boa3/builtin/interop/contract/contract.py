from typing import Any, Dict


class Contract:
    def __init__(self):
        self.script: bytes = bytes()
        self.manifest: Dict[str, Any] = {}
