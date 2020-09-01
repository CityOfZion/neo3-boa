def test_raise(arg: int):
    x = 'raised an exception'
    if arg < 0:
        raise x
