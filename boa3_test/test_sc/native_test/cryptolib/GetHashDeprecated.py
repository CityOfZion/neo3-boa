from boa3.sc.compiletime import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return CryptoLib.hash
