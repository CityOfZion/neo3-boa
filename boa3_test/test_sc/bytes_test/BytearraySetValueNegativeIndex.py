from boa3.builtin.compile_time import public


@public
def Main(arg: bytes) -> bytes:
    a = bytearray(arg)
    a[-1] = 0x01  # raises runtime error if the value is out of range(256)
    return a
