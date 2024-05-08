from typing import Any, Self

from boa3_test.tests.test_classes.contract.neoeventstruct import NeoEventStruct
from boa3_test.tests.test_classes.contract.neomethodstruct import NeoMethodStruct
from boa3_test.tests.test_classes.contract.neostruct import NeoStruct


class NeoAbiStruct(NeoStruct):
    _methods_field = 'methods'
    _events_field = 'events'

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        required_fields = [cls._methods_field,
                           cls._events_field
                           ]
        cls._validate_json(json, required_fields)

        struct = cls()
        struct.append(cls._get_methods(json[cls._methods_field]))
        struct.append(cls._get_events(json[cls._events_field]))

        return struct

    @classmethod
    def _get_methods(cls, json_list: list[dict[str, Any]]) -> list[NeoMethodStruct]:
        return [NeoMethodStruct.from_json(method_json) for method_json in json_list]

    @classmethod
    def _get_events(cls, json_list: list[dict[str, Any]]) -> list[NeoEventStruct]:
        return [NeoEventStruct.from_json(method_json) for method_json in json_list]
