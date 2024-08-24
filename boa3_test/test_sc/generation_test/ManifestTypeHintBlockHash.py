from boa3.sc.compiletime import public
from boa3.sc.types import UInt256, BlockHash


@public
def main() -> BlockHash:
    return BlockHash(UInt256())
