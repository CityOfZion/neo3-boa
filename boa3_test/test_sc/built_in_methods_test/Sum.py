from boa3.builtin.compile_time import public


@public
def main(x: list[int]) -> int:
    return sum(x)
