from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib


@public
def main() -> bool:
    return CryptoLib.bls12_381_equal(10, 'unit test')
