from typing import Any, Sequence

from boa3.internal.neo.vm.type.AbiType import AbiType


def value_to_parameter(value: Any) -> Any:
    if isinstance(value, (int, str)):
        return value

    if isinstance(value, (bytes, bytearray)):
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


def handle_return_error(json_result: str) -> dict:
    import json

    index = _get_first_json_closure(json_result)
    result = json.loads(json_result[:index])
    if 'stack' not in result:
        return result

    while index < len(json_result):
        next_index = _get_first_json_closure(json_result, starting_index=index)
        if next_index > index:
            new_object = json.loads(json_result[index:next_index])
            result['stack'].append(new_object)
        else:
            break
        index = next_index

    return result


def _get_first_json_closure(json_result: str, starting_index: int = 0):
    if starting_index < 0:
        starting_index = 0

    open_object = []
    open_array = []

    if len(json_result) == starting_index or json_result[starting_index] != '{':
        return starting_index

    open_object.append(starting_index)
    index = starting_index + 1
    while index < len(json_result) and len(open_object):
        char = json_result[index]
        if char == '{':
            open_object.append(index)
        elif char == '}':
            open_object.pop()
        elif char == '[':
            open_array.append(index)
        elif char == ']':
            open_array.pop()

        index += 1

    return index
