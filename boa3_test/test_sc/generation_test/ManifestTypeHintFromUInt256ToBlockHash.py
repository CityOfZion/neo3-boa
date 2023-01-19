from boa3.builtin.compile_time import public
from boa3.builtin.type import BlockHash, UInt256


@public
def Main() -> BlockHash:
    return UInt256()
