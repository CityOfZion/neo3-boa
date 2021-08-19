from boa3.builtin.nativecontract.stdlib import StdLib


def main(key: int) -> str:
    return StdLib.base58_check_encode(key)
