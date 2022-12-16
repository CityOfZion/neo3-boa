from boa3.builtin.compile_time import public


@public
def test_try_except(arg: int) -> int:
    try:
        x = arg
    except:
        x = 0

    return x
