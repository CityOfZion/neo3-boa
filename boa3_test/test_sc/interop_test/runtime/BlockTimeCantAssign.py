from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import time


@public
def Main(example: int) -> int:
    time = example
    return time


def interop_call():
    x = time
