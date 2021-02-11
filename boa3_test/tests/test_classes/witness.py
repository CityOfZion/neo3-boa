from __future__ import annotations

import base64
from typing import Any, Dict


class Witness:
    def __init__(self, invocation_script: bytes, verification_script: bytes):
        self._invocation_script = invocation_script
        self._verification_script = verification_script

    @property
    def invocation_script(self) -> bytes:
        return self._invocation_script

    @property
    def verification_script(self) -> bytes:
        return self._verification_script

    def to_json(self) -> Dict[str, Any]:
        import base64
        return {
            'invocation': base64.b64encode(self._invocation_script).decode(),
            'verification': base64.b64encode(self._verification_script).decode()
        }

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> Witness:
        invocation = base64.b64decode(json['invocation'])
        verification = base64.b64decode(json['verification'])
        return cls(invocation, verification)
