from boa3.builtin.compile_time import public


@public
def range_example(size: int) -> range:
    return range(size)
