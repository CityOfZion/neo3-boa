import ast
from abc import ABC
from typing import List

from boa3.exception.CompilerError import CompilerError
from boa3.exception.CompilerWarning import CompilerWarning


class IAstAnalyser(ABC):
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
