from boa3.sc.contracts import StdLib


def Main(key: int) -> str:
    return StdLib.base58_encode(key)
