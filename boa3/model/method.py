import ast
from typing import Dict, List, Optional

from boa3.model.expression import IExpression
from boa3.model.symbol import ISymbol
from boa3.model.type.type import IType, Type
from boa3.model.variable import Variable


class Method(IExpression):
    """
    A class used to represent a function or a class method

    :ivar args: a dictionary that maps each arg with its name. Empty by default.
    :ivar locals: a dictionary that maps each local variable with its name. Empty by default.
    :ivar imported_symbols: a dictionary that maps each imported symbol with its name. Empty by default.
    :ivar is_public: a boolean value that specifies if the method is public. False by default.
    :ivar return_type: the return type of the method. None by default.
    """

    def __init__(self, args: Dict[str, Variable] = None, return_type: IType = Type.none,
                 is_public: bool = False, origin_node: Optional[ast.AST] = None):
        from boa3.neo.vm.VMCode import VMCode
        if args is None:
            args = {}
        self.args: Dict[str, Variable] = args
        self.return_type: IType = return_type

        self.imported_symbols = {}

        self._origin_node = origin_node
        self.is_public: bool = is_public
        self._requires_storage: bool = False

        self.locals: Dict[str, Variable] = {}
        self.init_bytecode: Optional[VMCode] = None
        self.init_address: Optional[int] = None

    @property
    def shadowing_name(self) -> str:
        return 'method'

    def include_variable(self, var_id: str, var: Variable):
        """
        Includes a variable into the list of locals

        :param var_id: variable identifier
        :param var: variable to be included
        """
        if var_id not in self.symbols:
            self.locals[var_id] = var

    @property
    def type(self) -> IType:
        return self.return_type

    def __str__(self) -> str:
        args_types: List[str] = [str(arg.type) for arg in self.args.values()]
        if self.return_type is not Type.none:
            signature = '({0}) -> {1}'.format(', '.join(args_types), self.return_type)
        else:
            signature = '({0})'.format(', '.join(args_types))
        public = 'public ' if self.is_public else ''
        return '{0}{1}'.format(public, signature)

    @property
    def symbols(self) -> Dict[str, Variable]:
        """
        Gets all the symbols in the method

        :return: a dictionary that maps each symbol in the module with its name
        """
        symbols = {}
        symbols.update(self.imported_symbols)
        symbols.update(self.args)
        symbols.update(self.locals)
        return symbols

    def include_symbol(self, symbol_id: str, symbol: ISymbol):
        """
        Includes a method into the scope of the module

        :param symbol_id: method identifier
        :param symbol: method to be included
        """
        if symbol_id not in self.symbols:
            if isinstance(symbol, Variable):
                self.include_variable(symbol_id, symbol)
            else:
                self.imported_symbols[symbol_id] = symbol

    @property
    def bytecode_address(self) -> Optional[int]:
        """
        Gets the address where this method starts in the bytecode

        :return: the first address of the method
        """
        if self.init_bytecode is None:
            return self.init_address
        else:
            return self.init_bytecode.start_address

    @property
    def requires_storage(self) -> bool:
        """
        This method requires blockchain storage access

        :return: True if the method uses storage features. False otherwise.
        """
        return self._requires_storage

    @property
    def origin(self) -> ast.AST:
        """
        Returns the method origin ast node.

        :return: the ast node that describes this method. None if it is not from a ast.
        """
        return self._origin_node

    def set_storage(self):
        self._requires_storage = True
