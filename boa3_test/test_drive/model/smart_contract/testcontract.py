from typing import Optional

from boa3 import constants
from boa3.neo import to_hex_str


class TestContract:
    def __init__(self, file_path: str, manifest_path: str):
        self._nef_path: str = file_path
        self._manifest_path: str = manifest_path
        self._manifest: dict = self._read_manifest()
        self._script_hash: Optional[bytes] = None

    @property
    def path(self) -> str:
        return self._nef_path

    @property
    def script_hash(self) -> Optional[bytes]:
        return self._script_hash

    @script_hash.setter
    def script_hash(self, new_value: Optional[bytes]):
        if self._script_hash is None and isinstance(new_value, bytes) and len(new_value) == constants.SIZE_OF_INT160:
            self._script_hash = new_value

    @property
    def name(self) -> str:
        return self._manifest['name'] if 'name' in self._manifest else None

    def _read_manifest(self) -> dict:
        try:
            with open(self._manifest_path) as manifest_output:
                import json
                manifest = json.loads(manifest_output.read())
        except BaseException:
            manifest = {}

        return manifest

    def is_valid_identifier(self, item: str) -> bool:
        # valid identifiers are nef path or a representation of the script hash
        return (item == self._nef_path
                or item == self._script_hash
                or (self._script_hash is not None and item == to_hex_str(self._script_hash)))

    def __str__(self) -> str:
        return '[{0}] {1}'.format(to_hex_str(self._script_hash) if isinstance(self._script_hash, bytes) else ' ',
                                  self.name)

    def __repr__(self) -> str:
        return str(self)

    def get_identifier(self) -> str:
        if self.name.isspace() and self._script_hash is not None:
            return to_hex_str(self._script_hash)
        return self.name if ' ' not in self.name else f'"{self.name}"'
