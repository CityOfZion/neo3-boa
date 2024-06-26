from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Block
from boa3.builtin.nativecontract.ledger import Ledger


@public
def Main(index: int) -> Block | None:
    return Ledger.get_block(index)
