import ast
from typing import Dict

from boa3.model.method import Method
from boa3.model.symbol import ISymbol
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class Import(ISymbol):
    """
    A class used to represent an imported package

    :ivar variables: a dictionary that maps each variable with its name. Empty by default.
    :ivar methods: a dictionary that maps each method with its name. Empty by default.
    :ivar types: a dictionary that maps each type with its name. Empty by default.
    """

    def __init__(self, origin: str, syntax_tree: ast.AST, symbols: Dict[str, ISymbol] = None):
        if symbols is None:
            symbols = {}

        self.variables = {var_id: var for var_id, var in symbols.items() if isinstance(var, Variable)}
        self.methods = {fun_id: fun for fun_id, fun in symbols.items() if isinstance(fun, Method)}
        self.types = {type_id: tpe for type_id, tpe in symbols.items() if isinstance(tpe, IType)}
        self.imports = {alias: imprt for alias, imprt in symbols.items() if isinstance(imprt, Import)}
        self._other_symbols = {alias: symbol for alias, symbol in symbols.items()
                               if not isinstance(symbol, (Variable, Method, IType, Import))}

        self.origin: str = origin
        self.ast: ast.AST = syntax_tree

    @property
    def shadowing_name(self) -> str:
        return 'module'

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        symbol = {}
        symbol.update(self.variables)
        symbol.update(self.methods)
        symbol.update(self.types)
        symbol.update(self._other_symbols)
        symbol.update(self.imports)
        return symbol
