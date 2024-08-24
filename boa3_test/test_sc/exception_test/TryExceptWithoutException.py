from boa3.sc.compiletime import public


@public
def test_try_except(arg: int) -> int:
    try:
        x = arg
    except:
        x = 0

    return x
