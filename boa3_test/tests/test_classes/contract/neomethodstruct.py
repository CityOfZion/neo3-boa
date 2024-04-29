from typing import Any, Self

from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType
from boa3_test.tests.test_classes.contract.neostruct import NeoStruct


class NeoMethodStruct(NeoStruct):
    _name_field = 'name'
    _parameters_field = 'parameters'
    _return_type_field = 'returntype'
    _offset_field = 'offset'
    _is_safe_field = 'safe'

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        required_fields = [cls._name_field,
                           cls._parameters_field,
                           cls._return_type_field,
                           cls._offset_field,
                           cls._is_safe_field
                           ]
        cls._validate_json(json, required_fields)

        struct = cls()
        struct.append(json[cls._name_field])
        struct.append([cls._get_param_info(arg) for arg in json[cls._parameters_field]])
        struct.append(ContractParameterType._get_by_name(json[cls._return_type_field]))
        struct.append(json[cls._offset_field])
        struct.append(json[cls._is_safe_field])

        return struct
