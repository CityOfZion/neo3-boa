from boa3.sc.contracts import LedgerContract
from boa3.sc.types import Block


def Main(index: str) -> Block | None:
    return LedgerContract.get_block(index)
