from boa3.builtin import public
from boa3.builtin.interop import runtime


@public
def main() -> int:
    return runtime.get_time + runtime.gas_left + runtime.invocation_counter
