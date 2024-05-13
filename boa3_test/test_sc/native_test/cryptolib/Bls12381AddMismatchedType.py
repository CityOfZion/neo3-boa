from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib
from boa3.sc.types import IBls12381


@public
def main() -> IBls12381:
    return CryptoLib.bls12_381_add(10, 'unit test')
