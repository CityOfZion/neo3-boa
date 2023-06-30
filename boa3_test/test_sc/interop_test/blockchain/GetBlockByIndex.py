from typing import Optional

from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Block, get_block


@public
def Main(index: int) -> Optional[Block]:
    return get_block(index)
