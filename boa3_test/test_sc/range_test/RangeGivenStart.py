from boa3.sc.compiletime import public


@public
def range_example(start: int, stop: int) -> range:
    return range(start, stop)
