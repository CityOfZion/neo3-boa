from typing import Any, Self

from boa3.internal.neo3.core.types import UInt160
from boa3_test.tests.test_classes.contract.neostruct import NeoStruct


class NeoPermissionsStruct(NeoStruct):
    _contract_fields = 'contract'
    _methods_fields = 'methods'

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
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
    def get_contract(cls, value: Any) -> UInt160 | bytes | None:
        if cls._is_wildcard(value):
            return None

        if isinstance(value, str):
            if len(value) == 40 or len(value) == 42:
                return UInt160.from_string(value)
            return bytes.fromhex(value)

    @classmethod
    def get_methods(cls, value: Any) -> list | None:
        if cls._is_wildcard(value):
            return None
        else:
            return [method for method in value]
