from abc import ABC, abstractmethod


class IExpression(ABC):
    """
    An interface used to represent expressions
    """

    @property
    @abstractmethod
    def type(self) -> type:
        """
        Gets the type of the evaluated expression

        :return: the resulting type when the expression is evaluated
        """
        pass
