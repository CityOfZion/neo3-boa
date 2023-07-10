from typing import Optional

from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Block
from boa3.builtin.nativecontract.ledger import Ledger
from boa3.builtin.type import UInt256


@public
def Main(block_hash: UInt256) -> Optional[Block]:
    return Ledger.get_block(block_hash)
