import ast
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from boa3.exception.CompilerError import CompilerError
from boa3.exception.CompilerWarning import CompilerWarning
from boa3.model.expression import IExpression
from boa3.model.symbol import ISymbol
from boa3.model.type.type import IType, Type


class IAstAnalyser(ABC, ast.NodeVisitor):
    """
    An interface for the analysers that walk the Python abstract syntax tree

    :ivar errors: a list that contains all the errors raised by the compiler. Empty by default.
    :ivar warnings: a list that contains all the warnings found by the compiler. Empty by default.
    """
    def __init__(self, ast_tree: ast.AST):
        self.errors: List[CompilerError] = []
        self.warnings: List[CompilerWarning] = []
        self._tree: ast.AST = ast_tree
        self.symbols: Dict[str, ISymbol] = {}

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def _log_error(self, error: CompilerError):
        self.errors.append(error)

    def _log_warning(self, warning: CompilerWarning):
        self.warnings.append(warning)

    def get_type(self, value: Any) -> IType:
        """
        Returns the type of the given value.

        :param value: value to get the type
        :return: Returns the :class:`IType` of the the type of the value. `Type.none` by default.
        """
        if isinstance(value, ast.AST):
            fun_rtype_id: str = ast.NodeVisitor.visit(self, value)
            if fun_rtype_id not in self.symbols:
                return Type.none

            symbol = self.symbols[fun_rtype_id]
            if isinstance(symbol, IType):
                return symbol
            return Type.none
        elif isinstance(value, IType):
            return value
        elif isinstance(value, IExpression):
            return value.type
        elif isinstance(value, bool):
            return Type.bool
        elif isinstance(value, int):
            return Type.int
        elif isinstance(value, str):
            return Type.str

        return Type.none

    @abstractmethod
    def get_symbol(self, symbol_id: str) -> Optional[ISymbol]:
        """
        Tries to get the symbol by its id name

        :param symbol_id: the id name of the symbol
        :return: the symbol if found. None otherwise.
        :rtype: ISymbol or None
        """
        pass
