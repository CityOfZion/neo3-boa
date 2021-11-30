from boa3.builtin import public


@public
def bytes_mult(a: bytes, b: int) -> bytes:
    return a * b
