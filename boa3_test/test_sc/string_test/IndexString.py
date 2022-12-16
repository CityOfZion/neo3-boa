from boa3.builtin.compile_time import public


@public
def main(a: str, value: str, start: int, end: int) -> int:
    return a.index(value, start, end)
