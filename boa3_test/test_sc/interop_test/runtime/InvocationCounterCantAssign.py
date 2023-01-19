from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import invocation_counter


@public
def Main(example: int) -> int:
    invocation_counter = example
    return invocation_counter


def interop_call():
    x = invocation_counter
