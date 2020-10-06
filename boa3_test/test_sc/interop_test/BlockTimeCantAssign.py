from boa3.builtin.interop.runtime import get_time


def Main(example: int) -> int:
    global get_time
    get_time = example
    return get_time
