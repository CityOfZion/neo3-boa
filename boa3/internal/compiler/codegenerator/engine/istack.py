import abc
from typing import TypeVar, Self

T = TypeVar("T")


class IStack(abc.ABC):
    def __init__(self, stack_type: type[T]):
        self._stack_type = stack_type
        self._stack: list[T] = []

    @abc.abstractmethod
    def _default_constructor_args(self) -> tuple:
        return (self._stack_type,)

    def append(self, value: T):
        return self._stack.append(value)

    def clear(self):
        return self._stack.clear()

    def copy(self) -> Self:
        new_stack = self.__class__(*self._default_constructor_args())
        new_stack._stack = self._stack.copy()
        return new_stack

    def pop(self, index: int) -> T:
        return self._stack.pop(index)

    def __len__(self) -> int:
        return len(self._stack)

    def __getitem__(self, index_or_slice: int | slice):
        return self._stack[index_or_slice]

    def reverse(self, start: int = 0, end: int = None, *, rotate: bool = False):
        if end is None:
            end = len(self._stack)

        if rotate:
            reverse = self._stack[start:end]
            reverse.append(reverse.pop(0))
        else:
            reverse = list(reversed(self._stack[start:end]))
        self._stack[start:end] = reverse
