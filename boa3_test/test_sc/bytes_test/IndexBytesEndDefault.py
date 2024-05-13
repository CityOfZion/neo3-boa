from boa3.sc.compiletime import public


@public
def main(a: bytes, value: bytes, start: int) -> int:
    return a.index(value, start)
