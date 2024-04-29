import ast
from typing import Self

from boa3.internal.neo.vm.VMCode import VMCode


class DebugInstruction:
    def __init__(self, code: VMCode, start_line: int, start_col: int, end_line: int = None, end_col: int = None):
        if end_line is None or end_line < start_line:
            end_line = start_line
        if end_col is None or end_col < end_col:
            end_col = start_col

        self.code: VMCode = code
        self.start_line: int = start_line
        self.start_col: int = start_col
        self.end_line: int = end_line
        self.end_col: int = end_col

    def __str__(self) -> str:
        return '{0}:{1}-{2}:{3} {4}'.format(self.start_line, self.start_col,
                                            self.end_line, self.end_col,
                                            self.code)

    @classmethod
    def build(cls, ast_node: ast.AST, bytecode: VMCode) -> Self:
        end_line: int = ast_node.end_lineno if hasattr(ast_node, 'end_lineno') else ast_node.lineno
        end_col: int = ast_node.end_col_offset + 1 if hasattr(ast_node, 'end_lineno') else ast_node.col_offset
        return cls(bytecode, ast_node.lineno, ast_node.col_offset, end_line, end_col)
