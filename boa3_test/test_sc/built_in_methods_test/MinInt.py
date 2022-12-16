from boa3.builtin.compile_time import public


@public
def main(val1: int, val2: int) -> int:
    return min(val1, val2)
