from boa3.builtin import public


@public
def str_to_bytes() -> bytes:
    return str.to_bytes('123')
