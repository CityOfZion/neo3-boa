from boa3.builtin.compile_time import public


@public
def Main() -> bytearray:
    a = bytearray(b'\x01\x02\x03')
    a.extend(b'\x04\x05\x06')
    return a
