from boa3.sc.compiletime import public
from boa3.sc import runtime


@public
def main() -> int:
    return runtime.gas_left + runtime.invocation_counter
