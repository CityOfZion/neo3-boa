# type: ignore

from enum import Enum
from typing import Iterable

from boa3.internal.neo3.core import Size, serialization


def get_var_size(value: object) -> int:
    """
    Determine the variable size of an object.

    Note:
        This function is only used internally for correctly returning object sizes of network payloads to be in line
        with C#'s output.

    Args:
        value: any object type

    Raises:
        TypeError: if a specific Iterable type is not supported.
        ValueError: if a specific object type is not supported .
    """
    # public static int GetVarSize(this string value)
    if isinstance(value, str):
        value_size = len(value.encode('utf-8'))
        return get_var_size(value_size) + value_size

    # internal static int GetVarSize(int value)
    elif isinstance(value, int):
        if (value < 0xFD):
            return Size.uint8
        elif (value <= 0xFFFF):
            return Size.uint8 + Size.uint16
        else:
            return Size.uint8 + Size.uint32

    # internal static int GetVarSize<T>(this T[] value)
    elif isinstance(value, Iterable):
        value_length = len(value)
        value_size = 0

        if value_length > 0:
            if isinstance(value[0], serialization.ISerializable):
                value_size = sum(map(lambda t: len(t), value))
            elif isinstance(value[0], Enum):
                # Note: currently all Enum's in neo core (C#) are of type Byte. Only porting that part of the code
                value_size = value_length * Size.uint8
            elif isinstance(value, (bytes, bytearray)):
                # experimental replacement for: value_size = value.Length * Marshal.SizeOf<T>();
                # because I don't think we have a reliable 'SizeOf' in python
                value_size = value_length * Size.uint8
            else:
                raise TypeError(
                    f"Cannot accurately determine size of objects that do not inherit from 'ISerializable', "
                    f"'Enum' or 'bytes'. Found type: {type(value[0])}")
    else:
        raise ValueError(f"[NOT SUPPORTED] Unexpected value type {type(value)} for get_var_size()")

    return get_var_size(value_length) + value_size
