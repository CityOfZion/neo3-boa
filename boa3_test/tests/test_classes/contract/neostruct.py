from abc import ABC, abstractmethod
from typing import Any, Self


class NeoStruct(list, ABC):

    @classmethod
    @abstractmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        pass

    @classmethod
    def _validate_json(cls, json: dict[str, Any], required_fields: list[str]):
        required = set(required_fields)
        if not required.issubset(json.keys()):
            raise ValueError

    @classmethod
    def _get_param_info(cls, json: dict[str, Any]) -> list:
        _name = 'name'
        _type = 'type'

        required_fields = [_name, _type]
        cls._validate_json(json, required_fields)

        name = json[_name]
        from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType
        try:
            param_type = ContractParameterType._get_by_name(json[_type])
        except BaseException:
            param_type = None

        return [name, param_type]
