import ast
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from boa3.internal import constants
from boa3.internal.analyser.astanalyser import IAstAnalyser
from boa3.internal.analyser.model.optimizer import ScopeValue, Undefined
from boa3.internal.analyser.model.optimizer.Operation import Operation
from boa3.internal.exception import CompilerWarning
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.method import Method
from boa3.internal.model.module import Module
from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.operation.unary.unaryoperation import UnaryOperation
from boa3.internal.model.property import Property
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.classes.userclass import UserClass
from boa3.internal.model.type.primitive.primitivetype import PrimitiveType


class AstOptimizer(IAstAnalyser, ast.NodeTransformer):
    """
    This class is responsible for reducing the generated ast.

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    :ivar modules: a list with the analysed modules. Empty by default.
    :ivar symbols: a dictionary that maps the global symbols.
    """

    def __init__(self, analyser, log: bool = False, fail_fast: bool = True):
        super().__init__(analyser.ast_tree, filename=analyser.filename, root_folder=analyser.root,
                         log=log, fail_fast=fail_fast)
        self.modules: Dict[str, Module] = {}
        self.symbols: Dict[str, ISymbol] = analyser.symbol_table

        self._is_optimizing: bool = False
        self.has_changes: bool = False
        self.current_scope: ScopeValue = ScopeValue()

        self._current_class: UserClass = None

        self.analyse_visit(self._tree)

    @property
    def tree(self) -> ast.AST:
        """
        Gets the analysed abstract syntax tree

        :return: the analysed ast
        """
        return self._tree

    def literal_eval(self, node: ast.AST) -> Any:
        """
        Evaluates an expression node containing a Python expression.

        :param node: the node that will be evaluated
        :return: the evaluated expression if the node is valid. Otherwise, returns Undefined.
        """
        try:
            return ast.literal_eval(node)
        except BaseException:
            return Undefined

    def parse_to_node(self, expression: str, origin: ast.AST = None, is_origin_str: bool = False) -> Union[ast.AST, Sequence[ast.AST]]:
        """
        Parses an expression to an ast.

        :param expression: string expression to be parsed
        :param origin: an existing ast. If not None, the parsed node will have the same location of origin.
        :return: the parsed node
        :rtype: ast.AST or Sequence[ast.AST]
        """
        if is_origin_str:
            expression = "'{0}'".format(expression)

        new_node = self.visit(super().parse_to_node(expression, origin))
        if hasattr(new_node, 'op'):
            new_node.op = Operator.get_operation(new_node.op)

        return new_node

    def reset_state(self):
        self.current_scope.reset()

    def get_symbol_id(self, node: ast.AST) -> Optional[str]:
        parts = []
        cur_node = node
        while isinstance(cur_node, ast.Attribute):
            parts.insert(0, cur_node.attr)
            cur_node = cur_node.value

        if isinstance(cur_node, ast.Name):
            parts.insert(0, cur_node.id)

        return constants.ATTRIBUTE_NAME_SEPARATOR.join(parts)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        if node.name in self.symbols:
            class_symbol = self.symbols[node.name]
            if isinstance(class_symbol, UserClass):
                self._current_class = class_symbol

        self.generic_visit(node)
        self._current_class = None
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        symbols = self.symbols if self._current_class is None else self._current_class.symbols
        method = symbols[node.name]

        if isinstance(method, Property):
            method = method.getter

        if isinstance(method, Method):
            self._is_optimizing = True
            self.has_changes = True

            while self.has_changes:
                self.reset_state()
                self.has_changes = False

                super().generic_visit(node)

        self.end_function_optimization()
        return node

    def end_function_optimization(self):
        self.reset_state()
        self.has_changes = False
        self._is_optimizing = False

    def visit_Assign(self, node: ast.Assign) -> ast.AST:
        super().generic_visit(node)
        self.set_variables_value(node.targets, node.value)
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AST:
        super().generic_visit(node)
        self.set_variables_value([node.target], node.value)
        return node

    def visit_AugAssign(self, node: ast.AugAssign) -> ast.AST:
        super().generic_visit(node)

        value = self.parse_to_node("x+y", node)
        value.left = node.target
        value.op = node.op
        value.right = node.value

        self.set_variables_value([node.target], value)
        return node

    def set_variables_value(self, targets: List[ast.AST], value: ast.AST):
        new_value = self.literal_eval(value)
        for target in targets:
            if isinstance(target, ast.Name) and isinstance(target.ctx, ast.Store):
                self.current_scope.assign(target.id)

                if new_value is not Undefined:
                    self.current_scope[target.id] = new_value
                elif target.id in self.current_scope:
                    self.current_scope.remove(target.id)

    def visit_BinOp(self, bin_op: ast.BinOp) -> ast.AST:
        """
        Visitor of a binary operation node

        :param bin_op: the python ast binary operation node
        """
        try:
            super().generic_visit(bin_op)

            left_value = self.literal_eval(bin_op.left)
            right_value = self.literal_eval(bin_op.right)

            if (left_value is Undefined and isinstance(bin_op.left, ast.BinOp)
                    and self.is_symmetric_operation(bin_op.op, bin_op.left.op)):
                left_value, right_value = self.reorder_operations(bin_op, bin_op.left)
            elif (right_value is Undefined and isinstance(bin_op.right, ast.BinOp)
                  and self.is_symmetric_operation(bin_op.op, bin_op.right.op)):
                left_value, right_value = self.reorder_operations(bin_op, bin_op.right)

            value = self._evaluate_binary_operation(left_value, right_value, bin_op.op)
            if value is not None:
                self.has_changes = True
                return self.parse_to_node(str(value), bin_op, isinstance(value, str))
            return bin_op
        except ValueError:
            return bin_op

    def is_symmetric_operation(self, first_op: BinaryOperation, second_op: BinaryOperation) -> bool:
        if not isinstance(first_op, BinaryOperation) or not isinstance(second_op, BinaryOperation):
            return False

        operation = type(first_op)
        second_operation = type(second_op)

        if operation != second_operation:
            return False

        return first_op.is_symmetric

    def reorder_operations(self, outer_bin_op: ast.BinOp, inner_bin_op: ast.BinOp) -> Tuple[Any, Any]:
        inner_first_value = self.literal_eval(inner_bin_op.left)
        inner_second_value = self.literal_eval(inner_bin_op.right)

        if (not (isinstance(outer_bin_op.op, BinaryOperation) and outer_bin_op.op.is_symmetric)
                or not (isinstance(outer_bin_op.op, BinaryOperation) and outer_bin_op.op.is_symmetric)):
            return inner_first_value, inner_second_value

        is_left_operand: bool = inner_bin_op is outer_bin_op.left
        other_value = self.literal_eval(outer_bin_op.right if is_left_operand else outer_bin_op.left)

        if inner_first_value is not Undefined or inner_second_value is not Undefined:
            if inner_first_value is Undefined:
                if other_value is Undefined:
                    if is_left_operand:
                        # (x + 1) + y -> (x + y) + 1
                        inner_bin_op.right, outer_bin_op.right = outer_bin_op.right, inner_bin_op.right
                    else:
                        # y + (x + 1) -> 1 + (x + y)
                        inner_bin_op.right, outer_bin_op.left = outer_bin_op.left, inner_bin_op.right
                else:
                    if is_left_operand:
                        # (x + 2) + 1 -> (1 + 2) + x
                        inner_bin_op.left, outer_bin_op.right = outer_bin_op.right, inner_bin_op.left
                    else:
                        # 1 + (x + 2) -> x + (1 + 2)
                        inner_bin_op.left, outer_bin_op.left = outer_bin_op.left, inner_bin_op.left
            else:
                if other_value is Undefined:
                    if is_left_operand:
                        # (1 + x) + y -> (y + x) + 1
                        inner_bin_op.left, outer_bin_op.right = outer_bin_op.right, inner_bin_op.left
                    else:
                        # y + (1 + x) ->  1 + (y + x)
                        inner_bin_op.left, outer_bin_op.left = outer_bin_op.left, inner_bin_op.left
                else:
                    if is_left_operand:
                        # (2 + x) + 1 -> (2 + 1) + x
                        inner_bin_op.right, outer_bin_op.right = outer_bin_op.right, inner_bin_op.right
                    else:
                        # 1 + (2 + x) -> x + (2 + 1)
                        inner_bin_op.right, outer_bin_op.left = outer_bin_op.left, inner_bin_op.right

        super().generic_visit(outer_bin_op)

        return self.literal_eval(outer_bin_op), self.literal_eval(outer_bin_op)

    def _evaluate_binary_operation(self, left: Any, right: Any,
                                   op: Union[ast.operator, BinaryOperation]) -> Optional[Any]:
        operator = Operation.get_operation(op)
        try:
            if operator is Operation.Add:
                return left + right
            if operator is Operation.Sub:
                return left - right
            if operator is Operation.Mult:
                return left * right
            if operator is Operation.FloorDiv:
                return left // right
            if operator is Operation.Mod:
                return left % right
            return None
        except BaseException:
            return None

    def visit_UnaryOp(self, un_op: ast.UnaryOp) -> ast.AST:
        """
        Visitor of a binary operation node

        :param un_op: the python ast binary operation node
        """
        try:
            self.visit(un_op.operand)

            operand_value = ast.literal_eval(un_op.operand)

            value = self._evaluate_unary_operation(operand_value, un_op.op)
            if value is not None:
                self.has_changes = True
                if hasattr(un_op.operand, 'n'):
                    un_op.operand.n = value
                    self.update_line_and_col(un_op.operand, un_op)
                    return un_op.operand
                return self.parse_to_node(str(value), un_op, isinstance(value, str))
            return un_op
        except ValueError:
            return un_op

    def _evaluate_unary_operation(self, operand: Any, op: Union[ast.operator, UnaryOperation]) -> Optional[Any]:
        operator = Operation.get_operation(op)
        try:
            if operator is Operation.Add:
                return +operand
            elif operator is Operation.Sub:
                return -operand
            return None
        except BaseException:
            return None

    def visit_Match(self, match_node: ast.Match) -> ast.AST:
        self.visit(match_node.subject)

        case_scopes = []

        match_scope = self.current_scope

        for case in match_node.cases:
            case_scopes.append(match_scope.new_scope())

            self.current_scope = case_scopes[-1]
            for stmt in case.body:
                self.visit(stmt)

        self.current_scope = match_scope
        self.current_scope.update_values(*case_scopes)

        return match_node

    def visit_If(self, node: ast.If) -> ast.AST:
        self.visit(node.test)

        if_scope: ScopeValue = self.current_scope.new_scope()
        else_scope: ScopeValue = self.current_scope.new_scope()

        self.current_scope = if_scope
        for stmt in node.body:
            self.visit(stmt)

        if len(node.orelse) > 0:
            self.current_scope = else_scope
            for stmt in node.orelse:
                self.visit(stmt)

        self.current_scope = self.current_scope.previous_scope()
        self.current_scope.update_values(if_scope, else_scope)

        return node

    def visit_loop_body(self, node: ast.AST):
        if not hasattr(node, 'body') or not hasattr(node, 'orelse'):
            self.generic_visit(node)

        loop_scope: ScopeValue = self.current_scope.new_scope()
        # TODO: substitute the variables only if they're not reassigned inside the loop #2kq0wk3
        loop_scope.reset()

        self.current_scope = loop_scope
        for stmt in node.body:
            self.visit(stmt)

        if len(node.orelse) > 0:
            else_scope: ScopeValue = self.current_scope.new_scope()
            self.current_scope = else_scope

            for stmt in node.orelse:
                self.visit(stmt)

            self.current_scope = else_scope.previous_scope()
            loop_scope.update_values(else_scope, is_loop_scope=True)

        outer_scope = self.current_scope.previous_scope()
        outer_scope.update_values(loop_scope)

        return loop_scope

    def visit_For(self, node: ast.For) -> ast.AST:
        self.visit(node.iter)

        for_scope = self.visit_loop_body(node)
        self.current_scope = for_scope.previous_scope()

        return node

    def visit_While(self, node: ast.While) -> ast.AST:
        while_scope = self.visit_loop_body(node)
        self.visit(node.test)

        self.current_scope = while_scope.previous_scope()

        return node

    def visit_Try(self, node: ast.Try) -> ast.AST:
        outer_scope = self.current_scope
        try_scope: ScopeValue = self.current_scope.new_scope()
        except_scopes: List[ScopeValue] = []

        self.current_scope = try_scope
        for stmt in node.body:
            self.visit(stmt)

        if len(node.handlers) > 0:
            for handler in node.handlers:
                except_scope = outer_scope.new_scope()
                self.current_scope = except_scope

                for stmt in handler.body:
                    self.visit(stmt)

                except_scopes.append(except_scope)

        if len(node.orelse) > 0:
            else_scope = outer_scope.new_scope()
            self.current_scope = else_scope

            for stmt in node.orelse:
                self.visit(stmt)

            except_scopes.append(else_scope)

        self.current_scope = self.current_scope.previous_scope()
        self.current_scope.update_values(try_scope, *except_scopes)

        for stmt in node.finalbody:
            self.visit(stmt)

        return node

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if (isinstance(node.ctx, ast.Load)
                and node.id in self.current_scope
                and isinstance(self.get_type(self.current_scope[node.id]), PrimitiveType)):
            # only values from int, bool, str and bytes types are going to replace the variable
            # TODO: check if it's worth to replace other types #2kq0zhe
            value = self.current_scope[node.id]
            if isinstance(value, str):
                value = "'{0}'".format(value)
            return self.parse_to_node(str(value), node)
        return node

    def visit_Call(self, node: ast.Call) -> ast.AST:
        # check if the call can be evaluated during compile time
        # TODO: right now only UInt160 and UInt256 constructors are evaluated #2kq12zd
        literal_args = []
        args_are_literal = True

        for index, arg in enumerate(node.args.copy()):
            updated_arg = self.visit(arg)  # first try to optimize the arguments
            if updated_arg != arg:
                node.args[index] = updated_arg

            if args_are_literal:
                value = self.literal_eval(updated_arg)
                if value is Undefined:
                    # don't break if one argument is not literal to make sure that all arguments were checked
                    # if they can be optimized
                    args_are_literal = False

                literal_args.append(value)

        if args_are_literal:
            # try to get the result
            try:
                func_id = self.get_symbol_id(node.func)
            except BaseException:
                return node
            func = self.get_symbol(func_id)

            if isinstance(func, IBuiltinMethod):
                try:
                    result = func.evaluate_literal(*literal_args)
                    if result is not Undefined:
                        return self.parse_to_node(str(result), node, is_origin_str=isinstance(result, str))
                except BaseException:
                    self._log_warning(CompilerWarning.InvalidArgument(
                        node.lineno, node.col_offset
                    ))

        return node
