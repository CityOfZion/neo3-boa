from typing import MutableSequence


def Main() -> MutableSequence[int]:
    a: MutableSequence[int] = bytearray(b'\x01\x02\x03')
    MutableSequence.reverse(a)
    return a
