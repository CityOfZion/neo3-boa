from boa3.builtin.interop.runtime import invocation_counter


def Main(example: int) -> int:
    invocation_counter = example
    return invocation_counter
