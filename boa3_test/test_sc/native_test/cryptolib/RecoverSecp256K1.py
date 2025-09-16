from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib


@public
def main(message_hash: bytes, signature: bytes) -> bytes | None:
    return CryptoLib.recover_secp256k1(message_hash, signature)
