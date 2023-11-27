__all__ = [
    'literal_eval_node',
    'INVALID_NODE_RESULT'
]

import ast


class NodeEvaluationResult:
    pass


INVALID_NODE_RESULT = NodeEvaluationResult()


def literal_eval_node(node: ast.AST):
    try:
        return ast.literal_eval(node)
    except ValueError:
        return INVALID_NODE_RESULT
