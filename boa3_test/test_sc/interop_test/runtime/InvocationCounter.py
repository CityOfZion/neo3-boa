from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import invocation_counter


@public
def Main() -> int:
    return invocation_counter
