from boa3.builtin.interop.stdlib import base58_check_encode


def main(key: int) -> str:
    return base58_check_encode(key)
