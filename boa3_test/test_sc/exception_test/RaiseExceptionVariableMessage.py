from boa3.sc.compiletime import public


@public
def test_raise(arg: int):
    x = 'raised an exception'
    if arg < 0:
        raise Exception(x)
