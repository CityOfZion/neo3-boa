from collections.abc import Sequence
from typing import Any

from boa3.internal.neo.core.types.InteropInterface import InteropInterface
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3.internal.neo.vm.type.String import String


def stack_item_from_json(item: dict[str, Any]) -> Any:
    if 'type' not in item:
        return None

    item_type: StackItemType = StackItemType.get_stack_item_type(item['type'])
    if item_type is StackItemType.InteropInterface:
        if 'value' in item:
            interop_interface = item['value']
        else:
            interop_interface = item

        if isinstance(interop_interface, dict) and 'iterator' in interop_interface:
            return [stack_item_from_json(value) for value in interop_interface['iterator']]
        else:
            return InteropInterface

    if item_type is StackItemType.Any or 'value' not in item:
        return None

    value: Any = None
    item_value: Any = item['value']

    if item_type is StackItemType.Boolean:
        if isinstance(item_value, str) and item_value in (str(True), str(False)):
            item_value = item_value == str(True)
        if not isinstance(item_value, bool):
            raise ValueError
        value = item_value

    elif item_type is StackItemType.Integer:
        if isinstance(item_value, str):
            item_value = int(item_value)
        if not isinstance(item_value, int):
            raise ValueError
        value = item_value

    elif item_type in (StackItemType.ByteString, StackItemType.Buffer):
        if not isinstance(item_value, str):
            raise ValueError

        import base64
        decoded: bytes = base64.b64decode(item_value)

        try:
            value = String.from_bytes(decoded)
        except BaseException:
            value = decoded

    elif item_type in (StackItemType.Array, StackItemType.Struct):
        if not isinstance(item_value, Sequence) or isinstance(item_value, (str, bytes)):
            raise ValueError
        value = [stack_item_from_json(x) for x in item_value]

    elif item_type is StackItemType.Map:
        if not isinstance(item_value, Sequence):
            raise ValueError
        value = {}

        for x in item_value:
            if 'key' not in x or 'value' not in x:
                raise ValueError
            value[stack_item_from_json(x['key'])] = stack_item_from_json(x['value'])

    return value


def bytes_from_json(item: dict[str, Any]) -> bytes | None:
    value = stack_item_from_json(item)

    if isinstance(value, str):
        value = String(value).to_bytes()
    elif isinstance(value, int):
        value = Integer(value).to_byte_array()

    return value if isinstance(value, bytes) else None


def contract_parameter_to_json(value: Any) -> dict[str, Any]:
    if value is None:
        return {'type': AbiType.Any}

    stack_type: AbiType = AbiType.Any
    parameter_value: Any = None

    if isinstance(value, bool):
        stack_type = AbiType.Boolean
        parameter_value = value
    elif isinstance(value, int):
        stack_type = AbiType.Integer
        parameter_value = value
    elif isinstance(value, str):
        stack_type = AbiType.String
        parameter_value = value
    elif isinstance(value, (bytes, bytearray)):
        import base64
        stack_type = AbiType.ByteArray
        parameter_value = String.from_bytes(base64.b64encode(value))
    elif isinstance(value, Sequence):
        stack_type = AbiType.Array
        parameter_value = [contract_parameter_to_json(x) for x in value]
    elif isinstance(value, dict):
        stack_type = AbiType.Map
        parameter_value = [{'key': contract_parameter_to_json(key),
                            'value': contract_parameter_to_json(value)
                            } for key, value in value.items()
                           ]

    result = {'type': stack_type.value}
    if parameter_value is not None:
        result['value'] = parameter_value

    return result
