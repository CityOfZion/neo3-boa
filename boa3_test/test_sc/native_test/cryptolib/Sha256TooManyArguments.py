from boa3.builtin.nativecontract.cryptolib import CryptoLib


def Main() -> bytes:
    return CryptoLib.sha256('arg', 'arg')
