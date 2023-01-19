from boa3.builtin.compile_time import public


@public
def Main():
    a: bytearray = bytearray(b'\x01\x02\x03')
