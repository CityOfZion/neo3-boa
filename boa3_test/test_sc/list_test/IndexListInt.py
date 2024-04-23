from boa3.builtin.compile_time import public


@public
def main(a: list[int], value: int) -> int:
    return a.index(value)
