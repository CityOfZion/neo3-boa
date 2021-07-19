from boa3.builtin.interop.stdlib import base58_check_decode


def main(key: int) -> bytes:
    return base58_check_decode(key)
