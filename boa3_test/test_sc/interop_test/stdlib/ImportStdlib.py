from boa3.builtin.interop import stdlib
from boa3.sc.compiletime import public


@public
def main(value: str, base: int) -> int:
    return stdlib.atoi(value, base)
