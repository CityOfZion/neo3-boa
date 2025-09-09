from boa3.sc.compiletime import public
from boa3.sc.types import CallFlags


@public
def main(x: int) -> CallFlags:
    return CallFlags(x)
