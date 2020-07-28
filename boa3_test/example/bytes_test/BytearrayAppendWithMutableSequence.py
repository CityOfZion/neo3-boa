from typing import MutableSequence


def Main() -> bytearray:
    a = bytearray(b'\x01\x02\x03')
    MutableSequence.append(a, 4)
    return a
