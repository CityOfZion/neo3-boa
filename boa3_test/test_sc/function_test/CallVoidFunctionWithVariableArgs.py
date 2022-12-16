from boa3.builtin.compile_time import public


@public
def Main() -> bool:
    a = 1
    b = 2
    TestAdd(a, b)
    return True


def TestAdd(a: int, b: int):
    c = a + b
