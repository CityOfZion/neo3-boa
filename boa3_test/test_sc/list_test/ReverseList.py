from boa3.sc.compiletime import public


@public
def Main() -> list[int]:
    a: list[int] = [1, 2, 3]
    a.reverse()
    return a
