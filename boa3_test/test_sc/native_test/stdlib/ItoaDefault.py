from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(value: int) -> str:
    return StdLib.itoa(value)
