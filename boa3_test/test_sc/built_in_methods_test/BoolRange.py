from boa3.sc.compiletime import public


@public
def range_0() -> bool:
    return bool(range(0))


@public
def range_not_0() -> bool:
    return bool(range(10))
