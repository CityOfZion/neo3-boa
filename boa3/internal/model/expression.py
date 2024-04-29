import ast
from abc import abstractmethod

from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType


class IExpression(ISymbol):
    """
    An interface used to represent expressions
    """

    def __init__(self, origin_node: ast.AST | None = None, deprecated: bool = False):
        self._origin_node = origin_node
        self._deprecated = deprecated

    @property
    @abstractmethod
    def type(self) -> IType:
        """
        Gets the type of the evaluated expression

        :return: the resulting type when the expression is evaluated
        """
        pass

    @property
    def is_deprecated(self) -> bool:
        return self._deprecated

    def deprecate(self, new_location: str = None):
        self._deprecated = True

    @property
    def origin(self) -> ast.AST:
        """
        Returns the method origin ast node.

        :return: the ast node that describes this method. None if it is not from a ast.
        """
        return self._origin_node
