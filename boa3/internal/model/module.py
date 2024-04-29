from boa3.internal.model.callable import Callable
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.variable import Variable


class Module(ISymbol):
    """
    A class used to represent a Python module

    :ivar variables: a dictionary that maps each variable with its name. Empty by default.
    :ivar methods: a dictionary that maps each method with its name. Empty by default.
    :ivar callables: a dictionary that maps each callable object with its name. Empty by default.
    :ivar classes: a dictionary that maps each class with its name. Empty by default.
    :ivar imported_symbols: a dictionary that maps each imported symbol with its name. Empty by default.
    """

    def __init__(self,
                 variables: dict[str, Variable] = None,
                 methods: dict[str, Method] = None,
                 deprecated: bool = False
                 ):
        if variables is None:
            variables = {}
        self.variables = variables

        if methods is None:
            methods = {}
        self.methods = methods
        self.callables: dict[str, Callable] = {}
        self.classes: dict[str, ClassType] = {}

        self.defined_by_entry = True
        self._deprecated = deprecated
        self.imported_symbols = {}
        self.assigned_variables = []

    @property
    def shadowing_name(self) -> str:
        return 'module'

    @property
    def is_deprecated(self) -> bool:
        return self._deprecated

    def deprecate(self, new_location: str = None):
        self._deprecated = True

    def include_variable(self, var_id: str, var: Variable):
        """
        Includes a variable into the scope of the module

        :param var_id: variable identifier
        :param var: variable to be included
        """
        if var_id not in self.symbols:
            self.variables[var_id] = var

    def is_variable_assigned(self, var_id: str) -> bool:
        if var_id not in self.variables:
            return False

        if var_id in self.assigned_variables or var_id in self.imported_symbols:
            return True

        for imported in self.imported_symbols.values():
            from boa3.internal.model.imports.importsymbol import Import
            if isinstance(imported, Import) and self.variables[var_id] in imported.variables.values():
                return True

        return False

    def assign_variable(self, var_id: str):
        if var_id in self.variables:
            self.assigned_variables.append(var_id)

    def include_callable(self, method_id: str, method: Callable) -> bool:
        """
        Includes a method into the scope of the module

        :param method_id: method identifier
        :param method: method to be included
        """
        if method_id not in self.symbols:
            if isinstance(method, Method):
                self.methods[method_id] = method
            else:
                self.callables[method_id] = method

            return True

        return False

    def include_class(self, class_id: str, class_obj: ClassType):
        """
        Includes a class into the scope of the module

        :param class_id: class identifier
        :param class_obj: class object to be included
        """
        if class_id not in self.symbols:
            self.classes[class_id] = class_obj

    def include_symbol(self, symbol_id: str, symbol: ISymbol):
        """
        Includes a method into the scope of the module

        :param symbol_id: method identifier
        :param symbol: method to be included
        """
        if symbol_id not in self.symbols:
            if isinstance(symbol, Variable):
                self.include_variable(symbol_id, symbol)
            elif isinstance(symbol, Callable):
                self.include_callable(symbol_id, symbol)
            elif isinstance(symbol, ClassType):
                self.include_class(symbol_id, symbol)
            else:
                self.imported_symbols[symbol_id] = symbol

    @property
    def symbols(self) -> dict[str, ISymbol]:
        """
        Gets all the symbols in the module

        :return: a dictionary that maps each symbol in the module with its name
        """
        symbols = {}
        symbols.update(self.imported_symbols)
        symbols.update(self.variables)
        symbols.update(self.methods)
        symbols.update(self.callables)
        symbols.update(self.classes)
        return symbols
