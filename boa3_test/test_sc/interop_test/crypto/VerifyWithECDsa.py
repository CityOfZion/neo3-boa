from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib
from boa3.sc.types import ECPoint, NamedCurveHash


@public
def Main(message: bytes, pubkey: ECPoint, signature: bytes, curve: NamedCurveHash) -> bool:
    return CryptoLib.verify_with_ecdsa(message, pubkey, signature, curve)
