from boa3.builtin import public


@public
def Main(a: bytearray) -> bytes:
    a[-1] = 0x01  # raises runtime error if the value is out of range(256)
    return a
