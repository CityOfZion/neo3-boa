from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import gas_left


@public
def Main() -> int:
    return gas_left
