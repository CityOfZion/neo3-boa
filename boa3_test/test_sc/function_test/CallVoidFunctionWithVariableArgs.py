from boa3.builtin import public


@public
def Main() -> bool:
    a = 1
    b = 2
    TestAdd(a, b)
    return True


def TestAdd(a: int, b: int):
    c = a + b
