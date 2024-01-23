import ast

from boa3.internal import constants
from boa3.internal.analyser.astanalyser import IAstAnalyser
from boa3.internal.model.symbol import ISymbol


class InitStatementsVisitor(IAstAnalyser):
    """
    This class is separate the instructions that should be included in the '_deploy" internal method from those
    from the '_initialize' internal method.

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    """

    def __init__(self, symbols: dict[str, ISymbol], fail_fast: bool = True):
        super().__init__(ast.parse(""), log=True, fail_fast=fail_fast)
        self.symbols = symbols.copy()

        self._deploy_instructions: list[ast.AST] = []
        self._init_instructions: list[ast.AST] = []

    @classmethod
    def separate_global_statements(cls,
                                   symbol_table: dict[str, ISymbol],
                                   statements: list[ast.AST]) -> tuple[list[ast.AST], list[ast.AST]]:

        visitor = InitStatementsVisitor(symbol_table)

        root_ast = ast.parse("")
        root_ast.body = statements
        visitor.visit(root_ast)

        return visitor._deploy_instructions, visitor._init_instructions

    def get_symbol_id(self, node: ast.AST, parent: ast.AST) -> str:
        symbol_id = self.visit(node)
        # filter to find the imported variables
        if symbol_id not in self.symbols and hasattr(parent, 'origin') and isinstance(parent.origin, ast.AST):
            symbol_id = '{0}{2}{1}'.format(parent.origin.__hash__(), symbol_id, constants.VARIABLE_NAME_SEPARATOR)
        return symbol_id

    def append_symbol(self, symbol: ISymbol, node: ast.AST):
        if self._should_be_on_deploy(symbol):
            if node not in self._deploy_instructions:
                self._deploy_instructions.append(node)
        else:
            if node not in self._init_instructions:
                self._init_instructions.append(node)

    def _should_be_on_deploy(self, symbol: ISymbol) -> bool:
        return hasattr(symbol, 'is_reassigned') and symbol.is_reassigned

    # region AST visitors

    def visit_Assign(self, node: ast.Assign):
        deploy_var_nodes = []
        init_var_nodes = []

        deploy_symbol = None
        init_symbol = None
        for target in node.targets:
            target_id = self.get_symbol_id(target, node)
            symbol = self.get_symbol(target_id)

            if self._should_be_on_deploy(symbol):
                deploy_var_nodes.append(target)
                deploy_symbol = symbol
            else:
                init_var_nodes.append(target)
                init_symbol = symbol

        if len(deploy_var_nodes) == len(node.targets) or len(init_var_nodes) == len(node.targets):
            self.append_symbol(deploy_symbol if deploy_symbol is not None else init_symbol,
                               node)
        else:
            deploy_ast = ast.Assign(targets=deploy_var_nodes,
                                    value=node.value)
            ast.copy_location(deploy_ast, node)

            init_ast = ast.Assign(targets=init_var_nodes,
                                  value=node.value)
            ast.copy_location(init_ast, node)

            if hasattr(node, 'origin'):
                deploy_ast.origin = node.origin
                init_ast.origin = node.origin

            self.append_symbol(deploy_symbol, deploy_ast)
            self.append_symbol(init_symbol, init_ast)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        var_id = self.get_symbol_id(node.target, node)
        symbol = self.get_symbol(var_id)
        self.append_symbol(symbol, node)

    def visit_AugAssign(self, node: ast.AugAssign):
        var_id = self.get_symbol_id(node.target, node)
        symbol = self.get_symbol(var_id)
        self.append_symbol(symbol, node)

    def visit_Name(self, name: ast.Name) -> str:
        """
        Visitor of a name node

        :param name: the python ast name identifier node
        :return: the identifier of the name
        """
        return name.id

    # endregion
