from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(key: str) -> bytes:
    return StdLib.base58_check_decode(key)
