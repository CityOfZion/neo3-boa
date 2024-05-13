from boa3.sc.compiletime import public


@public
def Main(a: list[int], value: int) -> list[int]:
    a.remove(value)
    return a
