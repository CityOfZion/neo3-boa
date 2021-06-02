from boa3.builtin.interop.runtime import time


def Main(example: int) -> int:
    global time
    time = example
    return time
