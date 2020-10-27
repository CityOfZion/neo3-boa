from boa3.builtin import public


@public
def test_raise(arg: int):
    x = Exception
    if arg < 0:
        raise x
