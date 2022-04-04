from boa3.builtin import public
from boa3.builtin.interop.runtime import gas_left


@public
def Main() -> int:
    return gas_left
