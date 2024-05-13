from boa3.sc.compiletime import public


@public
def Main() -> int:
    a = TestAdd(1, 2)
    return a


def TestAdd(a: int, b: int) -> int:
    return a + b
