from boa3.sc.contracts import CryptoLib
from boa3.sc.types import UInt160


def main() -> UInt160:
    CryptoLib.hash = UInt160()
    return CryptoLib.hash
