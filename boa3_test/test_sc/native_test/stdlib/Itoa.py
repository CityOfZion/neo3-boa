from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(value: int, base: int) -> str:
    return StdLib.itoa(value, base)
