from typing import Any

from boa3.internal.neo.vm.type import StackItem
from boa3.internal.neo.vm.type.StackItem import StackItemType


class NativeAccountState:
    def __init__(self, balance: int):
        self.balance: int = balance if balance > 0 else 0
        self._balance_height: int = 0
        self._vote_to: Any = None

    def serialize(self) -> bytes:
        return (StackItemType.Struct
                + b'\x03'
                + StackItem.serialize(self.balance)
                + b'!\x00\x00'
                )
