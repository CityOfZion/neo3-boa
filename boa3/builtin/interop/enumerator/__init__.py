from __future__ import annotations

from typing import Sequence, Union


class Enumerator:
    def __init__(self, entry: Union[Sequence, int]):
        pass

    def concat(self, other: Enumerator) -> Enumerator:
        pass
