from boa3.builtin.compile_time import public


@public
def Main(a: bytes) -> int:
    return a[0]
