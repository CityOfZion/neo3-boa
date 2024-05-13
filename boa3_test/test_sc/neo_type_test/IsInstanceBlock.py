from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt256, Block


@public
def is_block(value: Any) -> bool:
    return isinstance(value, Block)


@public
def get_block_is_block(index_or_hash: int | UInt256) -> bool:
    block = LedgerContract.get_block(index_or_hash)
    return is_block(block)
