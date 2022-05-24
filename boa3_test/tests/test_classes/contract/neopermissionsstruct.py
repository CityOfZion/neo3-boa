from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.neo3.core.types import UInt160
from boa3_test.tests.test_classes.contract.neostruct import NeoStruct


class NeoPermissionsStruct(NeoStruct):
    _contract_fields = 'contract'
    _methods_fields = 'methods'

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> NeoPermissionsStruct:
        required_fields = [cls._contract_fields,
                           cls._methods_fields
                           ]
        cls._validate_json(json, required_fields)

        struct = cls()
        struct.append(cls.get_contract(json[cls._contract_fields]))
        struct.append(cls.get_methods(json[cls._methods_fields]))
        return struct

    @classmethod
    def _is_wildcard(cls, value: Any) -> bool:
        if value is None:
            return True
        return value == '*'

    @classmethod
    def get_contract(cls, value: Any) -> Optional[UInt160]:
        if cls._is_wildcard(value):
            return None

        # TODO: Permissions are not implemented yet
        return UInt160()

    @classmethod
    def get_methods(cls, value: Any) -> Optional[list]:
        if cls._is_wildcard(value):
            return None

        # TODO: Permissions are not implemented yet
        return []
