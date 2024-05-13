from boa3.sc.compiletime import public


@public
def main(a: str, value: str, start: int) -> int:
    return a.index(value, start)
