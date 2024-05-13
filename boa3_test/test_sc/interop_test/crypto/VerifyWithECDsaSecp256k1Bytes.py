from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib
from boa3.sc.types import ECPoint, NamedCurve


@public
def Main():
    CryptoLib.verify_with_ecdsa(b'unit test', ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'), b'signature', NamedCurve.SECP256K1)
