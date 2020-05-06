import ast
from abc import ABC
from typing import List

from boa3.exception.CompilerError import CompilerError
from boa3.exception.CompilerWarning import CompilerWarning


class IAstAnalyser(ABC):
    """
    An interface for the analysers that walk the Python abstract syntax tree

    This interface doesn't inherit the :class:`NodeVisitor` because there are two kinds of node visitor in the
    `ast` module: :class:`NodeVisitor` and :class:`NodeTransformer`

    :ivar errors: a list that contains all the errors raised by the compiler. Empty by default.
    :ivar warnings: a list that contains all the warnings found by the compiler. Empty by default.
    """
    def __init__(self, ast_tree: ast.AST):
        self.errors: List[CompilerError] = []
        self.warnings: List[CompilerWarning] = []
        self._tree: ast.AST = ast_tree

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def _log_error(self, error: CompilerError):
        self.errors.append(error)

    def _log_warning(self, warning: CompilerWarning):
        self.warnings.append(warning)
