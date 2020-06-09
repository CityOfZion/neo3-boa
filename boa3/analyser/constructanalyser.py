import ast
from typing import List, Sequence, Union

from boa3 import helpers
from boa3.analyser.astanalyser import IAstAnalyser


class ConstructAnalyser(IAstAnalyser, ast.NodeTransformer):
    """
    This class is responsible for pre processing Python constructs

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.
    """

    def __init__(self, ast_tree: ast.AST):
        super().__init__(ast_tree)
        self.visit(self._tree)

    @property
    def tree(self) -> ast.AST:
        """
        Gets the analysed abstract syntax tree

        :return: the analysed ast
        """
        return self._tree

    def visit_For(self, for_node: ast.For):
        """
        Includes additional operations for converting the for statement into Neo VM

        :param for_node: the python ast for node
        """
        # get auxiliary variables
        var_iter_id = helpers.get_auxiliary_name(for_node, 'iter')
        var_index_id = helpers.get_auxiliary_name(for_node, 'index')

        add_instructs: List[ast.AST] = self.parse_to_node('{0} = x; {1} = 0'.format(var_iter_id, var_index_id), for_node)
        add_instructs[0].value = for_node.iter  # iter auxiliary variable is assigned with the node iter value

        update_target: ast.Assign = self.parse_to_node('x = {0}[{1}]'.format(var_iter_id, var_index_id), for_node)
        update_target.targets[0] = for_node.target  # target variable is updated each loop iteration

        update_index: ast.Assign = self.parse_to_node('{0} = {0} + 1'.format(var_index_id), for_node)
        loop_test: ast.Compare = self.parse_to_node('{0} < len({1})'.format(var_index_id, var_iter_id), for_node)

        for_node.body.insert(0, update_target)
        for_node.body.append(update_index)
        for_node.body.append(loop_test)

        for node in add_instructs:
            self.generic_visit(node)
        self.generic_visit(for_node)

        add_instructs.append(for_node)
        return add_instructs

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
                        ast.copy_location(item, origin)
            elif isinstance(value, ast.AST):
                ast.copy_location(value, origin)
        ast.fix_missing_locations(target)
