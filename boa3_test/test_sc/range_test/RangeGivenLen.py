from boa3.builtin import public


@public
def range_example(size: int) -> range:
    return range(size)
