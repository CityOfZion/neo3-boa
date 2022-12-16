from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(key: bytes) -> str:
    return StdLib.base58_check_encode(key)
