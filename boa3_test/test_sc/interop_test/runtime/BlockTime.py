from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import time


@public
def Main() -> int:
    return time
