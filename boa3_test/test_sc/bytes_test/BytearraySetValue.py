from boa3.builtin import public


@public
def Main(arg: bytes) -> bytes:
    a = bytearray(arg)
    a[0] = 0x01  # raises runtime error if the value is out of range(256)
    return a
