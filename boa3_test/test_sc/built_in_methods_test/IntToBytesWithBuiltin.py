from boa3.builtin import public


@public
def int_to_bytes() -> bytes:
    return int.to_bytes(123)
