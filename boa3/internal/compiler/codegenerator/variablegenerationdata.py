import ast
from typing import Optional


class VariableGenerationData:
    def __init__(self, var_id: str, index: Optional[ast.AST], address: int):
        self.var_id: str = var_id
        self.index: Optional[ast.AST] = index
        self.address: int = address

    def __iter__(self):
        yield self.var_id
        yield self.index
        yield self.address
