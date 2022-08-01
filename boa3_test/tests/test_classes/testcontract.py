import os
from typing import Optional

from boa3.neo import to_hex_str
from boa3.neo.vm.type.StackItem import StackItemType


class TestContract:
    def __init__(self, file_path: str, manifest_path: str):
        self._nef_path: str = file_path
        self._manifest_path: str = manifest_path
        self._script_hash: Optional[bytes] = self._get_script_hash()
        self._manifest: dict = self._read_manifest()

    def _get_script_hash(self) -> bytes:
        file_path = self._nef_path
        if file_path.endswith('.nef') and os.path.isfile(file_path):
            with open(file_path, mode='rb') as nef:
                file = nef.read()
            from boa3.neo.contracts.neffile import NefFile
            return NefFile.deserialize(file).script_hash

    def _read_manifest(self) -> dict:
        try:
            with open(self._manifest_path) as manifest_output:
                import json
                manifest = json.loads(manifest_output.read())
        except BaseException:
            manifest = {}

        return manifest

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

    def get_method_return_type(self, called_method: str) -> StackItemType:
        cur_json = self._manifest
        return_type = StackItemType.Any

        if 'abi' in cur_json:
            cur_json = cur_json['abi']
            if 'methods' in cur_json:
                cur_json = cur_json['methods']
                method_json = next((node for node in cur_json
                                    if 'name' in node and node['name'] == called_method),
                                   {})
                if 'returntype' in method_json:
                    return_type = StackItemType.get_stack_item_type(method_json['returntype'])

        return return_type
