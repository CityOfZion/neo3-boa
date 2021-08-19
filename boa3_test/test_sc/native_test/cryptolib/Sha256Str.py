from boa3.builtin import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def Main(test: str) -> bytes:
    return CryptoLib.sha256(test)
