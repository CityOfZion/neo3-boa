from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import IBls12381
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def main(g: IBls12381, mul: bytes) -> IBls12381:
    return CryptoLib.bls12_381_mul(g, mul, True)
