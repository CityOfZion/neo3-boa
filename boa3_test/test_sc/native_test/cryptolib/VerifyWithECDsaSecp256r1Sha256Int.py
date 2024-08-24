from boa3.sc.contracts import CryptoLib
from boa3.sc.types import ECPoint, NamedCurveHash


def Main():
    CryptoLib.verify_with_ecdsa(10, ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'), b'signature', NamedCurveHash.SECP256R1SHA256)
