from boa3.sc.contracts import StdLib


def Main(key: int) -> bytes:
    return StdLib.base58_decode(key)
