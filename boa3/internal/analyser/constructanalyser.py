import ast
from typing import Dict

from boa3.internal.analyser.astanalyser import IAstAnalyser
from boa3.internal.model import set_internal_call
from boa3.internal.model.symbol import ISymbol


class ConstructAnalyser(IAstAnalyser, ast.NodeTransformer):
    """
    This class is responsible for pre processing Python constructs

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.
    """

    def __init__(self, analyser, ast_tree: ast.AST, symbol_table: Dict[str, ISymbol],
                 log: bool = False, fail_fast: bool = True):
        super().__init__(ast_tree, root_folder=analyser.root, log=log, fail_fast=fail_fast)
        self.symbols = symbol_table.copy()
        self.analyse_visit(self._tree)

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
        if isinstance(call.func, ast.Name):
            from boa3.internal.model.builtin.method import ScriptHashMethod
            to_script_hash = None
            for symbol_id, symbol in self.symbols.items():
                if isinstance(symbol, ScriptHashMethod) and call.func.id == symbol_id:
                    to_script_hash = symbol
                    break

            if to_script_hash is not None:
                from boa3.internal.model.type.type import Type
                types = {
                    Type.int.identifier: int,
                    Type.str.identifier: str,
                    Type.bytes.identifier: bytes
                }

                if len(call.args) != 1:
                    return call

                if isinstance(call.args[0], ast.Constant):
                    value = ast.literal_eval(call.args[0])
                    if not isinstance(value, tuple(types.values())):
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
