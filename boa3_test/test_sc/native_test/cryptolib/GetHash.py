from boa3.builtin import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib
from boa3.builtin.type import UInt160


@public
def main() -> UInt160:
    return CryptoLib.hash
