from boa3.builtin.compile_time import public


@public
def test_raise(arg: int):
    if arg < 0:
        raise Exception('raised an exception')
