from boa3.builtin.nativecontract.stdlib import StdLib


def Main(key: int) -> bytes:
    return StdLib.base64_encode(key)
