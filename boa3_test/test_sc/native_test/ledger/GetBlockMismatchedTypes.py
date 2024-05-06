from boa3.builtin.interop.blockchain import Block
from boa3.builtin.nativecontract.ledger import Ledger


def Main(index: str) -> Block | None:
    return Ledger.get_block(index)
