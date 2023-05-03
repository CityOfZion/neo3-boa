from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import NamedCurve, verify_with_ecdsa
from boa3.builtin.type import ByteString, ECPoint


@public
def Main(message: ByteString, pubkey: ECPoint, signature: ByteString, curve: NamedCurve) -> bool:
    return verify_with_ecdsa(message, pubkey, signature, curve)
