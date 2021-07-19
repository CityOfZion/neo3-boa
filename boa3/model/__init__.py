import ast


def set_internal_call(node: ast.AST) -> ast.AST:
    node.is_internal_call = True
    node._fields += ('is_internal_call',)
    return node
