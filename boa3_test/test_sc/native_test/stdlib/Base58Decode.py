from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def Main(key: str) -> bytes:
    return StdLib.base58_decode(key)
