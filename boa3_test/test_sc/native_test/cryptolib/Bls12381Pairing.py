from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import IBls12381
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def main(g1: IBls12381, g2: IBls12381) -> IBls12381:
    return CryptoLib.bls12_381_pairing(g1, g2)
