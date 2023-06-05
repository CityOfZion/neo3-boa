from boa3.builtin.interop.crypto import NamedCurve
from boa3.builtin.nativecontract.cryptolib import CryptoLib
from boa3.builtin.type import ECPoint


def Main():
    CryptoLib.verify_with_ecdsa('unit test', ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'), b'signature', NamedCurve.SECP256R1)
