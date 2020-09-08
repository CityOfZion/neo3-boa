def test_try_except(arg: int) -> int:
    try:
        x = arg
    except BaseException:
        x = 0

    return x
