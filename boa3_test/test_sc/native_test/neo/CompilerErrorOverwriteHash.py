from boa3.sc.contracts import NeoToken
from boa3.sc.types import UInt160


def main() -> UInt160:
    NeoToken.hash = UInt160()
    return NeoToken.hash
