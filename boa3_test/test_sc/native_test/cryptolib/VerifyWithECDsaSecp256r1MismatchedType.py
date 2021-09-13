from boa3.builtin.interop.crypto import NamedCurve
from boa3.builtin.nativecontract.cryptolib import CryptoLib


def Main():
    CryptoLib.verify_with_ecdsa('unit test', 10, b'signature', NamedCurve.SECP256R1)
