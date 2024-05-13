from boa3.sc.compiletime import public


@public
def Main() -> list[int]:
    a = [1, 2, 3]
    a.append(4)
    return a
