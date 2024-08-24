from boa3.sc.compiletime import public
from boa3.sc.types import UInt256, BlockHash


@public
def Main() -> BlockHash:
    return UInt256()
