from boa3.builtin.compile_time import public


@public
def str_to_bytes() -> bytes:
    return str.to_bytes('123')
