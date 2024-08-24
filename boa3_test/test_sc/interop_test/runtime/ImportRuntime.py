from boa3.sc import runtime
from boa3.sc.compiletime import public


@public
def main() -> int:
    return runtime.gas_left + runtime.invocation_counter
