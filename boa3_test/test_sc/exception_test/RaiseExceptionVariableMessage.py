from boa3.builtin.compile_time import public


@public
def test_raise(arg: int):
    x = 'raised an exception'
    if arg < 0:
        raise Exception(x)
