from boa3.builtin import public
from boa3.builtin.interop.binary import base58_check_encode


@public
def main(key: bytes) -> str:
    return base58_check_encode(key)
