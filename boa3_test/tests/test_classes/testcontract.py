from typing import Optional


class TestContract:
    def __init__(self, path: str):
        self._nef_path: str = path

        script_hash = None
        if path.endswith('.nef'):
            with open(path, mode='rb') as nef:
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
