from collections.abc import MutableSequence

from boa3.sc.compiletime import public


@public
def Main() -> MutableSequence[int]:
    a: MutableSequence[int] = bytearray(b'\x01\x02\x03')
    MutableSequence.reverse(a)
    return a
