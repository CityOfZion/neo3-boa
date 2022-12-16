from typing import Any, Union

from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Block, get_block
from boa3.builtin.type import UInt256


@public
def is_block(value: Any) -> bool:
    return isinstance(value, Block)


@public
def get_block_is_block(index_or_hash: Union[int, UInt256]) -> bool:
    block = get_block(index_or_hash)
    return is_block(block)
