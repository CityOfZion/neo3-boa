from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(key: bytes) -> str:
    return StdLib.base58_check_encode(key)
