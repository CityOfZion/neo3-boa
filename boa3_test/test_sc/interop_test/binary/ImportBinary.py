from boa3.builtin import public
from boa3.builtin.interop import binary


@public
def main(value: str, base: int) -> int:
    return binary.atoi(value, base)
