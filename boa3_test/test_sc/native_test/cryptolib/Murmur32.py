from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib


@public
def main(data: bytes, seed: int) -> bytes:
    return CryptoLib.murmur32(data, seed)
