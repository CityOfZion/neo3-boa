from boa3.builtin import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def Main() -> bytes:
    return CryptoLib.ripemd160(b'unit test')
