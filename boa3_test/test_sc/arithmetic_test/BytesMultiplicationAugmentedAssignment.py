from boa3.builtin import public


@public
def Main(a: bytes, b: int) -> bytes:
    a *= b
    return a
