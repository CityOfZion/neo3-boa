from boa3.builtin.compile_time import public


@public
def Main(a: str, b: int) -> bool:
    return a != b
