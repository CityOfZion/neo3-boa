import enum

from boa3.internal.model.callable import Callable
from boa3.internal.model.event import Event


class ManifestSymbol(int, enum.Enum):
    Method = enum.auto()
    Event = enum.auto()

    @classmethod
    def get_manifest_symbol(cls, callable_: Callable):
        if isinstance(callable_, Event):
            return cls.Event
        return cls.Method

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
