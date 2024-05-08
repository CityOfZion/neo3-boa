from boa3.builtin.compile_time import public


@public
def main(x: list[int], start: int) -> int:
    return sum(x, start)
