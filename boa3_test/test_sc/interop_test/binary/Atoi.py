from boa3.builtin import public
from boa3.builtin.interop.binary import atoi


@public
def main(value: str, base: int) -> int:
    return atoi(value, base)
