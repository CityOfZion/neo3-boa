from boa3.sc.compiletime import public


@public
def range_example(start: int, stop: int, step: int) -> range:
    return range(start, stop, step)
