from boa3.builtin import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib
from boa3.builtin.type import ECPoint


@public
def Main():
    CryptoLib.verify_with_ecdsa_secp256r1(False, ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'), b'signature')
