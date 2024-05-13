from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib
from boa3.sc.types import IBls12381


@public
def main(g: IBls12381) -> bytes:
    return CryptoLib.bls12_381_serialize(g)
