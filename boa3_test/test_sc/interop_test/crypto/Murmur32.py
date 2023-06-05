from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def main(data: bytes, seed: int) -> bytes:
    return CryptoLib.murmur32(data, seed)
