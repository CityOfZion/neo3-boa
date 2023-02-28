import ast
from typing import Dict

from boa3.internal.analyser.importanalyser import ImportAnalyser
from boa3.internal.model.builtin.builtincallable import IBuiltinCallable
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class Import(ISymbol):
    """
    A class used to represent an imported package

    :ivar variables: a dictionary that maps each variable with its name. Empty by default.
    :ivar methods: a dictionary that maps each method with its name. Empty by default.
    :ivar types: a dictionary that maps each type with its name. Empty by default.
    """

    def __init__(self, origin: str, syntax_tree: ast.AST, import_analyser: ImportAnalyser,
                 imported_symbols: Dict[str, ISymbol] = None):
        if imported_symbols is None:
            symbols = import_analyser.symbols
        else:
            symbols = import_analyser.export_symbols(list(imported_symbols.keys()))

        self.variables = {var_id: var for var_id, var in symbols.items() if isinstance(var, Variable)}
        self.methods = {fun_id: fun for fun_id, fun in symbols.items() if isinstance(fun, Method)}
        self.types = {type_id: tpe for type_id, tpe in symbols.items() if isinstance(tpe, IType)}
        self.imports = {alias: imprt for alias, imprt in symbols.items() if isinstance(imprt, Import)}
        self._other_symbols = {alias: symbol for alias, symbol in symbols.items()
                               if not isinstance(symbol, (Variable, Method, IType, Import))}

        self._symbols_not_imported = {alias: symbol for alias, symbol in import_analyser.symbols.items()
                                      if alias not in symbols}

        for method in self.methods.values():
            if not isinstance(method, IBuiltinCallable) and hasattr(method, 'defined_by_entry'):
                # methods imported are treated as methods defined in the entry file
                method.defined_by_entry = True

        self.analyser = import_analyser.analyser
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

    @property
    def all_symbols(self) -> Dict[str, ISymbol]:
        symbol = self.symbols.copy()
        symbol.update(self._symbols_not_imported)
        return symbol


class BuiltinImport(Import):
    """
    A class used to differentiate built-in importings
    """
    pass
