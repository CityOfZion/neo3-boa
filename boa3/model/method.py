import ast
from typing import Dict, List, Optional

from boa3.model.callable import Callable
from boa3.model.debuginstruction import DebugInstruction
from boa3.model.symbol import ISymbol
from boa3.model.type.type import IType, Type
from boa3.model.variable import Variable


class Method(Callable):
    """
    A class used to represent a function or a class method

    :ivar args: a dictionary that maps each arg with its name. Empty by default.
    :ivar locals: a dictionary that maps each local variable with its name. Empty by default.
    :ivar imported_symbols: a dictionary that maps each imported symbol with its name. Empty by default.
    :ivar is_public: a boolean value that specifies if the method is public. False by default.
    :ivar return_type: the return type of the method. None by default.
    """

    def __init__(self, args: Dict[str, Variable] = None, defaults: List[ast.AST] = None,
                 return_type: IType = Type.none, is_public: bool = False, origin_node: Optional[ast.AST] = None):
        super().__init__(args, defaults, return_type, is_public, origin_node)

        self.imported_symbols = {}
        self._symbols = {}
        self.locals: Dict[str, Variable] = {}

        self._debug_map: List[DebugInstruction] = []

    @property
    def shadowing_name(self) -> str:
        return 'method'

    def include_variable(self, var_id: str, var: Variable, is_global: bool = False):
        """
        Includes a variable into the list of locals

        :param var_id: variable identifier
        :param var: variable to be included
        :param is_global: whether the variable is declared outside the method
        """
        if var_id not in self.symbols:
            if is_global:
                self._symbols[var_id] = var
            else:
                self.locals[var_id] = var

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
        symbols = self._symbols.copy()
        symbols.update(self.imported_symbols)
        symbols.update(self.args)
        symbols.update(self.locals)
        return symbols

    def include_symbol(self, symbol_id: str, symbol: ISymbol, is_global: bool = False):
        """
        Includes a method into the scope of the module

        :param symbol_id: method identifier
        :param symbol: method to be included
        :param is_global: whether the variable is declared outside the method
        """
        if symbol_id not in self.symbols:
            if isinstance(symbol, Variable):
                self.include_variable(symbol_id, symbol, is_global)
            else:
                self.imported_symbols[symbol_id] = symbol

    @property
    def origin(self) -> ast.AST:
        """
        Returns the method origin ast node.

        :return: the ast node that describes this method. None if it is not from a ast.
        """
        return self._origin_node

    def debug_map(self) -> List[DebugInstruction]:
        """
        Returns a list with the debug information of each mapped Python instruction inside this method
        """
        from boa3.compiler.codegenerator.vmcodemapping import VMCodeMapping
        return sorted(self._debug_map, key=lambda instr: VMCodeMapping.instance().get_start_address(instr.code))

    def include_instruction(self, instr_info: DebugInstruction):
        """
        Includes a new instruction in the debug info

        :param instr_info: debug information from the new instruction
        """
        if not any((info.start_line == instr_info.start_line and info.start_col == instr_info.start_col
                    for info in self._debug_map)):
            existing_instr_info: Optional[DebugInstruction] =\
                next((info for info in self._debug_map if info.code == instr_info.code), None)
            if existing_instr_info is not None:
                self._debug_map.remove(existing_instr_info)
            self._debug_map.append(instr_info)

    def remove_instruction(self, start_line: int, start_col: int):
        """
        Removes a instruction from the debug info at the given position if it exists

        :param start_line: instruction's first line
        :param start_col: instruction's beginning offset in the first line
        """
        instruction = next((info for info in self._debug_map
                            if info.start_line == start_line and info.start_col == start_col),
                           None)
        if instruction is not None:
            self._debug_map.remove(instruction)

    def args_to_be_generated(self) -> List[int]:
        """
        Gets the indexes of the arguments that must be generated.
        If method has `self` arg, it must be in this list.

        By default, all the arguments are generated.

        :return: A list with the indexes of the arguments that must be generated
        """
        return list(range(len(self.args)))
