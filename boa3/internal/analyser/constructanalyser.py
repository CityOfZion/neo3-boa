import ast

from boa3.internal.analyser.astanalyser import IAstAnalyser
from boa3.internal.model import set_internal_call


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

    def visit_Call(self, call: ast.Call) -> ast.AST:
        """
        Visitor of a function call node

        :param call: the python ast function call node
        """
        if isinstance(call.func, ast.Attribute):
            from boa3.internal.model.builtin.builtin import Builtin
            if call.func.attr == Builtin.ScriptHashMethod_.identifier:
                from boa3.internal.constants import SYS_VERSION_INFO
                from boa3.internal.model.type.type import Type
                types = {
                    Type.int.identifier: int,
                    Type.str.identifier: str,
                    Type.bytes.identifier: bytes
                }
                literal: tuple = ((ast.Constant,)
                                  if SYS_VERSION_INFO >= (3, 8)
                                  else (ast.Num, ast.Str, ast.Bytes))

                if isinstance(call.func.value, literal) and len(call.args) == 0:
                    value = ast.literal_eval(call.func.value)
                    if not isinstance(value, tuple(types.values())):
                        return call
                elif (isinstance(call.func.value, ast.Name)  # checks if is the name of a type
                      and call.func.value.id in types  # and if the arguments is from the same type
                      and len(call.args) == 1
                      and isinstance(call.args[0], literal)):
                    value = ast.literal_eval(call.args[0])
                    if not isinstance(value, (types[call.func.value.id],)):
                        return call
                else:
                    return call

                from boa3.internal.neo import to_script_hash
                # value must be bytes
                if isinstance(value, int):
                    from boa3.internal.neo.vm.type.Integer import Integer
                    value = Integer(value).to_byte_array()
                elif isinstance(value, str):
                    from boa3.internal.neo.vm.type.String import String
                    value = String(value).to_bytes()
                return set_internal_call(self.parse_to_node(f"UInt160({str(to_script_hash(value))})", call))

        return call
