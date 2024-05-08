import ast

from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.type.itype import IType


class Property(IExpression):
    """
    A class used to represent a variable

    :ivar var_type: the type of the variable.
    """

    def __init__(self,
                 getter: Method,
                 setter: Method = None,
                 origin_node: ast.AST | None = None,
                 deprecated: bool = False
                 ):
        super().__init__(origin_node, deprecated)
        self._getter: Method = getter
        self._setter: Method | None = setter

    @property
    def shadowing_name(self) -> str:
        return 'property'

    @property
    def type(self) -> IType:
        return self._getter.type

    @property
    def getter(self) -> Method:
        return self._getter

    @property
    def setter(self) -> Method | None:
        return self._setter

    def __str__(self) -> str:
        return str(self.type)
