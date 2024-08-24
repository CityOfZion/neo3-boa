from boa3.sc.compiletime import public


@public
def Main() -> bool:
    TestFunction()
    return True


def TestFunction():
    a = 1
