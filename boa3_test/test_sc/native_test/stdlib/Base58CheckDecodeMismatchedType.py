from boa3.builtin.nativecontract.stdlib import StdLib


def main(key: int) -> bytes:
    return StdLib.base58_check_decode(key)
