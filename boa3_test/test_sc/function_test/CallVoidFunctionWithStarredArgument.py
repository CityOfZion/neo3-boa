from boa3.builtin import public


@public
def Main() -> bool:
    a = 1
    b = 2
    TestAdd(a, b)
    return True


def TestAdd(*args: int):
    c = sum(args)
