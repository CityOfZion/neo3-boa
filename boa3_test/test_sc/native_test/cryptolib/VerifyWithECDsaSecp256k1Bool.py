from boa3.sc.contracts import CryptoLib
from boa3.sc.types import ECPoint, NamedCurve


def Main():
    CryptoLib.verify_with_ecdsa(False, ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'), b'signature', NamedCurve.SECP256K1)
