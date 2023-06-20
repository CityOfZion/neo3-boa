from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import NamedCurve, verify_with_ecdsa
from boa3.builtin.type import ECPoint


@public
def Main(message: bytes, pubkey: ECPoint, signature: bytes, curve: NamedCurve) -> bool:
    return verify_with_ecdsa(message, pubkey, signature, curve)
