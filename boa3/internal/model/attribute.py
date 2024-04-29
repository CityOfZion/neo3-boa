import ast

from boa3.internal.model.expression import IExpression
from boa3.internal.model.imports.package import Package
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.type.itype import IType


class Attribute(IExpression):
    """
    A class used to represent an attribute

    :ivar value: the origin expression that has the attribute
    :ivar attr_name: the name of the attribute
    :ivar attr_symbol: the found symbol for the attribute
    """

    def __init__(self,
                 value: ast.AST | IExpression | Package,
                 attr_name: str,
                 attr_symbol: ISymbol | None = None,
                 origin: ast.AST | None = None,
                 deprecated: bool = False
                 ):
        super().__init__(origin, deprecated)

        self.value: ast.AST | IExpression | Package = value
        self.attr_name: str = attr_name

        obj_with_symbols = value.type if isinstance(value, IExpression) else value
        if (isinstance(value, (IExpression, ClassType, Package))
                and hasattr(obj_with_symbols, 'symbols') and attr_name in obj_with_symbols.symbols):
            attr_symbol = obj_with_symbols.symbols[attr_name]

        self.attr_symbol: ISymbol | None = attr_symbol

    @property
    def shadowing_name(self) -> str:
        return 'attribute'

    @property
    def type(self) -> IType:
        from boa3.internal.model.type.type import Type
        return self.attr_symbol.type if isinstance(self.attr_symbol, IExpression) else Type.none

    @property
    def values(self) -> tuple[ast.AST | IExpression, ISymbol | None, str]:
        return self.value, self.attr_symbol, self.attr_name
