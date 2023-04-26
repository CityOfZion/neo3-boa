from __future__ import annotations

from typing import Union

from boa3.builtin.compile_time import NeoMetadata
from boa3.internal import constants
from boa3.internal.neo3.core.types import UInt160


class CompiledMetadata:
    _instance = None

    @classmethod
    def instance(cls) -> CompiledMetadata:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._metadata = NeoMetadata()

    @classmethod
    def reset(cls):
        cls.instance()._metadata = NeoMetadata()

    @classmethod
    def set_current_metadata(cls, metadata: NeoMetadata):
        cls.instance()._metadata = metadata

    def add_contract_permission(self, contract: Union[UInt160, bytes, str], method: str = None):
        if isinstance(contract, bytes):
            contract = UInt160(contract)
        elif not isinstance(contract, UInt160):
            contract = UInt160.from_string(contract)
        contract_hex_script = str(contract)
        method_string = method if isinstance(method, str) and len(method) > 0 else constants.IMPORT_WILDCARD

        # look for permissions for the given contract
        existing_permission = next((permission for permission in self._metadata.permissions
                                    if ('contract' in permission
                                        and permission['contract'] == contract_hex_script)
                                    ), None)

        if existing_permission is not None:
            # if there's already a permission, include the method name
            permitted_methods = existing_permission['methods'] if 'methods' in existing_permission else []

            # if it's using the wildcard, all methods in this contract can already be called
            if permitted_methods != constants.IMPORT_WILDCARD:
                if method_string == constants.IMPORT_WILDCARD:
                    existing_permission['methods'] = constants.IMPORT_WILDCARD
                else:
                    if method_string not in permitted_methods:
                        permitted_methods.append(method_string)

                    if 'methods' not in existing_permission:
                        existing_permission['methods'] = permitted_methods

            return

        # look for generic permissions for the given method
        existing_permission = next((permission for permission in self._metadata.permissions
                                    if ('contract' in permission
                                        and permission['contract'] == constants.IMPORT_WILDCARD
                                        and 'method' in permission
                                        and (permission['methods'] == constants.IMPORT_WILDCARD
                                             or method_string in permission['methods']))
                                    ), None)

        if existing_permission is None:
            # if no permission is found, include it
            self._metadata.add_permission(contract=contract_hex_script,
                                          methods=([method_string] if method_string != constants.IMPORT_WILDCARD
                                                   else method_string))
