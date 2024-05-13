from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import Block


@public
def Main(index: str) -> Block:
    return LedgerContract.get_block(index)
