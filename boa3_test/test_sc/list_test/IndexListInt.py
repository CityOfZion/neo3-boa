from boa3.sc.compiletime import public


@public
def main(a: list[int], value: int) -> int:
    return a.index(value)
