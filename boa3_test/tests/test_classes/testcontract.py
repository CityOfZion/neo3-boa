import os
from typing import Optional

from boa3.neo import to_hex_str


class TestContract:
    def __init__(self, file_path: str):
        self._nef_path: str = file_path
        self._script_hash: Optional[bytes] = self._get_script_hash()

    def _get_script_hash(self) -> bytes:
        file_path = self._nef_path
        if file_path.endswith('.nef') and os.path.isfile(file_path):
            with open(file_path, mode='rb') as nef:
                file = nef.read()
            from boa3.neo.contracts.neffile import NefFile
            return NefFile.deserialize(file).script_hash

    @property
    def path(self) -> str:
        return self._nef_path

    @property
    def script_hash(self) -> Optional[bytes]:
        return self._script_hash

    def __str__(self) -> str:
        return f'[{to_hex_str(self._script_hash)}] {self._nef_path}'

    def __repr__(self) -> str:
        return str(self)

    def is_valid_identifier(self, item: str) -> bool:
        # valid identifiers are nef path or a representation of the script hash
        return (item == self._nef_path
                or item == self._script_hash
                or item == to_hex_str(self._script_hash))
