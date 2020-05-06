import ast
from abc import ABC
from typing import List, Dict

from boa3.exception.CompilerError import CompilerError
from boa3.exception.CompilerWarning import CompilerWarning
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

    def get_type(self, node: ast.AST) -> IType:
        """
        Get the type of the value stored in the node

        :param node: ast node that represents a value to be evaluated
        :return: the type of the evaluated value. None by default.
        """
        if node is not None:
            fun_rtype_id: str = ast.NodeVisitor.visit(self, node)
        else:
            fun_rtype_id: str = Type.none.identifier

        if fun_rtype_id not in self.symbols:
            return Type.none

        symbol = self.symbols[fun_rtype_id]
        if isinstance(symbol, IType):
            return symbol
        return Type.none
