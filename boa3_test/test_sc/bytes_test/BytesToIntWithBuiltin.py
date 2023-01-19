from boa3.builtin.compile_time import public


@public
def bytes_to_int() -> int:
    return bytes.to_int(b'\x01\x02')
