from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(arg: bytes) -> str:
    return StdLib.hex_encode(arg)
