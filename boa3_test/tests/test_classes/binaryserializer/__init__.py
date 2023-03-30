from typing import Any

from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3.internal.neo3.core.serialization import BinaryReader


def deserialize_binary(reader: BinaryReader) -> Any:
    deserialized_items = []
    underserialized = 1

    while underserialized > 0:
        stack_type = reader.read_byte()
        if stack_type == StackItemType.Any:
            deserialized_items.append(None)
        elif stack_type == StackItemType.Boolean:
            deserialized_items.append(reader.read_bool())
        elif stack_type == StackItemType.Integer:
            value_in_bytes = reader.read_var_bytes()
            deserialized_items.append(Integer.from_bytes(value_in_bytes))
        elif stack_type in (StackItemType.ByteString, StackItemType.Buffer):
            deserialized_items.append(reader.read_var_bytes())
        elif stack_type in (StackItemType.Array, StackItemType.Struct):
            count = reader.read_var_int()
            deserialized_items.append(list(range(count)))
            underserialized += count
        elif stack_type == StackItemType.Map:
            count = reader.read_var_int()
            deserialized_items.append({key: None for key in range(count)})
            underserialized += count * 2
        else:
            raise ValueError

        underserialized -= 1

    stack_temp = []
    while len(deserialized_items) > 0:
        item = deserialized_items.pop()
        if isinstance(item, list):
            new_item = []
            for _ in range(len(item)):
                new_item.append(stack_temp.pop())
            item = new_item
        elif isinstance(item, dict):
            new_item = {}
            for _ in range(0, len(item), 2):
                key = stack_temp.pop()
                value = stack_temp.pop()
                new_item[key] = value
            item = new_item
        stack_temp.append(item)

    return stack_temp.pop()
