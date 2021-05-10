import ast
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

from boa3.analyser.astanalyser import IAstAnalyser
from boa3.analyser.builtinfunctioncallanalyser import BuiltinFunctionCallAnalyser
from boa3.analyser.optimizer import UndefinedType
from boa3.analyser.symbolscope import SymbolScope
from boa3.exception import CompilerError, CompilerWarning
from boa3.model.attribute import Attribute
from boa3.model.builtin.builtin import Builtin
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.callable import Callable
from boa3.model.expression import IExpression
from boa3.model.importsymbol import Import
from boa3.model.method import Method
from boa3.model.module import Module
from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.binaryop import BinaryOp
from boa3.model.operation.operation import IOperation
from boa3.model.operation.operator import Operator
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.operation.unaryop import UnaryOp
from boa3.model.symbol import ISymbol
from boa3.model.type.classtype import ClassType
from boa3.model.type.collection.icollection import ICollectionType as Collection
from boa3.model.type.type import IType, Type
from boa3.model.type.typeutils import TypeUtils
from boa3.model.variable import Variable


class TypeAnalyser(IAstAnalyser, ast.NodeVisitor):
    """
    This class is responsible for the type checking of the code

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    :ivar type_errors: a list with the found type errors. Empty by default.
    :ivar modules: a list with the analysed modules. Empty by default.
    :ivar symbols: a dictionary that maps the global symbols.
    """

    def __init__(self, analyser, symbol_table: Dict[str, ISymbol], log: bool = False):
        super().__init__(analyser.ast_tree, log=log)
        self.type_errors: List[Exception] = []
        self.modules: Dict[str, Module] = {}
        self.symbols: Dict[str, ISymbol] = symbol_table

        self._current_method: Method = None
        self._scope_stack: List[SymbolScope] = []
        self.visit(self._tree)

    @property
    def _current_method_id(self) -> str:
        """
        Get the string identifier of the current method

        :return: The name identifier of the method. If the current method is None, returns None.
        :rtype: str or None
        """
        if self._current_method in self.symbols.values():
            index = list(self.symbols.values()).index(self._current_method)
            return list(self.symbols.keys())[index]

    @property
    def _current_scope(self) -> Optional[SymbolScope]:
        return self._scope_stack[-1] if len(self._scope_stack) > 0 else None

    @property
    def _modules_symbols(self) -> Dict[str, ISymbol]:
        """
        Gets all the symbols in the modules scopes.

        :return: Returns a dictionary that maps the modules symbols.
        """
        symbols = {}
        for module in self.modules.values():
            symbols.update(module.symbols)
        return symbols

    def get_symbol(self, symbol_id: str, is_internal: bool = False) -> Optional[ISymbol]:
        if not isinstance(symbol_id, str):
            return Variable(self.get_type(symbol_id))

        if len(self._scope_stack) > 0:
            for scope in self._scope_stack[::-1]:
                if symbol_id in scope:
                    return scope[symbol_id]

        if self._current_method is not None and symbol_id in self._current_method.symbols:
            # the symbol exists in the local scope
            return self._current_method.symbols[symbol_id]
        elif symbol_id in self.modules:
            # the symbol exists in the modules scope
            return self.modules[symbol_id]
        else:
            return super().get_symbol(symbol_id, is_internal)

    def new_local_scope(self, symbols: Dict[str, ISymbol] = None):
        if symbols is None:
            symbols = self._current_scope.symbols if self._current_scope is not None else {}

        self._scope_stack.append(SymbolScope(symbols))

    def pop_local_scope(self) -> SymbolScope:
        return self._scope_stack.pop()

    def visit_Module(self, module: ast.Module):
        """
        Visitor of the module node

        Performs the type checking in the body of the method

        :param module: the python ast module node
        """
        for stmt in module.body:
            self.visit(stmt)

    def visit_FunctionDef(self, function: ast.FunctionDef):
        """
        Visitor of the function node

        Performs the type checking in the body of the function

        :param function: the python ast function definition node
        """
        self.visit(function.args)
        method = self.symbols[function.name]

        from boa3.model.event import Event
        if isinstance(method, Method):
            self._current_method = method
            self.new_local_scope({var_id: var for var_id, var in method.symbols.items()
                                  if isinstance(var, Variable) and var.type is not UndefinedType})

            for stmt in function.body:
                self.visit(stmt)

            self._validate_return(function)

            method_scope = self.pop_local_scope()
            self._current_method = None
        elif (isinstance(method, Event)  # events don't have return
              and function.returns is not None):
            return_type = self.get_type(function.returns)
            if return_type is not Type.none:
                self._log_error(
                    CompilerError.MismatchedTypes(line=function.lineno, col=function.col_offset,
                                                  expected_type_id=Type.none.identifier,
                                                  actual_type_id=return_type.identifier)
                )

    def visit_arguments(self, arguments: ast.arguments):
        """
        Verifies if each argument of a function has a type annotation

        :param arguments: the python ast function arguments node
        """
        for arg in arguments.args:
            self.visit(arg)

        # continue to walk through the tree
        self.generic_visit(arguments)

    def visit_arg(self, arg: ast.arg):
        """
        Verifies if the argument of a function has a type annotation

        :param arg: the python ast arg node
        """
        if arg.annotation is None:
            self._log_error(
                CompilerError.TypeHintMissing(arg.lineno, arg.col_offset, symbol_id=arg.arg)
            )

        # continue to walk through the tree
        self.generic_visit(arg)

    def visit_Return(self, ret: ast.Return):
        """
        Verifies if the return of the function is the same type as the return type annotation

        :param ret: the python ast return node
        """
        ret_value: Any = self.visit(ret.value) if ret.value is not None else None
        if ret.value is not None and self.get_type(ret.value) is not Type.none:
            # multiple returns are not allowed
            if isinstance(ret.value, ast.Tuple):
                self._log_error(
                    CompilerError.TooManyReturns(ret.lineno, ret.col_offset)
                )
                return
            # it is returning something, but there is no type hint for return
            elif self._current_method.return_type is Type.none:
                self._log_error(
                    CompilerError.TypeHintMissing(ret.lineno, ret.col_offset, symbol_id=self._current_method_id)
                )
                return
        self.validate_type_variable_assign(ret, ret_value, self._current_method)

        # continue to walk through the tree
        self.generic_visit(ret)

    def _validate_return(self, node: ast.AST):
        if (self._current_method.return_type is not Type.none
                and hasattr(node, 'body')
                and not self._has_return(node)):
            lst = list(self.symbols.items())
            keys, values = [key_value[0] for key_value in lst], [key_value[-1] for key_value in lst]
            self._log_error(
                CompilerError.MissingReturnStatement(
                    line=node.lineno, col=node.col_offset,
                    symbol_id=keys[values.index(self._current_method)]
                )
            )

    def _has_return(self, node: ast.AST) -> bool:
        if not hasattr(node, 'body'):
            return False

        has_else_stmt: bool = hasattr(node, 'orelse')
        has_body_return: bool = any(isinstance(stmt, (ast.Return, ast.Pass)) for stmt in node.body)
        if has_body_return and not has_else_stmt:
            # if any statement in the function body is a return, all flow has a return
            return True

        body = [stmt for stmt in node.body if hasattr(stmt, 'body')]
        body_has_inner_return: bool = len(body) > 0 and all(self._has_return(stmt) for stmt in body)
        if not has_body_return and not body_has_inner_return:
            # for and while nodes must to check if there is a return inside the else statement
            if not isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                return False

        if has_else_stmt:
            if any(isinstance(stmt, (ast.Return, ast.Pass)) for stmt in node.orelse):
                return True
            else:
                orelse = [stmt for stmt in node.orelse if hasattr(stmt, 'body')]
                return len(orelse) > 0 and all(self._has_return(stmt) for stmt in orelse)
        return body_has_inner_return

    def visit_Assign(self, assign: ast.Assign):
        """
        Verifies if it is a multiple assignments statement

        :param assign: the python ast variable assignment node
        """
        # multiple assignments
        if isinstance(assign.targets[0], ast.Tuple):
            self._log_error(
                CompilerError.NotSupportedOperation(assign.lineno, assign.col_offset, 'Multiple variable assignments')
            )
        else:
            for target in assign.targets:
                self.validate_type_variable_assign(target, assign.value)

        # continue to walk through the tree
        self.generic_visit(assign)

    def visit_AnnAssign(self, ann_assign: ast.AnnAssign):
        """
        Verifies if the assigned type is the same as the variable type

        :param ann_assign: the python ast variable annotated assignment node
        """
        # if value is None, it is a declaration
        if ann_assign.value is not None:
            self.validate_type_variable_assign(ann_assign.target, ann_assign.value, implicit_cast=True)

    def visit_AugAssign(self, aug_assign: ast.AugAssign):
        """
        Verifies if the types of the target variable and the value are compatible with the operation

        If the operation is valid, changes de Python operator by the Boa operator in the syntax tree

        :param aug_assign: the python ast augmented assignment node
        """
        operation = self.validate_binary_operation(aug_assign, aug_assign.target, aug_assign.value)
        if operation is not None:
            # TODO: remove when other augmented assignment operations are implemented
            if operation.result not in [Type.int, Type.str]:
                raise NotImplementedError

            self.validate_type_variable_assign(aug_assign.target, operation)
            aug_assign.op = operation

    def validate_type_variable_assign(self, node: ast.AST, value: Any, target: Any = None,
                                      implicit_cast: bool = False) -> bool:
        value_type: IType = self.get_type(value)
        if isinstance(value, ast.AST):
            value = self.visit(value)
            if isinstance(value, ast.Name):
                symbol: ISymbol = self.get_symbol(value.id)
                if isinstance(symbol, IExpression):
                    value_type = symbol.type
                elif isinstance(symbol, IType):
                    value_type = symbol
                else:
                    self._log_error(
                        CompilerError.UnresolvedReference(
                            value.lineno, value.col_offset,
                            symbol_id=value.id
                        ))

        if target is not None:
            target_type = self.get_type(target)
        elif not isinstance(node, ast.Name):
            target_type = self.get_type(node)
        else:
            var: ISymbol = self.get_symbol(node.id)
            if not isinstance(var, Variable):
                self._log_error(
                    CompilerError.UnresolvedReference(
                        node.lineno, node.col_offset,
                        symbol_id=node.id
                    ))
                return False

            if var.type is UndefinedType:
                var = var.copy()

            if var.type in (None, UndefinedType):
                # it is an declaration with assignment and the value is neither literal nor another variable
                var.set_type(value_type)
            target_type = var.type

        if self._current_scope is not None:
            if isinstance(node, ast.Name):
                if node.id not in self._current_scope:
                    if not isinstance(value_type, Collection):
                        target_type = value_type
                    elif not (isinstance(type(value_type), type(target_type)) and
                              (value_type.value_type is Type.any or value_type.valid_key is Type.any)):
                        # if the collection is generic, let the validation for the outer scope
                        value_type = target_type

                    self._current_scope.include_symbol(node.id, Variable(value_type))

                else:
                    if self._current_method is not None and node.id in self._current_method.symbols:
                        can_change_target_type = self._current_method.symbols[node.id].type is UndefinedType
                    else:
                        can_change_target_type = True

                    if can_change_target_type:
                        if (not target_type.is_type_of(value_type) and
                                value != target_type.default_value):
                            target_type = value_type
                        self._current_scope.include_symbol(node.id, Variable(value_type))

        if not target_type.is_type_of(value_type) and value != target_type.default_value:
            if not implicit_cast:
                self._log_error(
                    CompilerError.MismatchedTypes(
                        node.lineno, node.col_offset,
                        actual_type_id=value_type.identifier,
                        expected_type_id=target_type.identifier
                    ))
                return False
            else:
                self._log_warning(
                    CompilerWarning.TypeCasting(
                        node.lineno, node.col_offset,
                        origin_type_id=value_type.identifier,
                        cast_type_id=target_type.identifier
                    )
                )

        return True

    def visit_Subscript(self, subscript: ast.Subscript) -> IType:
        """
        Verifies if the subscribed value is a sequence

        :param subscript: the python ast subscript node
        :return: the type of the accessed value if it is valid. Type.none otherwise.
        """
        if isinstance(subscript.slice, ast.Slice):
            return self.validate_slice(subscript, subscript.slice)

        return self.validate_get_or_set(subscript, subscript.slice)

    def validate_get_or_set(self, subscript: ast.Subscript, index_node: ast.AST) -> IType:
        """
        Verifies if the subscribed value is a sequence and if the index is valid to this sequence

        :param subscript: the python ast subscript node
        :param index_node: the subscript index
        :return: the type of the accessed value if it is valid. Type.none otherwise.
        """
        value = self.visit(subscript.value)
        index = self.visit(index_node)

        if isinstance(value, ast.Name):
            value = self.get_symbol(value.id)
        if isinstance(index, ast.Name):
            index = self.get_symbol(index.id)
        if not isinstance(index, tuple):
            index = (index,)

        # if it is a type hint, returns the outer type
        if isinstance(value, IType) and all(isinstance(i, IType) for i in index):
            if isinstance(value, Collection):
                value = value.build_collection(*index)
            return TypeUtils.type.build(value)

        symbol_type: IType = self.get_type(value)
        index_type: IType = self.get_type(index[0])

        # only sequence types can be subscribed
        if not isinstance(symbol_type, Collection):
            self._log_error(
                CompilerError.UnresolvedOperation(
                    subscript.lineno, subscript.col_offset,
                    type_id=symbol_type.identifier,
                    operation_id=Operator.Subscript)
            )
            return symbol_type
        # the sequence can't use the given type as index
        if not symbol_type.is_valid_key(index_type):
            self._log_error(
                CompilerError.MismatchedTypes(
                    subscript.lineno, subscript.col_offset,
                    actual_type_id=index_type.identifier,
                    expected_type_id=symbol_type.valid_key.identifier)
            )
        # it is setting a value in a sequence that doesn't allow reassign values
        elif isinstance(subscript.ctx, ast.Store) and not symbol_type.can_reassign_values:
            self._log_error(
                CompilerError.UnresolvedOperation(
                    subscript.lineno, subscript.col_offset,
                    type_id=symbol_type.identifier,
                    operation_id=Operator.Subscript)
            )
        return symbol_type.item_type

    def validate_slice(self, subscript: ast.Subscript, slice_node: ast.Slice) -> IType:
        """
        Verifies if the subscribed value is a sequence and if the slice is valid to this sequence

        :param subscript: the python ast subscript node
        :param slice_node: the subscript slice
        :return: the type of the accessed value if it is valid. Type.none otherwise.
        """
        value = self.visit(subscript.value)
        lower, upper, step = (self.get_type(value) for value in self.visit(slice_node))

        if step is not Type.none:
            # TODO: remove when slices with stride are implemented
            raise NotImplementedError
        # is not allowed to store into a slice
        if isinstance(subscript.ctx, ast.Store):
            self._log_error(
                CompilerError.NotSupportedOperation(
                    subscript.lineno, subscript.col_offset,
                    symbol_id=Operator.Subscript
                )
            )

        symbol_type: IType = self.get_type(value)
        # only collection types can be subscribed
        if not isinstance(symbol_type, Collection):
            self._log_error(
                CompilerError.UnresolvedOperation(
                    subscript.lineno, subscript.col_offset,
                    type_id=symbol_type.identifier,
                    operation_id=Operator.Subscript)
            )
            return Type.none

        lower = lower if lower is not Type.none else symbol_type.valid_key
        upper = upper if upper is not Type.none else symbol_type.valid_key

        # TODO: remove when slices of other sequence types are implemented
        if (not symbol_type.is_valid_key(lower)
                or not symbol_type.is_valid_key(upper)
                or (step is not Type.none and not symbol_type.is_valid_key(step))
            ):
            actual: Tuple[IType, ...] = (lower, upper) if step is Type.none else (lower, upper, step)
            self._log_error(
                CompilerError.MismatchedTypes(
                    subscript.lineno, subscript.col_offset,
                    expected_type_id=[symbol_type.valid_key.identifier for value in actual],
                    actual_type_id=[value.identifier for value in actual]
                )
            )
        else:
            return symbol_type

        return Type.none

    def visit_While(self, while_node: ast.While):
        """
        Verifies if the type of while test is valid

        :param while_node: the python ast while statement node
        """
        test = self.visit(while_node.test)
        test_type: IType = self.get_type(test)

        if test_type is not Type.bool:
            self._log_error(
                CompilerError.MismatchedTypes(
                    while_node.lineno, while_node.col_offset,
                    actual_type_id=test_type.identifier,
                    expected_type_id=Type.bool.identifier)
            )

        # continue to walk through the tree
        for stmt in while_node.body:
            self.visit(stmt)
        for stmt in while_node.orelse:
            self.visit(stmt)

    def visit_For(self, for_node: ast.For):
        """
        Verifies if the type of for iterator is valid

        :param for_node: the python ast for node
        """
        iterator = self.visit(for_node.iter)
        iterator_type: IType = self.get_type(iterator)

        if not isinstance(iterator_type, Collection):
            self._log_error(
                CompilerError.MismatchedTypes(
                    for_node.lineno, for_node.col_offset,
                    actual_type_id=iterator_type.identifier,
                    expected_type_id=Type.sequence.identifier)
            )

        # TODO: change when optimizing for loops
        elif self.get_type(for_node.target) != iterator_type.item_type:
            target_id = self.visit(for_node.target)
            if isinstance(target_id, ast.Name):
                target_id = target_id.id
            symbol = self.get_symbol(target_id)
            symbol.set_type(iterator_type.item_type)

        # continue to walk through the tree
        for stmt in for_node.body:
            self.visit(stmt)
        for stmt in for_node.orelse:
            self.visit(stmt)

    def visit_If(self, if_node: ast.If):
        """
        Verifies if the type of if test is valid

        :param if_node: the python ast if statement node
        """
        is_instance_if, is_instance_else = self.validate_if(if_node)

        # continue to walk through the tree
        self.new_local_scope(is_instance_if)
        for stmt in if_node.body:
            self.visit(stmt)
        is_instance_if = self.pop_local_scope().symbols

        self.new_local_scope(is_instance_else)
        for stmt in if_node.orelse:
            self.visit(stmt)
        is_instance_else = self.pop_local_scope().symbols

        last_scope = self._current_scope if len(self._scope_stack) > 0 else self._current_method
        # updates the outer scope for each variable that is changed in both branches
        intersected_ids = is_instance_if.keys() & is_instance_else.keys()
        for changed_symbol in intersected_ids:
            new_value_type_if_branch = self.get_type(is_instance_if[changed_symbol])
            new_value_type_else_branch = self.get_type(is_instance_else[changed_symbol])
            new_type = Type.union.build([new_value_type_if_branch, new_value_type_else_branch])
            last_scope.include_symbol(changed_symbol, Variable(new_type))

        # updates with the variables assigned in a branch that doesn't exist in the outer scope
        self._include_symbols_to_scope(last_scope, is_instance_if, intersected_ids)
        self._include_symbols_to_scope(last_scope, is_instance_else, intersected_ids)

    def _include_symbols_to_scope(self, scope: SymbolScope, other_scope: Dict[str, ISymbol], items_filter: Set[str]):
        for new_symbol in {key for key in other_scope if key not in items_filter}:
            new_value_type = self.get_type(other_scope[new_symbol])
            outer_symbol = self.get_symbol(new_symbol)
            outer_value_type = outer_symbol.type if isinstance(outer_symbol, IExpression) else Type.none

            new_type = Type.union.build([new_value_type, outer_value_type])
            scope.include_symbol(new_symbol, Variable(new_type))

    def visit_IfExp(self, if_node: ast.IfExp):
        """
        Verifies if the type of if test is valid

        :param if_node: the python ast if expression node
        """
        is_instance_if, is_instance_else = self.validate_if(if_node)
        body = if_node.body
        orelse = if_node.orelse
        if_value = body[-1] if isinstance(body, list) and len(body) > 0 else body
        else_value = orelse[-1] if isinstance(orelse, list) and len(orelse) > 0 else orelse

        self.new_local_scope(is_instance_if)
        if_type: IType = self.get_type(if_value)
        self.pop_local_scope()

        self.new_local_scope(is_instance_else)
        else_type: IType = self.get_type(else_value)
        self.pop_local_scope()

        return Type.get_generic_type(if_type, else_type)

    def validate_if(self, if_node: ast.AST) -> Tuple[Dict[str, ISymbol], Dict[str, ISymbol]]:
        """
        Verifies if the type of if test is valid

        :param if_node: the python ast if statement node
        :type if_node: ast.If or ast.IfExp
        """
        test = self.visit(if_node.test)
        test_type: IType = self.get_type(test)

        if test_type is not Type.bool:
            self._log_error(
                CompilerError.MismatchedTypes(
                    if_node.lineno, if_node.col_offset,
                    actual_type_id=test_type.identifier,
                    expected_type_id=Type.bool.identifier)
            )

        return self._get_is_instance_function_calls(if_node.test)

    def _get_is_instance_function_calls(self, node: ast.AST) -> Tuple[Dict[str, ISymbol], Dict[str, ISymbol]]:
        from boa3.model.builtin.method.isinstancemethod import IsInstanceMethod
        is_instance_objs = [x for x, symbol in self.symbols.items()
                            if isinstance(symbol, IsInstanceMethod)]
        is_instance_objs.append(isinstance.__name__)

        is_instance_symbols = {}
        is_not_instance_symbols = {}

        if isinstance(node, ast.BoolOp) and isinstance(node.op, type(BinaryOp.And)):
            conditions = node.values
        else:
            conditions = [node]

        for condition in conditions:
            negate = False
            if isinstance(condition, ast.UnaryOp) and isinstance(condition.op, type(UnaryOp.Not)):
                condition = condition.operand
                negate = True

            if (isinstance(condition, ast.Call) and isinstance(condition.func, ast.Name)
                    and condition.func.id in is_instance_objs and len(condition.args) == 2):
                original = self.get_symbol(condition.args[0])
                if isinstance(original, Variable) and isinstance(condition.args[0], ast.Name):
                    original_id = condition.args[0].id
                    original_type = (original.type
                                     if original_id not in is_instance_symbols
                                     else is_instance_symbols[original_id])

                    instance_obj = self.get_symbol(condition.func.id)
                    if isinstance(instance_obj, type(Builtin.IsInstance)):
                        is_instance_type = instance_obj._instances_type
                        if isinstance(is_instance_type, list):
                            is_instance_type = Type.union.build(is_instance_type)
                    else:
                        is_instance_type = self.get_type(condition.args[1])
                    is_instance_type = is_instance_type.intersect_type(original_type)
                    negation = original_type.except_type(is_instance_type)
                    resulting_type = is_instance_type if not negate else negation

                    if original_id not in is_not_instance_symbols:
                        is_instance_symbols[original_id] = resulting_type
                    else:
                        is_instance_symbols[original_id] = is_instance_symbols[original_id].except_type(resulting_type)

                    if len(is_instance_symbols) == 1:
                        is_not_instance_symbols[original_id] = is_instance_type if negate else negation
                    elif len(is_not_instance_symbols) > 1:
                        is_not_instance_symbols.clear()

        for key, value in is_instance_symbols.copy().items():
            if value == self.get_type(self.get_symbol(key)):
                is_instance_symbols.pop(key)
            else:
                is_instance_symbols[key] = Variable(value)

        for key, value in is_not_instance_symbols.copy().items():
            if value == self.get_type(self.get_symbol(key)):
                is_not_instance_symbols.pop(key)
            else:
                is_not_instance_symbols[key] = Variable(value)
        return is_instance_symbols, is_not_instance_symbols

    def visit_BinOp(self, bin_op: ast.BinOp) -> Optional[IType]:
        """
        Verifies if the types of the operands are valid to the operation

        If the operation is valid, changes de Python operator by the Boa operator in the syntax tree

        :param bin_op: the python ast binary operation node
        :return: the type of the result of the operation if the operation is valid. Otherwise, returns None
        :rtype: IType or None
        """
        operation = self.validate_binary_operation(bin_op, bin_op.left, bin_op.right)
        if operation is not None:
            bin_op.op = operation
            return operation.result

    def validate_binary_operation(self, node: ast.AST, left_op: ast.AST, right_op: ast.AST) -> Optional[IOperation]:
        """
        Validates a ast node that represents a binary operation

        :param node: ast node that represents a binary operation
        :param left_op: ast node that represents the left operand of the operation
        :param right_op: ast node that represents the right operand of the operation
        :return: the corresponding :class:`BinaryOperation` if is valid. None otherwise.
        """
        if not hasattr(node, 'op'):
            return

        operator: Operator = self.get_operator(node.op)
        l_operand = self.visit(left_op)
        r_operand = self.visit(right_op)

        if not isinstance(operator, Operator):
            # the operator is invalid or it was not implemented yet
            self._log_error(
                CompilerError.UnresolvedReference(node.lineno, node.col_offset, type(node.op).__name__)
            )

        try:
            operation: IOperation = self.get_bin_op(operator, r_operand, l_operand)
            if operation is None:
                self._log_error(
                    CompilerError.NotSupportedOperation(node.lineno, node.col_offset, operator)
                )
            elif not operation.is_supported:
                # TODO: concat and power not implemented yet
                # number float division is not supported by Neo VM
                self._log_error(
                    CompilerError.NotSupportedOperation(node.lineno, node.col_offset, operator)
                )
            else:
                return operation
        except CompilerError.MismatchedTypes as raised_error:
            raised_error.line = node.lineno
            raised_error.col = node.col_offset
            # raises the exception with the line/col info
            self._log_error(raised_error)

    def get_bin_op(self, operator: Operator, right: Any, left: Any) -> IOperation:
        """
        Returns the binary operation specified by the operator and the types of the operands

        :param operator: the operator
        :param right: right operand
        :param left: left operand

        :return: Returns the corresponding :class:`BinaryOperation` if the types are valid.
        :raise MismatchedTypes: raised if the types aren't valid for the operator
        """
        l_type: IType = self.get_type(left)
        r_type: IType = self.get_type(right)

        if l_type is None or r_type is None:
            return BinaryOp.get_operation_by_operator(operator, l_type if l_type is not None else r_type)

        actual_types = (l_type.identifier, r_type.identifier)
        operation: IOperation = BinaryOp.validate_type(operator, l_type, r_type)

        if operation is not None:
            return operation
        else:
            if operator.requires_right_operand_for_validation():
                left = l_type
                right = r_type
            else:
                left = l_type if left is not None else r_type
                right = None

            expected_op: BinaryOperation = BinaryOp.get_operation_by_operator(operator, left, right)
            expected_types = (expected_op.left_type.identifier, expected_op.right_type.identifier)
            raise CompilerError.MismatchedTypes(0, 0, expected_types, actual_types)

    def visit_UnaryOp(self, un_op: ast.UnaryOp) -> Optional[IType]:
        """
        Verifies if the type of the operand is valid to the operation

        If the operation is valid, changes de Python operator by the Boa operator in the syntax tree

        :param un_op: the python ast unary operation node
        :return: the type of the result of the operation if the operation is valid. Otherwise, returns None
        :rtype: IType or None
        """
        operator: Operator = self.get_operator(un_op.op)
        operand = self.visit(un_op.operand)

        if not isinstance(operator, Operator):
            # the operator is invalid or it was not implemented yet
            self._log_error(
                CompilerError.UnresolvedReference(un_op.lineno, un_op.col_offset, type(un_op.op).__name__)
            )

        try:
            operation: UnaryOperation = self.get_un_op(operator, operand)
            if operation is None:
                self._log_error(
                    CompilerError.NotSupportedOperation(un_op.lineno, un_op.col_offset, operator)
                )
            elif not operation.is_supported:
                self._log_error(
                    CompilerError.NotSupportedOperation(un_op.lineno, un_op.col_offset, operator)
                )
            else:
                un_op.op = operation
                return operation.result
        except CompilerError.MismatchedTypes as raised_error:
            raised_error.line = un_op.lineno
            raised_error.col = un_op.col_offset
            # raises the exception with the line/col info
            self._log_error(raised_error)

    def get_un_op(self, operator: Operator, operand: Any) -> UnaryOperation:
        """
        Returns the binary operation specified by the operator and the types of the operands

        :param operator: the operator
        :param operand: the operand

        :return: Returns the corresponding :class:`UnaryOperation` if the types are valid.
        :raise MismatchedTypes: raised if the types aren't valid for the operator
        """
        op_type: IType = self.get_type(operand)

        actual_type: str = op_type.identifier
        operation: UnaryOperation = UnaryOp.validate_type(operator, op_type)

        if operation is not None:
            return operation
        else:
            expected_op: UnaryOperation = UnaryOp.get_operation_by_operator(operator)
            expected_type: str = expected_op.operand_type.identifier
            raise CompilerError.MismatchedTypes(0, 0, expected_type, actual_type)

    def visit_Compare(self, compare: ast.Compare) -> Optional[IType]:
        """
        Verifies if the types of the operands are valid to the compare operations

        If the operations are valid, changes de Python operator by the Boa operator in the syntax tree

        :param compare: the python ast compare operation node
        :return: the type of the result of the operation if the operation is valid. Otherwise, returns None
        :rtype: IType or None
        """
        if len(compare.comparators) != len(compare.ops):
            self._log_error(
                CompilerError.IncorrectNumberOfOperands(
                    compare.lineno,
                    compare.col_offset,
                    len(compare.ops),
                    len(compare.comparators) + 1  # num comparators + compare.left
                )
            )

        line = compare.lineno
        col = compare.col_offset
        try:
            return_type = None
            l_operand = self.visit_value(compare.left)
            for index, op in enumerate(compare.ops):
                operator: Operator = self.get_operator(op)
                r_operand = self.visit_value(compare.comparators[index])

                if not isinstance(operator, Operator):
                    # the operator is invalid or it was not implemented yet
                    self._log_error(
                        CompilerError.UnresolvedReference(line, col, type(op).__name__)
                    )

                operation: IOperation = self.get_bin_op(operator, r_operand, l_operand)
                if operation is None:
                    self._log_error(
                        CompilerError.NotSupportedOperation(line, col, operator)
                    )
                elif not operation.is_supported:
                    # TODO: is, is not and eq were not implemented yet
                    self._log_error(
                        CompilerError.NotSupportedOperation(line, col, operator)
                    )
                else:
                    compare.ops[index] = operation
                    return_type = operation.result

                line = compare.comparators[index].lineno
                col = compare.comparators[index].col_offset
                l_operand = r_operand

            return return_type
        except CompilerError.MismatchedTypes as raised_error:
            raised_error.line = line
            raised_error.col = col
            # raises the exception with the line/col info
            self._log_error(raised_error)

    def visit_BoolOp(self, bool_op: ast.BoolOp) -> Optional[IType]:
        """
        Verifies if the types of the operands are valid to the boolean operations

        If the operations are valid, changes de Python operator by the Boa operator in the syntax tree

        :param bool_op: the python ast boolean operation node
        :return: the type of the result of the operation if the operation is valid. Otherwise, returns None
        :rtype: IType or None
        """
        lineno: int = bool_op.lineno
        col_offset: int = bool_op.col_offset
        try:
            return_type: IType = None
            bool_operation: IOperation = None
            operator: Operator = self.get_operator(bool_op.op)

            if not isinstance(operator, Operator):
                # the operator is invalid or it was not implemented yet
                self._log_error(
                    CompilerError.UnresolvedReference(lineno, col_offset, type(operator).__name__)
                )

            l_operand = self.visit(bool_op.values[0])
            for index, operand in enumerate(bool_op.values[1:]):
                r_operand = self.visit(operand)

                operation: IOperation = self.get_bin_op(operator, r_operand, l_operand)
                if operation is None:
                    self._log_error(
                        CompilerError.NotSupportedOperation(lineno, col_offset, operator)
                    )
                elif bool_operation is None:
                    return_type = operation.result
                    bool_operation = operation

                lineno = operand.lineno
                col_offset = operand.col_offset
                l_operand = r_operand

            bool_op.op = bool_operation
            return return_type
        except CompilerError.MismatchedTypes as raised_error:
            raised_error.line = lineno
            raised_error.col = col_offset
            # raises the exception with the line/col info
            self._log_error(raised_error)

    def get_operator(self, node: Union[ast.operator, Operator, IOperation]) -> Optional[Operator]:
        """
        Gets the :class:`Operator` equivalent to given Python ast operator

        :param node: object with the operator data
        :type node: ast.operator or Operator or IOperation
        :return: the Boa operator equivalent to the node. None if it doesn't exit.
        :rtype: Operator or None
        """
        # the node has already been visited
        if isinstance(node, Operator):
            return node
        elif isinstance(node, IOperation):
            return node.operator

        return Operator.get_operation(node)

    def visit_Call(self, call: ast.Call):
        """
        Verifies if the number of arguments is correct

        :param call: the python ast function call node
        :return: the result type of the called function
        """
        if isinstance(call.func, ast.Name):
            callable_id: str = call.func.id
            is_internal = hasattr(call, 'is_internal_call') and call.is_internal_call
            callable_target = self.get_symbol(callable_id, is_internal)
        else:
            callable_id, callable_target = self.get_callable_and_update_args(call)  # type: str, ISymbol

        callable_target = self.validate_builtin_callable(callable_id, callable_target)

        if not isinstance(callable_target, Callable):
            # if the outer call is a builtin, enable call even without the import
            builtin_symbol = Builtin.get_any_symbol(callable_id)
            if builtin_symbol is not None:
                callable_target = builtin_symbol

        callable_method_id = None
        if isinstance(callable_target, ClassType):
            callable_target = callable_target.constructor_method()
            callable_method_id = '__init__'

        if not isinstance(callable_target, Callable):
            # the symbol doesn't exists or is not a function
            # if it is None, the error was already logged
            if callable_id is not None:
                if callable_method_id is not None:
                    callable_id = '{0}.{1}()'.format(callable_id, callable_method_id)
                self._log_error(
                    CompilerError.UnresolvedReference(call.func.lineno, call.func.col_offset, callable_id)
                )
        else:
            if callable_target is Builtin.NewEvent:
                return callable_target.return_type
            # TODO: change when kwargs is implemented
            if len(call.keywords) > 0:
                raise NotImplementedError

            private_identifier = None  # used for validating internal builtin methods
            if self.validate_callable_arguments(call, callable_target):
                args = [self.get_type(param, use_metatype=True) for param in call.args]
                if isinstance(callable_target, IBuiltinMethod):
                    # if the arguments are not generic, build the specified method
                    if callable_target.raw_identifier.startswith('-'):
                        private_identifier = callable_target.raw_identifier
                    callable_target: IBuiltinMethod = callable_target.build(args)
                    if not callable_target.is_supported:
                        self._log_error(
                            CompilerError.NotSupportedOperation(call.lineno, call.col_offset,
                                                                callable_target.not_supported_str(callable_id))
                        )
                        return callable_target.return_type

                    if callable_target.is_cast:
                        # every typing cast raises a warning
                        cast_types = callable_target.cast_types
                        if cast_types is None:
                            origin_type_id = 'unknown'
                            cast_type_id = callable_target.type.identifier
                        else:
                            origin_type_id = cast_types[0].identifier
                            cast_type_id = cast_types[1].identifier

                        self._log_warning(
                            CompilerWarning.TypeCasting(call.lineno, call.col_offset,
                                                        origin_type_id=origin_type_id,
                                                        cast_type_id=cast_type_id)
                        )

                self.validate_passed_arguments(call, args, callable_id, callable_target)

            if private_identifier is not None and callable_target.identifier != private_identifier:
                # updates the callable_id for validation of internal builtin that accepts generic variables
                callable_id = private_identifier
            self.update_callable_after_validation(call, callable_id, callable_target)

        return self.get_type(callable_target)

    def get_callable_and_update_args(self, call: ast.Call) -> Tuple[str, ISymbol]:
        attr: Attribute = self.visit(call.func)
        arg0, callable_target, callable_id = attr.values
        arg0_identifier = self.visit(arg0)
        if isinstance(arg0_identifier, ast.Name):
            arg0_identifier = arg0_identifier.id

        if (callable_target is not None
                and (len(call.args) < 1 or call.args[0] != arg0)
                and not isinstance(self.get_symbol(arg0_identifier), (IType, Import))):
            call.args.insert(0, arg0)

        if len(call.args) > 0 and isinstance(callable_target, IBuiltinMethod) and callable_target.has_self_argument:
            self_type: IType = self.get_type(call.args[0])
            caller = self.get_symbol(arg0_identifier)
            if isinstance(caller, IType) and not caller.is_type_of(self_type):
                self_type = caller
            callable_target = callable_target.build(self_type)

        return callable_id, callable_target

    def validate_builtin_callable(self, callable_id: str, callable_target: ISymbol) -> ISymbol:
        if not isinstance(callable_target, Callable):
            # verify if it is a builtin method with its name shadowed
            call_target = Builtin.get_symbol(callable_id)
            if not isinstance(call_target, Callable) and self.is_exception(callable_id):
                call_target = Builtin.Exception

            callable_target = call_target if call_target is not None else callable_target
        return callable_target

    def validate_callable_arguments(self, call: ast.Call, callable_target: Callable) -> bool:
        if (callable_target.allow_starred_argument
                and not hasattr(call, 'checked_starred_args')
                and len(call.args) > len(callable_target.args_without_default)):
            args = self.parse_to_node(str(Type.sequence.default_value), call)
            args.elts = call.args
            call.args = [args]
            call.checked_starred_args = True

        len_call_args = len(call.args)
        callable_required_args = len(callable_target.args_without_default)

        if len_call_args > len(callable_target.args):
            unexpected_arg = call.args[len(callable_target.args)]
            self._log_error(
                CompilerError.UnexpectedArgument(unexpected_arg.lineno, unexpected_arg.col_offset)
            )
            return False
        elif len_call_args < callable_required_args:
            missed_arg = list(callable_target.args)[len(call.args)]
            self._log_error(
                CompilerError.UnfilledArgument(call.lineno, call.col_offset, missed_arg)
            )
            return False

        if isinstance(callable_target, IBuiltinMethod) and callable_target.requires_reordering:
            if not hasattr(call, 'was_reordered') or not call.was_reordered:
                callable_target.reorder(call.args)
                call.was_reordered = True

        if callable_required_args <= len_call_args < len(callable_target.args):
            included_args = len_call_args - callable_required_args
            for default in callable_target.defaults[included_args:]:
                call.args.append(self.clone(default))
        return True

    def validate_passed_arguments(self, call: ast.Call, args_types: List[IType], callable_id: str, callable: Callable):
        if isinstance(callable, IBuiltinMethod):
            builtin_analyser = BuiltinFunctionCallAnalyser(self, call, callable_id, callable, self._log)
            if builtin_analyser.validate():
                self.errors.extend(builtin_analyser.errors)
                self.warnings.extend(builtin_analyser.warnings)
                return

        for index, (arg_id, arg_value) in enumerate(callable.args.items()):
            param = call.args[index]
            param_type = self.get_type(param, use_metatype=True)
            args_types.append(param_type)
            if not arg_value.type.is_type_of(param_type):
                self._log_error(
                    CompilerError.MismatchedTypes(
                        param.lineno, param.col_offset,
                        arg_value.type.identifier,
                        param_type.identifier
                    ))

    def update_callable_after_validation(self, call: ast.Call, callable_id: str, callable_target: Callable):
        # if the arguments are not generic, include the specified method in the symbol table
        if (isinstance(callable_target, IBuiltinMethod)
                and callable_target.identifier != callable_id
                and callable_target.raw_identifier == callable_id):
            if callable_target.identifier not in self.symbols:
                self.symbols[callable_target.identifier] = callable_target
            call.func = ast.Name(lineno=call.func.lineno, col_offset=call.func.col_offset,
                                 ctx=ast.Load(), id=callable_target.identifier)

    def visit_Raise(self, raise_node: ast.Raise):
        """
        Visitor of the raise node

        Verifies if the raised object is a exception

        :param raise_node: the python ast raise node
        """
        raised = self.visit(raise_node.exc)
        raised_type: IType = self.get_type(raised)
        if raised_type is not Type.exception:
            self._log_error(
                CompilerError.MismatchedTypes(
                    raise_node.lineno, raise_node.col_offset,
                    actual_type_id=raised_type.identifier,
                    expected_type_id=Type.exception.identifier
                ))

    def visit_Try(self, try_node: ast.Try):
        """
        Visitor of the try node

        :param try_node: the python ast try node
        """
        self.validate_except_handlers(try_node)

        for stmt in try_node.body:
            self.visit(stmt)

        for exception_handler in try_node.handlers:
            self.visit(exception_handler)

        for stmt in try_node.finalbody:
            self.visit(stmt)

    def validate_except_handlers(self, try_node: ast.Try):
        if len(try_node.handlers) > 1:
            exception_handlers: List[ast.ExceptHandler] = try_node.handlers.copy()
            general_exc_handler: ast.ExceptHandler = next(
                (handler
                 for handler in exception_handlers
                 if (handler.type is None or  # no specified exception or is BaseException
                     (isinstance(handler.type, ast.Name) and handler.type.id == BaseException.__name__)
                     )
                 ), exception_handlers[0]
            )

            try_node.handlers = [general_exc_handler]
            exception_handlers.remove(general_exc_handler)

            for handler in exception_handlers:
                warnings = len(self.warnings)
                self.visit(handler)
                if warnings == len(self.warnings):
                    self._log_using_specific_exception_warning(handler.type)

        if len(try_node.handlers) == 1:
            self.visit(try_node.handlers[0])

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        """
        Visitor of the try except node

        :param node: the python ast try except node
        """
        logged_errors = False

        exception_type: IType = self.get_type(node.type)
        if node.type is not None and exception_type is not Type.exception:
            self._log_error(
                CompilerError.MismatchedTypes(line=node.type.lineno,
                                              col=node.type.col_offset,
                                              expected_type_id=Type.exception.identifier,
                                              actual_type_id=exception_type.identifier)
            )
            logged_errors = True

        if node.name is not None:
            # TODO: remove when getting the exception is implemented
            self._log_error(
                CompilerError.NotSupportedOperation(line=node.lineno,
                                                    col=node.col_offset,
                                                    symbol_id='naming exceptions')
            )
            logged_errors = True

        if not logged_errors and node.type is not None:
            self._log_using_specific_exception_warning(node.type)

        self.generic_visit(node)

    def _log_using_specific_exception_warning(self, node: ast.AST):
        if node is None:
            exc_id = 'Exception'
        elif isinstance(node, ast.Name):
            exc_id = node.id
        else:
            exc_id = self.get_type(node).identifier

        self._log_warning(
            CompilerWarning.UsingSpecificException(line=node.lineno,
                                                   col=node.col_offset,
                                                   exception_id=exc_id)
        )

    def visit_value(self, node: ast.AST):
        result = self.visit(node)

        if isinstance(node, ast.Attribute):
            if isinstance(result, str):
                return self.get_symbol(result)
            else:
                origin, value, attribute = result.values
                if value is None and isinstance(origin, ast.Name):
                    value = self.get_symbol(origin.id)
                if value is not None:
                    return value

        return result

    def visit_Attribute(self, attribute: ast.Attribute) -> Union[str, Attribute]:
        """
        Gets the attribute inside the ast node

        :param attribute: the python ast attribute node
        :return: returns the type of the value, the attribute symbol and its id if the attribute exists.
                 Otherwise, returns None
        """
        is_internal = hasattr(attribute, 'is_internal_call') and attribute.is_internal_call
        value: Optional[Union[str, ISymbol]] = self.get_symbol(attribute.value.id, is_internal) \
            if isinstance(attribute.value, ast.Name) else self.visit(attribute.value)

        if value is None and isinstance(attribute.value, ast.Name):
            return '{0}.{1}'.format(attribute.value.id, attribute.attr)

        symbol = None
        if isinstance(value, str) and not isinstance(attribute.value, ast.Str):
            symbol = self.get_symbol(value)
            if symbol is None:
                return '{0}.{1}'.format(value, attribute.attr)
        if isinstance(value, ISymbol):
            symbol = value

        if isinstance(symbol, IExpression):
            symbol = symbol.type
        if hasattr(symbol, 'symbols') and attribute.attr in symbol.symbols:
            attr_symbol = symbol.symbols[attribute.attr]
        else:
            attr_symbol: Optional[ISymbol] = self.get_symbol(attribute.attr)

        if attr_symbol is None and hasattr(symbol, 'symbols'):
            # if it couldn't find the symbol in the attribute symbols, raise unresolved reference
            self._log_error(
                CompilerError.UnresolvedReference(
                    attribute.lineno, attribute.col_offset,
                    symbol_id='{0}.{1}'.format(symbol.identifier, attribute.attr)
                ))
            return Attribute(attribute.value, None, attr_symbol, attribute)

        attr_type = value.type if isinstance(value, IExpression) else value
        # for checking during the code generation
        if (isinstance(attr_type, ClassType) and
                not (isinstance(attribute.value, ast.Name) and attribute.value.id == attr_type.identifier) and
                (not hasattr(attribute, 'generate_value') or not attribute.generate_value)):
            attribute.generate_value = True

        return Attribute(attribute.value, attribute.attr, attr_symbol, attribute)

    def visit_Constant(self, constant: ast.Constant) -> Any:
        """
        Visitor of constant values node

        :param constant: the python ast constant value node
        :return: the value of the constant
        """
        if isinstance(constant, ast.Num) and not isinstance(constant.value, int):
            # only integer numbers are allowed
            self._log_error(
                CompilerError.InvalidType(constant.lineno, constant.col_offset, symbol_id=type(constant.value).__name__)
            )
        return constant.value

    def visit_Num(self, num: ast.Num) -> int:
        """
        Verifies if the number is an integer

        :param num: the python ast number node
        :return: returns the value of the number
        """
        if not isinstance(num.n, int):
            # only integer numbers are allowed
            self._log_error(
                CompilerError.InvalidType(num.lineno, num.col_offset, symbol_id=type(num.n).__name__)
            )
        return num.n

    def visit_Str(self, string: ast.Str) -> str:
        """
        Visitor of literal string node

        :param string: the python ast string node
        :return: the value of the string
        """
        return string.s

    def visit_Bytes(self, bts: ast.Bytes) -> bytes:
        """
        Visitor of literal bytes node

        :param bts: the python ast bytes node
        :return: the value of the bytes
        """
        return bts.s

    def visit_Tuple(self, tup_node: ast.Tuple) -> Tuple[Any, ...]:
        """
        Visitor of literal tuple node

        :param tup_node: the python ast tuple node
        :return: the value of the tuple
        """
        return tuple(self.get_type(value) for value in tup_node.elts)

    def visit_List(self, list_node: ast.List) -> List[Any]:
        """
        Visitor of literal list node

        :param list_node: the python ast list node
        :return: the value of the list
        """
        return [self.get_type(value) for value in list_node.elts]

    def visit_Dict(self, dict_node: ast.Dict) -> Dict[Any, Any]:
        """
        Visitor of literal dict node

        :param dict_node: the python ast dict node
        :return: a list with each key and value type
        """
        dictionary = {}
        size = min(len(dict_node.keys), len(dict_node.values))
        for index in range(size):
            key = self.get_type(dict_node.keys[index])
            value = self.get_type(dict_node.values[index])
            if key in dictionary and dictionary[key] != value:
                dictionary[key] = Type.get_generic_type(dictionary[key], value)
            else:
                dictionary[key] = value
        return dictionary

    def visit_NameConstant(self, constant: ast.NameConstant) -> Any:
        """
        Visitor of constant names node

        :param constant: the python ast name constant node
        :return: the value of the constant
        """
        return constant.value

    def visit_Name(self, name: ast.Name) -> ast.Name:
        """
        Visitor of a name node

        :param name:
        :return: the object with the name node information
        """
        return name

    def visit_Index(self, index: ast.Index) -> Any:
        """
        Visitor of an index node

        :param index:
        :return: the object with the index value information
        """
        index = self.visit(index.value)
        if isinstance(index, (Iterable, Tuple)):
            return tuple(index)
        return index

    def visit_Slice(self, slice_node: ast.Slice) -> Tuple[Any, Any, Any]:
        """
        Visitor of an slice node

        :param slice_node:
        :return: the object with the index value information
        """
        return slice_node.lower, slice_node.upper, slice_node.step
