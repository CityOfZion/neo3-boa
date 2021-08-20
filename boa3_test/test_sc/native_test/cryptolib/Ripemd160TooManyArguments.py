from boa3.builtin.nativecontract.cryptolib import CryptoLib


def Main() -> bytes:
    return CryptoLib.ripemd160('arg', 'arg')
