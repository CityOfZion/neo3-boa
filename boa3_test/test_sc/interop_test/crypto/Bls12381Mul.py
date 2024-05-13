from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib
from boa3.sc.types import IBls12381


@public
def main(g: IBls12381, mul: bytes) -> IBls12381:
    return CryptoLib.bls12_381_mul(g, mul, True)
