from boa3.sc.contracts import CryptoLib
from boa3.sc.types import NamedCurveHash


def Main():
    CryptoLib.verify_with_ecdsa('unit test', 10, b'signature', NamedCurveHash.SECP256R1SHA256)
