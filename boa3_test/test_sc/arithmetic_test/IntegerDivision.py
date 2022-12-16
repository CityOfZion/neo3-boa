from boa3.builtin.compile_time import public


@public
def floor_div(a: int, b: int) -> int:
    return a // b
