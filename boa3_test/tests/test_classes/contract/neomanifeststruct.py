from __future__ import annotations

from typing import Any, Dict

from boa3_test.tests.test_classes.contract.neoabistruct import NeoAbiStruct
from boa3_test.tests.test_classes.contract.neopermissionsstruct import NeoPermissionsStruct
from boa3_test.tests.test_classes.contract.neostruct import NeoStruct


class NeoManifestStruct(NeoStruct):
    _name_field = 'name'
    _groups_field = 'groups'
    _supported_standards_field = 'supportedstandards'
    _abi_field = 'abi'
    _permissions_field = 'permissions'
    _trusts_field = 'trusts'
    _features_field = 'features'
    _extra_field = 'extra'

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> NeoManifestStruct:
        required_fields = [cls._name_field,
                           cls._groups_field,
                           cls._supported_standards_field,
                           cls._abi_field,
                           cls._permissions_field,
                           cls._trusts_field,
                           cls._features_field,
                           cls._extra_field
                           ]
        cls._validate_json(json, required_fields)

        struct = cls()
        struct.append(json[cls._name_field])
        struct.append(json[cls._groups_field])
        struct.append({})  # features were not implemented on Neo yet
        struct.append(json[cls._supported_standards_field])
        struct.append(NeoAbiStruct.from_json(json[cls._abi_field]))
        struct.append([NeoPermissionsStruct.from_json(permission) for permission in json[cls._permissions_field]])
        struct.append(json[cls._trusts_field])
        extras = json[cls._extra_field]
        struct.append(extras if extras is not None else "null")

        return struct
