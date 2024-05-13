from boa3.sc.compiletime import public


def TestAdd(a: int, b: int) -> int:
    return a + b


@public
def Main() -> int:
    return TestAdd(1, 2)
