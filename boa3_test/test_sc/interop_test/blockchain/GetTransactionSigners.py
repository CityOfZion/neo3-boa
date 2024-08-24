from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt256


@public
def main(hash_: UInt256) -> list:
    return LedgerContract.get_transaction_signers(hash_)
