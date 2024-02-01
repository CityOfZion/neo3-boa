from __future__ import annotations

import ast
from typing import Any, Optional, Union

from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType


class Variable(IExpression):
    """
    A class used to represent a variable

    :ivar var_type: the type of the variable.
    """

    def __init__(self, var_type: Optional[IType], origin_node: Optional[ast.AST] = None):
        super().__init__(origin_node)
        self.defined_by_entry = True

        from boa3.internal.analyser.model.optimizer import Undefined, UndefinedType
        if var_type is None:
            var_type = Undefined

        self._var_type: Union[IType, UndefinedType] = var_type

        self.is_reassigned = False
        self._origin_variable: Optional[Variable] = None
        self._first_assign_value: Any = Undefined

    def copy(self) -> Variable:
        var = Variable(self._var_type, self._origin_node)
        var.is_reassigned = self.is_reassigned
        var._first_assign_value = self._first_assign_value
        var._origin_variable = self._origin_variable if self._origin_variable is not None else self
        return var

    @property
    def shadowing_name(self) -> str:
        return 'variable'

    @property
    def type(self) -> IType:
        return self._var_type

    @property
    def is_global(self) -> bool:
        return hasattr(self, '_set_as_global') and self._set_as_global

    @property
    def has_literal_value(self) -> bool:
        from boa3.internal.analyser.model.optimizer import Undefined
        return self._first_assign_value is not Undefined

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

    def set_initial_assign(self, first_value: Any):
        if not self.has_literal_value:
            self._first_assign_value = first_value
