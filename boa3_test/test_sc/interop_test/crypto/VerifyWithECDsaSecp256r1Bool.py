from boa3.builtin import public
from boa3.builtin.interop.crypto import NamedCurve, verify_with_ecdsa
from boa3.builtin.type import ECPoint


@public
def Main():
    verify_with_ecdsa(False, ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'), b'signature', NamedCurve.SECP256R1)
