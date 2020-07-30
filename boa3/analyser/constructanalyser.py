import ast
from typing import Sequence, Union

from boa3.analyser.astanalyser import IAstAnalyser


class ConstructAnalyser(IAstAnalyser, ast.NodeTransformer):
    """
    This class is responsible for pre processing Python constructs

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.
    """

    def __init__(self, ast_tree: ast.AST, log: bool = False):
        super().__init__(ast_tree, log=log)
        self.visit(self._tree)

    @property
    def tree(self) -> ast.AST:
        """
        Gets the analysed abstract syntax tree

        :return: the analysed ast
        """
        return self._tree

    def parse_to_node(self, expression: str, origin: ast.AST = None) -> Union[ast.AST, Sequence[ast.AST]]:
        """
        Parses an expression to an ast.

        :param expression: string expression to be parsed
        :param origin: an existing ast. If not None, the parsed node will have the same location of origin.
        :return: the parsed node
        :rtype: ast.AST or Sequence[ast.AST]
        """
        node = ast.parse(expression)
        if origin is not None:
            self.update_line_and_col(node, origin)

        # get the expression instead of the default root node
        if hasattr(node, 'body'):
            node = node.body
        elif hasattr(node, 'argtypes'):
            node = node.argtypes

        if isinstance(node, list) and len(node) == 1:
            # the parsed node has a list of expression and only one expression is found
            result = node[0]
        else:
            result = node

        if isinstance(result, ast.Expr):
            # an expr node encapsulates another node in its value field.
            result = result.value
        return result

    def update_line_and_col(self, target: ast.AST, origin: ast.AST):
        """
        Updates the position of a node and its child nodes

        :param target: the node that will have its position updated
        :param origin: the node with the desired position
        """
        ast.copy_location(target, origin)
        for field, value in ast.iter_fields(target):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.update_line_and_col(item, origin)
            elif isinstance(value, ast.AST):
                self.update_line_and_col(value, origin)
        ast.fix_missing_locations(target)
