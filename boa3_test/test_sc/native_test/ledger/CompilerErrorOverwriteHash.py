from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt160


def main() -> UInt160:
    LedgerContract.hash = UInt160()
    return LedgerContract.hash
