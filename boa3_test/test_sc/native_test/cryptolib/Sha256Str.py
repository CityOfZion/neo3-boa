from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def Main(test: str) -> bytes:
    return CryptoLib.sha256(test)
