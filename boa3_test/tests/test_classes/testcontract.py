import os
from typing import Optional


class TestContract:
    def __init__(self, file_path: str):
        self._nef_path: str = file_path

        script_hash = None
        if file_path.endswith('.nef') and os.path.isfile(file_path):
            with open(file_path, mode='rb') as nef:
                file = nef.read()
            from boa3.neo.contracts.neffile import NefFile
            script_hash = NefFile.deserialize(file).script_hash

        self._script_hash: Optional[bytes] = script_hash

    @property
    def path(self) -> str:
        return self._nef_path

    @property
    def script_hash(self) -> Optional[bytes]:
        return self._script_hash
