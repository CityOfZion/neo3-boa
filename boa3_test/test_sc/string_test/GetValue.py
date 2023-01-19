from boa3.builtin.compile_time import public


@public
def Main(a: str) -> str:
    return a[0]
