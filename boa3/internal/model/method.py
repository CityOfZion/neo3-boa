import ast

from boa3.internal.model.callable import Callable
from boa3.internal.model.debuginstruction import DebugInstruction
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.type.type import IType, Type
from boa3.internal.model.variable import Variable


class Method(Callable):
    """
    A class used to represent a function or a class method

    :ivar args: a dictionary that maps each arg with its name. Empty by default.
    :ivar locals: a dictionary that maps each local variable with its name. Empty by default.
    :ivar imported_symbols: a dictionary that maps each imported symbol with its name. Empty by default.
    :ivar is_public: a boolean value that specifies if the method is public. False by default.
    :ivar return_type: the return type of the method. None by default.
    """

    def __init__(self,
                 args: dict[str, Variable] = None,
                 vararg: tuple[str, Variable] | None = None,
                 kwargs: dict[str, Variable] | None = None,
                 defaults: list[ast.AST] = None,
                 return_type: IType = Type.none, is_public: bool = False,
                 decorators: list[Callable] = None,
                 is_init: bool = False,
                 external_name: str = None,
                 is_safe: bool = False,
                 origin_node: ast.AST | None = None,
                 deprecated: bool = False
                 ):
        super().__init__(
            args=args,
            vararg=vararg,
            kwargs=kwargs,
            defaults=defaults,
            return_type=return_type,
            is_public=is_public,
            decorators=decorators,
            external_name=external_name,
            is_safe=is_safe,
            origin_node=origin_node,
            deprecated=deprecated
        )

        self.imported_symbols = {}
        self._symbols = {}
        self.defined_by_entry = True
        self.is_init = is_init
        self.locals: dict[str, Variable] = {}

        if is_init and self.has_cls_or_self:
            self.return_type = list(self.args.values())[0].type

        self._debug_map: list[DebugInstruction] = []
        self.origin_class: ClassType | None = None
        self.file_origin: str | None = None

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

    @property
    def symbols(self) -> dict[str, Variable]:
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

    def debug_map(self) -> list[DebugInstruction]:
        """
        Returns a list with the debug information of each mapped Python instruction inside this method
        """
        from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
        return sorted(self._debug_map, key=lambda instr: VMCodeMapping.instance().get_start_address(instr.code))

    def include_instruction(self, instr_info: DebugInstruction):
        """
        Includes a new instruction in the debug info

        :param instr_info: debug information from the new instruction
        """
        if not any((info.start_line == instr_info.start_line and info.start_col == instr_info.start_col
                    for info in self._debug_map)):
            existing_instr_info: DebugInstruction | None = \
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

    def args_to_be_generated(self) -> list[int]:
        """
        Gets the indexes of the arguments that must be generated.
        If method has `self` arg, it must be in this list.

        By default, all the arguments are generated.

        :return: A list with the indexes of the arguments that must be generated
        """
        return list(range(len(self.args)))
