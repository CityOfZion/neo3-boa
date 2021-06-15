from boa3.builtin import interop, public


@public
def main() -> int:
    return interop.runtime.time + interop.runtime.gas_left + interop.runtime.invocation_counter
