from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Block, get_block
from boa3.builtin.type import UInt256


@public
def Main(block_hash: UInt256) -> Block | None:
    return get_block(block_hash)
