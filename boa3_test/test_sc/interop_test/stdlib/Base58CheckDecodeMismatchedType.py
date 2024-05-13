from boa3.sc.contracts import StdLib


def main(key: int) -> bytes:
    return StdLib.base58_check_decode(key)
