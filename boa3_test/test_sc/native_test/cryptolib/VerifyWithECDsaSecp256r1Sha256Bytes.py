from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib
from boa3.sc.types import ECPoint, NamedCurveHash


@public
def Main():
    CryptoLib.verify_with_ecdsa(b'unit test', ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'), b'signature', NamedCurveHash.SECP256R1SHA256)
