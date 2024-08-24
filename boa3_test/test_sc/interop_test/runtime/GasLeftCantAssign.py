from boa3.sc.compiletime import public
from boa3.sc.runtime import gas_left


@public
def Main(example: int) -> int:
    gas_left = example
    return gas_left


def interop_call():
    x = gas_left
