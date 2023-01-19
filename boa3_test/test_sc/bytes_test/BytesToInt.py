from boa3.builtin.compile_time import public


@public
def bytes_to_int() -> int:
    return b'\x01\x02'.to_int()
