from boa3.builtin.compile_time import public


@public
def add_four(a: int, b: int) -> int:
    return 4 + b + a
