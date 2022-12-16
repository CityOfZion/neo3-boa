from boa3.builtin.compile_time import public


@public
def str_mult(a: str, b: int) -> str:
    return a * b
