from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt256


@public
def main() -> UInt256:
    return LedgerContract.get_current_hash()
