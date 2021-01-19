from __future__ import annotations

from typing import Any, Collection


class Iterator:
    def __init__(self, entry: Collection):
        pass

    @property
    def value(self) -> Any:
        return None

    def next(self) -> bool:
        pass
