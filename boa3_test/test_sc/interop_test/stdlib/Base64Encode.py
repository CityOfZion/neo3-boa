from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def Main(key: bytes) -> str:
    return StdLib.base64_encode(key)
