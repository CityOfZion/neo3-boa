from boa3.builtin import public
from boa3.builtin.interop.crypto import verify_with_ecdsa_secp256r1


@public
def Main():
    verify_with_ecdsa_secp256r1(10, b'publickey', b'signature')
