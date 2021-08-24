from boa3.builtin.nativecontract.cryptolib import CryptoLib
from boa3.builtin.interop.crypto import NamedCurve


def Main():
    CryptoLib.verify_with_ecdsa('unit test', 10, b'signature', NamedCurve.SECP256R1)
