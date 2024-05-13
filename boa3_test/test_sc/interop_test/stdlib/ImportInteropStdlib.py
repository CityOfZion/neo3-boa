from boa3.builtin import interop
from boa3.sc.compiletime import public


@public
def main(value: str, base: int) -> int:
    return interop.stdlib.atoi(value, base)
