from boa3.sc.compiletime import public


@public
def Main() -> bool:
    TestAdd(1, 2)
    return True


def TestAdd(a: int, b: int):
    c = a + b
