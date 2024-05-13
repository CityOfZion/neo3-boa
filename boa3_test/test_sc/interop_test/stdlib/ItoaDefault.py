from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(value: int) -> str:
    return StdLib.itoa(value)
