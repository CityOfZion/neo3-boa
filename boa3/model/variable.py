from __future__ import annotations

import ast
from typing import Optional, Union

from boa3.model.expression import IExpression
from boa3.model.type.itype import IType


class Variable(IExpression):
    """
    A class used to represent a variable

    :ivar var_type: the type of the variable.
    """

    def __init__(self, var_type: Optional[IType], origin_node: Optional[ast.AST] = None):
        super().__init__(origin_node)
        self.defined_by_entry = True
        if var_type is None:
            from boa3.analyser.model.optimizer import Undefined, UndefinedType
            var_type = Undefined

        self._var_type: Union[IType, UndefinedType] = var_type

        self.is_reassigned = False
        self._origin_variable: Optional[Variable] = None

    def copy(self) -> Variable:
        var = Variable(self._var_type, self._origin_node)
        var.is_reassigned = self.is_reassigned
        var._origin_variable = self._origin_variable if self._origin_variable is not None else self
        return var

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

    def set_is_reassigned(self):
        if not self.is_reassigned:
            self.is_reassigned = True
        if hasattr(self._origin_variable, 'set_is_reassigned'):
            self._origin_variable.set_is_reassigned()
