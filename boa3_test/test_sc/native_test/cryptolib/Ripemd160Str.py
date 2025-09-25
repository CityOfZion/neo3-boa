from boa3.sc.contracts import CryptoLib


def Main(test: str) -> bytes:
    return CryptoLib.ripemd160(test)
