from boa3.builtin.interop.crypto import verify_with_ecdsa_secp256k1


def Main():
    verify_with_ecdsa_secp256k1(10, b'publickey', b'signature')
