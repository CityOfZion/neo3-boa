from boa3.builtin.nativecontract.cryptolib import CryptoLib


def Main():
    CryptoLib.verify_with_ecdsa_secp256k1('unit test', 10, b'signature')
