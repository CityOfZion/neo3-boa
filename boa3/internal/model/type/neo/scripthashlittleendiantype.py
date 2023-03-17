from typing import Any

from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
from boa3.internal.model.type.itype import IType


class ScriptHashLittleEndianType(UInt160Type):
    """
    A class used to indicate that a parameter or return on the manifest is a ScripthashLittleEndian.
    It's a subclass of UInt160Type.
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'ScriptHashLittleEndian'

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _ScriptHashLittleEndian


_ScriptHashLittleEndian = ScriptHashLittleEndianType()
