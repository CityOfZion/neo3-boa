from typing import Any, Sequence

from boa3.neo.vm.type.AbiType import AbiType


def value_to_parameter(value: Any) -> Any:
    if isinstance(value, (int, str)):
        return value

    if isinstance(value, bytes):
        return bytes_to_hex(value)

    if isinstance(value, Sequence):
        return [value_to_parameter(x) for x in value]

    if isinstance(value, dict):
        return {
            'type': AbiType.Map.value,
            'value': [{'key': value_to_parameter(key),
                       'value': value_to_parameter(value)
                       } for key, value in value.items()
                      ]
        }

    if value is not None:
        raise TypeError(f"Unsupported type: '{type(value)}'")

    return None


def bytes_to_hex(data: bytes) -> str:
    return '0x' + data.hex()
