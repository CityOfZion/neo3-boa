from boa3.builtin.compile_time import public


@public
def test_try_except(arg: int) -> int:
    x = arg // 4
    try:
        x += arg
    except:
        x = -x
    finally:
        x *= 2

    return x
