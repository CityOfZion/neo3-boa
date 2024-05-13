from boa3.sc.compiletime import public


@public
def Main() -> int:
    return TestFunction()


def TestFunction():
    a = 1
