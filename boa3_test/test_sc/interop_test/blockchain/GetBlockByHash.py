from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt256, Block


@public
def Main(block_hash: UInt256) -> Block | None:
    return LedgerContract.get_block(block_hash)
