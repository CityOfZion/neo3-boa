from boa3.builtin import public


@public
def Main():
    a = b'\x01\x02\x03'
    b: bytearray = bytearray(a)
