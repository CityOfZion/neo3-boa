from boa3.sc.contracts import StdLib


def main(key: int) -> str:
    return StdLib.base58_check_encode(key)
