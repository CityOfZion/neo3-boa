from boa3.builtin.compile_time import public


@public
def test_try_except(arg: int) -> int:
    try:
        x = arg
    except BaseException:
        x = 0
    else:
        x = -arg

    return x
