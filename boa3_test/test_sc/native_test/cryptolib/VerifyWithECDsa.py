from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib
from boa3.sc.types import ECPoint, NamedCurve


@public
def Main(message: bytes, pubkey: ECPoint, signature: bytes, curve: NamedCurve) -> bool:
    return CryptoLib.verify_with_ecdsa(message, pubkey, signature, curve)
