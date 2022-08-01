from boa3.builtin import public


@public
def main(a: bytes, value: bytes, start: int, end: int) -> int:
    return a.index(value, start, end)
