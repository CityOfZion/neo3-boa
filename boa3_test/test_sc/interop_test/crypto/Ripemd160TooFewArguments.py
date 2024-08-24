from boa3.sc.contracts import CryptoLib


def Main() -> bytes:
    return CryptoLib.ripemd160()
