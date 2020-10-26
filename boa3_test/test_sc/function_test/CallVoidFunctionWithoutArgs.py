from boa3.builtin import public


@public
def Main() -> bool:
    TestFunction()
    return True


def TestFunction():
    a = 1
