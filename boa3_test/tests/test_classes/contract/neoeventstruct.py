from __future__ import annotations

from typing import Any, Dict

from boa3_test.tests.test_classes.contract.neostruct import NeoStruct


class NeoEventStruct(NeoStruct):
    _name_field = 'name'
    _parameters_field = 'parameters'

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> NeoEventStruct:
        required_fields = [cls._name_field,
                           cls._parameters_field
                           ]
        cls._validate_json(json, required_fields)

        struct = cls()
        struct.append(json[cls._name_field])
        struct.append([cls._get_param_info(arg) for arg in json[cls._parameters_field]])

        return struct
