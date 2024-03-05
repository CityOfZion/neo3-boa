import ast


class VariableGenerationData:
    def __init__(self, var_id: str, index: ast.AST | None, address: int):
        self.var_id: str = var_id
        self.index: ast.AST | None = index
        self.address: int = address

    def __iter__(self):
        yield self.var_id
        yield self.index
        yield self.address
