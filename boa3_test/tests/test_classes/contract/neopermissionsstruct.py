from __future__ import annotations

from typing import Any, Dict, Optional, Union

from boa3.internal.neo3.core.types import UInt160
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
    def get_contract(cls, value: Any) -> Optional[Union[UInt160, bytes]]:
        if cls._is_wildcard(value):
            return None

        if isinstance(value, str):
            if len(value) == 40 or len(value) == 42:
                return UInt160.from_string(value)
            return bytes.fromhex(value)

    @classmethod
    def get_methods(cls, value: Any) -> Optional[list]:
        if cls._is_wildcard(value):
            return None
        else:
            return [method for method in value]
