from boa3.builtin.compile_time import public


@public
def main(a: int, b: int, c: int, d: int) -> int:

    return a + b - c * d
