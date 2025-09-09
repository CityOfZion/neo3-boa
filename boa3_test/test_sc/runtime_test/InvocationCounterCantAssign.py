from boa3.sc.compiletime import public
from boa3.sc.runtime import invocation_counter


@public
def Main(example: int) -> int:
    invocation_counter = example
    return invocation_counter


def interop_call():
    x = invocation_counter
