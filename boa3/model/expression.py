from abc import abstractmethod

from boa3.model.symbol import ISymbol
from boa3.model.type.itype import IType


class IExpression(ISymbol):
    """
    An interface used to represent expressions
    """

    @property
    @abstractmethod
    def type(self) -> IType:
        """
        Gets the type of the evaluated expression

        :return: the resulting type when the expression is evaluated
        """
        pass
