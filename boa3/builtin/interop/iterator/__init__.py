from typing import Any, Collection


class Iterator:
    def __init__(self, entry: Collection):
        pass

    @property
    def key(self) -> Any:
        return None

    @property
    def value(self) -> Any:
        return None

    def next(self) -> bool:
        pass
