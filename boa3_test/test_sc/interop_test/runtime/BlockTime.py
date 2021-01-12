from boa3.builtin import public
from boa3.builtin.interop.runtime import get_time


@public
def Main() -> int:
    return get_time
