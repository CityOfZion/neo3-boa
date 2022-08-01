from boa3.builtin import public


@public
def main(a: bytes, value: bytes, start: int) -> int:
    return a.index(value, start)
