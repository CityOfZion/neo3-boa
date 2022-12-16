from boa3.builtin.compile_time import public


@public
def Main() -> bool:
    TestAdd(1, 2)
    return True


def TestAdd(a: int, b: int):
    c = a + b
