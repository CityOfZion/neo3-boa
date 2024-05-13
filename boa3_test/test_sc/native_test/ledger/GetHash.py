from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return LedgerContract.hash
