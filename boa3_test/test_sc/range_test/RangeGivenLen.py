from boa3.sc.compiletime import public


@public
def range_example(size: int) -> range:
    return range(size)
