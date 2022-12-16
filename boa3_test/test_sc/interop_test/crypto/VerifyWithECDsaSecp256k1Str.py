from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import NamedCurve, verify_with_ecdsa
from boa3.builtin.type import ECPoint


@public
def Main():
    verify_with_ecdsa('unit test', ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'), b'signature', NamedCurve.SECP256K1)
