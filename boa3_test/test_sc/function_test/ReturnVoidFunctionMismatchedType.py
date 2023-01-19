from boa3.builtin.compile_time import public


@public
def Main() -> int:
    return TestFunction()


def TestFunction():
    a = 1
