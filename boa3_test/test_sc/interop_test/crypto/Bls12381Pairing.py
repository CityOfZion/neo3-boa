from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib
from boa3.sc.types import IBls12381


@public
def main(g1: IBls12381, g2: IBls12381) -> IBls12381:
    return CryptoLib.bls12_381_pairing(g1, g2)
