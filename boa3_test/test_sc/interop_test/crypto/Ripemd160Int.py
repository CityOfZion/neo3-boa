from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib


@public
def Main() -> bytes:
    return CryptoLib.ripemd160(10)
