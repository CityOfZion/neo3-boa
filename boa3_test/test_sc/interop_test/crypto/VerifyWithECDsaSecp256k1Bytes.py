from boa3.builtin import public
from boa3.builtin.interop.crypto import verify_with_ecdsa_secp256k1


@public
def Main():
    verify_with_ecdsa_secp256k1(b'unit test', b'publickey', b'signature')
