from boa3.builtin.compile_time import public


@public
def Main(a: str) -> str:
    b = a[0]
    return b
