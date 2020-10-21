from boa3.builtin import public


@public
def test_raise(arg: int):
    if arg < 0:
        raise ValueError
