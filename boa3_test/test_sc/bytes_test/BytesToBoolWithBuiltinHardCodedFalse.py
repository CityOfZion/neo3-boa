from boa3.builtin.compile_time import public


@public
def bytes_to_bool() -> bool:
    return bytes.to_bool(b'\x00')
