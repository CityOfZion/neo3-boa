from abc import ABC, abstractmethod
from typing import Self


class ISymbol(ABC):
    defined_by_entry: bool = False

    @property
    @abstractmethod
    def shadowing_name(self) -> str:
        """
        Gets the type of the evaluated expression

        :return: the resulting type when the expression is evaluated
        """
        pass

    @property
    @abstractmethod
    def is_deprecated(self) -> bool:
        """
        Whether the symbol is deprecated.
        """
        return False

    @abstractmethod
    def deprecate(self, new_location: str = None):
        """
        Deprecate this symbol
        """
        pass

    def clone(self) -> Self:
        obj = object.__new__(type(self))
        for key, value in self.__dict__.items():
            obj.__dict__[key] = value
        return obj
