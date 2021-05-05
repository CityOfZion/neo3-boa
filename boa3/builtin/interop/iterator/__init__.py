from __future__ import annotations

from typing import Any


class Iterator:

    @property
    def value(self) -> Any:
        return None

    def next(self) -> bool:
        pass
