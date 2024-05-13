from boa3.sc.compiletime import public


@public
def Main(op: str, args: list) -> list[int]:
    a = [1, 2, 3]
    a.clear()
    return a
