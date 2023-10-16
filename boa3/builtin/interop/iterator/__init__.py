from __future__ import annotations

__all__ = [
    'Iterator',
]


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

        >>> from boa3.builtin.interop import storage
        ... iterator = storage.find(b'prefix')
        ... iterator.next()
        True

        :return: true if it advanced, false if there isn't a next element
        :rtype: bool
        """
        pass

    def __next__(self):
        if self.next():
            return self.value
        raise StopIteration

    def __iter__(self):
        return self
