from boa3.builtin import public
from boa3.builtin.interop.crypto import verify_with_ecdsa, NamedCurve
from boa3.builtin.type import ECPoint


@public
def Main():
    verify_with_ecdsa(False, ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'), b'signature', NamedCurve.SECP256R1)
