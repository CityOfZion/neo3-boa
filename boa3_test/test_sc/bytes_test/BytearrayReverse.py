from boa3.sc.compiletime import public


@public
def Main() -> bytearray:
    a = bytearray(b'\x01\x02\x03')
    a.reverse()
    return a
