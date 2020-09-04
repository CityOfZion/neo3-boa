def test_try_except(arg: int) -> int:
    try:
        x = arg
    except ValueError:
        x = 0

    return x
