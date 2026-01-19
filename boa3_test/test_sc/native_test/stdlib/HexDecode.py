from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(arg: str) -> bytes:
    return StdLib.hex_decode(arg)
