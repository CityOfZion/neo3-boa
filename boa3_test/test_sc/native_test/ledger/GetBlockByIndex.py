from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import Block


@public
def Main(index: int) -> Block | None:
    return LedgerContract.get_block(index)
