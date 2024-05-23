from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib


@public
def main(data: bytes) -> bytes:
    return CryptoLib.keccak256(data)
