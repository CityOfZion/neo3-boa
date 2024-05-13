from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib


@public
def main() -> bytes:
    return CryptoLib.bls12_381_serialize('unit test')
