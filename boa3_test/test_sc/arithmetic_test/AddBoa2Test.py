from boa3.builtin.compile_time import public


@public
def main(m: int) -> int:
    c = m + 2
    return c
