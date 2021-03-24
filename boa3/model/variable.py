from __future__ import annotations

import ast
from typing import Optional

from boa3.model.expression import IExpression
from boa3.model.type.itype import IType


class Variable(IExpression):
    """
    A class used to represent a variable

    :ivar var_type: the type of the variable.
    """

    def __init__(self, var_type: Optional[IType], origin_node: Optional[ast.AST] = None):
        super().__init__(origin_node)
        self._var_type: Optional[IType] = var_type

    def copy(self) -> Variable:
        return Variable(self._var_type, self._origin_node)

    @property
    def shadowing_name(self) -> str:
        return 'variable'

    @property
    def type(self) -> IType:
        return self._var_type

    def __repr__(self) -> str:
        return '{0}({1})'.format(self.__class__.__name__, self.__str__())

    def __str__(self) -> str:
        return str(self.type)

    def set_type(self, var_type: IType):
        """
        Sets a type for the variable

        :param var_type:
        """
        self._var_type = var_type
