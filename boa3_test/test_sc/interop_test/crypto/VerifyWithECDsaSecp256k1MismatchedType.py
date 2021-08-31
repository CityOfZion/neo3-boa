from boa3.builtin.interop.crypto import NamedCurve, verify_with_ecdsa


def Main():
    verify_with_ecdsa('unit test', 10, b'signature', NamedCurve.SECP256K1)
