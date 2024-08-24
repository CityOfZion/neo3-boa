from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt256, Transaction


@public
def main(hash_: UInt256) -> Transaction | None:
    return LedgerContract.get_transaction(hash_)
