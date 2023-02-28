from typing import Any

from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
from boa3.internal.model.type.itype import IType


class BlockHashType(UInt256Type):
    """
    A class used to indicate that a parameter or return on the manifest is a BlockHash. It's a subclass of UInt256Type.
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'BlockHash'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _BlockHash


_BlockHash = BlockHashType()
