from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def Main(key: bytes) -> str:
    return StdLib.base64_encode(key)
