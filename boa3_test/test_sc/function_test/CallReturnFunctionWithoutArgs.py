from boa3.builtin.compile_time import public


@public
def Main() -> int:
    a = TestFunction()
    return a


def TestFunction() -> int:
    return 1
