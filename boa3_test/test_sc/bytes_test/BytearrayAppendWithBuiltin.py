from boa3.builtin import public


@public
def Main() -> bytearray:
    a = bytearray(b'\x01\x02\x03')
    bytearray.append(a, 4)
    return a
