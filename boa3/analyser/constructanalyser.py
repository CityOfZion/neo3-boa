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

    def visit_Call(self, call: ast.Call):
        """
        Visitor of a function call node

        :param call: the python ast function call node
        """
        if isinstance(call.func, ast.Attribute):
            from boa3.model.builtin.builtin import Builtin
            if call.func.attr == Builtin.ScriptHash.identifier:
                import sys
                from boa3.model.type.type import Type
                types = {
                    Type.int.identifier: int,
                    Type.str.identifier: str,
                    Type.bytes.identifier: bytes
                }
                literal: tuple = ((ast.Constant,)
                                  if sys.version_info > (3, 8)
                                  else (ast.Num, ast.Str, ast.Bytes))

                if isinstance(call.func.value, literal) and len(call.args) == 0:
                    value = ast.literal_eval(call.func.value)
                    if not isinstance(value, tuple(types.values())):
                        return call
                elif (isinstance(call.func.value, ast.Name)     # checks if is the name of a type
                      and call.func.value.id in types        # and if the arguments is from the same type
                      and len(call.args) == 1
                      and isinstance(call.args[0], literal)):
                    value = ast.literal_eval(call.args[0])
                    if not isinstance(value, (types[call.func.value.id],)):
                        return call
                else:
                    return call

                from boa3.neo import to_script_hash
                # value must be bytes
                if isinstance(value, int):
                    from boa3.neo.vm.type.Integer import Integer
                    value = Integer(value).to_byte_array()
                elif isinstance(value, str):
                    from boa3.neo.vm.type.String import String
                    value = String(value).to_bytes()
                return self.parse_to_node(str(to_script_hash(value)), call)

        return call

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
