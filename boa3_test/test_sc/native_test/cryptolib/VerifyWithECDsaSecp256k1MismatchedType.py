from boa3.sc.contracts import CryptoLib
from boa3.sc.types import NamedCurve


def Main():
    CryptoLib.verify_with_ecdsa('unit test', 10, b'signature', NamedCurve.SECP256K1)
