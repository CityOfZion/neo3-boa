from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Block, get_block


@public
def Main(index: str) -> Block:
    return get_block(index)
