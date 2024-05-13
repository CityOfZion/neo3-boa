from boa3.sc.compiletime import public


@public
def test_raise(arg: int):
    if arg < 0:
        raise Exception
