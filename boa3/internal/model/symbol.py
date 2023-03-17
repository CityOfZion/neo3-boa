from abc import ABC, abstractmethod


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
