from boa3.builtin import public


@public
def bytes_to_int() -> int:
    return bytearray.to_int(bytearray(b'\x01\x02'))
