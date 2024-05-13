from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(value: str, base: int) -> int:
    return StdLib.atoi(value, base)
