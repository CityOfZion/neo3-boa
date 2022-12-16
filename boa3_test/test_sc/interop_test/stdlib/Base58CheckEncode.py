from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import base58_check_encode


@public
def main(key: bytes) -> str:
    return base58_check_encode(key)
