from boa3.builtin.compile_time import public
from boa3.builtin.interop import runtime


@public
def main() -> int:
    return runtime.gas_left + runtime.invocation_counter
