from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def Main(key: str) -> bytes:
    return StdLib.base64_decode(key)
