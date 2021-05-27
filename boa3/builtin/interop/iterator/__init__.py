from __future__ import annotations

from typing import Any


class Iterator:
    """
    The iterator for smart contracts.
    """

    @property
    def value(self) -> Any:
        """
        Gets the element in the collection at the current position of the iterator.

        :return: the element in the collection at the current position of the iterator
        :rtype: Any
        """
        return None

    def next(self) -> bool:
        """
        Advances the iterator to the next element of the collection.

        :return: true if it advanced, false if there isn't a next element
        :rtype: bool
        """
        pass
