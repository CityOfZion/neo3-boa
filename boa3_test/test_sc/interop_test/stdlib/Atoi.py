from boa3.builtin import public
from boa3.builtin.interop.stdlib import atoi


@public
def main(value: str, base: int) -> int:
    return atoi(value, base)
