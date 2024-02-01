from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def main() -> bool:
    return CryptoLib.bls12_381_equal(10, 'unit test')
