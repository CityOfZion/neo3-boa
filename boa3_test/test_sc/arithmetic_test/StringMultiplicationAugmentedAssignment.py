from boa3.builtin.compile_time import public


@public
def Main(a: str, b: int) -> str:
    a *= b
    return a
