import ast
from abc import abstractmethod
from typing import Optional

from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType


class IExpression(ISymbol):
    """
    An interface used to represent expressions
    """

    def __init__(self, origin_node: Optional[ast.AST] = None):
        self._origin_node = origin_node

    @property
    @abstractmethod
    def type(self) -> IType:
        """
        Gets the type of the evaluated expression

        :return: the resulting type when the expression is evaluated
        """
        pass

    @property
    def origin(self) -> ast.AST:
        """
        Returns the method origin ast node.

        :return: the ast node that describes this method. None if it is not from a ast.
        """
        return self._origin_node
