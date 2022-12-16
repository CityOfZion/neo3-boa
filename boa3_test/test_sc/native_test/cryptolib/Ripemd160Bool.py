from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def Main() -> bytes:
    return CryptoLib.ripemd160(True)
