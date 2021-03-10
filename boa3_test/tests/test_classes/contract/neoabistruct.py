from __future__ import annotations

from typing import Any, Dict, List

from boa3_test.tests.test_classes.contract.neoeventstruct import NeoEventStruct
from boa3_test.tests.test_classes.contract.neomethodstruct import NeoMethodStruct
from boa3_test.tests.test_classes.contract.neostruct import NeoStruct


class NeoAbiStruct(NeoStruct):
    _methods_field = 'methods'
    _events_field = 'events'

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> NeoAbiStruct:
        required_fields = [cls._methods_field,
                           cls._events_field
                           ]
        cls._validate_json(json, required_fields)

        struct = cls()
        struct.append(cls._get_methods(json[cls._methods_field]))
        struct.append(cls._get_events(json[cls._events_field]))

        return struct

    @classmethod
    def _get_methods(cls, json_list: List[Dict[str, Any]]) -> List[NeoMethodStruct]:
        return [NeoMethodStruct.from_json(method_json) for method_json in json_list]

    @classmethod
    def _get_events(cls, json_list: List[Dict[str, Any]]) -> List[NeoEventStruct]:
        return [NeoEventStruct.from_json(method_json) for method_json in json_list]
