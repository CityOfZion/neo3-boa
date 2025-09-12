from boa3.sc.compiletime import public
from boa3.sc.runtime import time


@public
def Main(example: int) -> int:
    time = example
    return time


def interop_call():
    x = time
