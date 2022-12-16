from boa3.builtin.compile_time import public


@public
def sub(a: int, b: int) -> int:
    return a - b
