from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib


@public
def Main() -> bytes:
    return CryptoLib.sha256(b'unit test')
