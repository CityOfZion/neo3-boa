from boa3.sc.compiletime import public


@public
def Main():
    a: bytearray = b'\x01\x02\x03'  # mismatched type error
