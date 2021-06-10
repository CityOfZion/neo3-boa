from boa3.builtin import interop, public


@public
def main(value: str, base: int) -> int:
    return interop.binary.atoi(value, base)
