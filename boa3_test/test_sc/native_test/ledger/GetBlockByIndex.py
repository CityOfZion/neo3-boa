from boa3.builtin import public
from boa3.builtin.interop.blockchain import Block
from boa3.builtin.nativecontract.ledger import Ledger


@public
def Main(index: int) -> Block:
    return Ledger.get_block(index)
