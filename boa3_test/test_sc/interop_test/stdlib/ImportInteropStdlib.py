from boa3.builtin import interop, public


@public
def main(value: str, base: int) -> int:
    return interop.stdlib.atoi(value, base)
