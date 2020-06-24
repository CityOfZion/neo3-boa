from __future__ import annotations
import abc
from enum import IntEnum
from events import Events  # type: ignore

msgrouter = Events()

# :noindex:


class Size(IntEnum):
    """
    Explicit bytes of memory consumed
    """
    uint8 = 1
    uint16 = 2
    uint32 = 4
    uint64 = 8
    uint160 = 20
    uint256 = 32


class IClonable(abc.ABC):
    @abc.abstractmethod
    def clone(self):
        """
        Create a deep copy of self
        """

    def from_replica(self, replica):
        pass


class IJson(abc.ABC):
    @abc.abstractmethod
    def to_json(self) -> dict:
        pass

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json: dict):
        pass
