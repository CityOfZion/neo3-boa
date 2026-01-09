from boa3.sc.contracts import GasToken
from boa3.sc.types import UInt160


def main() -> UInt160:
    GasToken.hash = UInt160()
    return GasToken.hash
