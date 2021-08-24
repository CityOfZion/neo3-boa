from boa3.builtin.interop.crypto import verify_with_ecdsa, NamedCurve


def Main():
    verify_with_ecdsa('unit test', 10, b'signature', NamedCurve.SECP256K1)
