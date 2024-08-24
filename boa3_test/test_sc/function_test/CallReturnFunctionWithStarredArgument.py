from boa3.sc.compiletime import public


@public
def Main() -> int:
    return TestAdd(1, 2, 3, 4, 5, 6)


def TestAdd(*args: int) -> int:
    return sum(args)
