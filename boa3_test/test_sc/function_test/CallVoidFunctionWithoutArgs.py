from boa3.builtin.compile_time import public


@public
def Main() -> bool:
    TestFunction()
    return True


def TestFunction():
    a = 1
