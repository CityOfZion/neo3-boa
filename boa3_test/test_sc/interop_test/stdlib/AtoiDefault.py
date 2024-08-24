from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(value: str) -> int:
    return StdLib.atoi(value)
