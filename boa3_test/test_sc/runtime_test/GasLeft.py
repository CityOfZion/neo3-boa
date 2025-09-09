from boa3.sc.compiletime import public
from boa3.sc.runtime import gas_left


@public
def Main() -> int:
    return gas_left
