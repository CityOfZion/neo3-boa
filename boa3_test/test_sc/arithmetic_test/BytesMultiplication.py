from boa3.sc.compiletime import public


@public
def bytes_mult(a: bytes, b: int) -> bytes:
    return a * b
