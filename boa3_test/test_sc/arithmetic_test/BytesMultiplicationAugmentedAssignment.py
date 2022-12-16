from boa3.builtin.compile_time import public


@public
def Main(a: bytes, b: int) -> bytes:
    a *= b
    return a
