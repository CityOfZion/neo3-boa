import ast
from inspect import isclass
from typing import Dict, List, Optional, Tuple

from boa3.analyser.astanalyser import IAstAnalyser
from boa3.compiler.codegenerator.codegenerator import CodeGenerator
from boa3.compiler.codegenerator.vmcodemapping import VMCodeMapping
from boa3.model.builtin.builtin import Builtin
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.binaryop import BinaryOp
from boa3.model.operation.operation import IOperation
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.type.classtype import ClassType
from boa3.model.type.type import IType, Type
from boa3.model.variable import Variable


class VisitorCodeGenerator(IAstAnalyser):
    """
    This class is responsible for walk through the ast.

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    :ivar generator:
    """

    def __init__(self, generator: CodeGenerator):
        super().__init__(ast.parse(""), log=True)
        self.generator = generator
        self.current_method: Optional[Method] = None
        self.symbols = generator.symbol_table

    def include_instruction(self, node: ast.AST, address: int):
        if self.current_method is not None and address in VMCodeMapping.instance().code_map:
            bytecode = VMCodeMapping.instance().code_map[address]
            from boa3.model.debuginstruction import DebugInstruction
            self.current_method.include_instruction(DebugInstruction.build(node, bytecode))

    def visit_to_map(self, node: ast.AST, generate: bool = False):
        address: int = VMCodeMapping.instance().bytecode_size
        if isinstance(node, ast.Expr):
            value = self.visit_Expr(node, generate)
        elif generate:
            value = self.visit_to_generate(node)
        else:
            value = self.visit(node)

        if not isinstance(node, (ast.For, ast.While, ast.If)):
            # control flow nodes must map each of their instructions
            self.include_instruction(node, address)
        return value

    def visit_to_generate(self, node):
        """
        Visitor to generate the nodes that the primary visitor is used to retrieve value

        :param node: an ast node
        """
        if isinstance(node, ast.AST):
            result = self.visit(node)
            # the default return of the name visitor is the name string
            if isinstance(result, str):
                if self.is_exception_name(result):
                    self.generator.convert_new_exception()
                else:
                    # TODO: validate function calls
                    is_internal = hasattr(node, 'is_internal_call') and node.is_internal_call
                    self.generator.convert_load_symbol(result, is_internal=is_internal)
            return result
        else:
            return self.generator.convert_literal(node)

    def is_exception_name(self, exc_id: str) -> bool:
        global_symbols = globals()
        if exc_id in global_symbols or exc_id in global_symbols['__builtins__']:
            symbol = (global_symbols[exc_id]
                      if exc_id in global_symbols
                      else global_symbols['__builtins__'][exc_id])
            if isclass(symbol) and issubclass(symbol, BaseException):
                return True
        return False

    def visit_Module(self, module: ast.Module):
        """
        Visitor of the module node

        Fills module symbol table

        :param module:
        """
        global_stmts = [node for node in module.body if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        function_stmts = module.body[len(global_stmts):]

        for stmt in function_stmts:
            self.visit(stmt)

        if self.generator.initialize_static_fields():
            for stmt in global_stmts:
                self.visit(stmt)

            self.generator.end_initialize()

    def visit_ImportFrom(self, import_from: ast.ImportFrom):
        """
        Includes methods and variables from other modules into the current scope

        :param import_from:
        """
        self._import_static_fields(import_from.names)

    def visit_Import(self, import_node: ast.Import):
        """
        Includes methods and variables from other modules into the current scope

        :param import_node:
        """
        self._import_static_fields(import_node.names)

    def _import_static_fields(self, names: List[ast.alias]):
        """
        Visits the imported nodes that aren't function definitions to initialize static fields

        :param names: list of imported alias
        """
        for alias in names:
            name = alias.asname if alias.asname is not None else alias.name
            if name in self.symbols:
                if hasattr(self.symbols[name], 'ast') and self.symbols[name].ast is not None:
                    ast_root = self.symbols[name].ast
                elif hasattr(self.symbols[name], 'origin') and self.symbols[name].origin is not None:
                    ast_root = self.symbols[name].origin
                else:
                    continue

                if isinstance(ast_root, ast.Module):
                    body = ast_root.body
                else:
                    body = [ast_root]

                for node in body:
                    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.visit(node)

    def visit_FunctionDef(self, function: ast.FunctionDef):
        """
        Visitor of the function definition node

        Generates the Neo VM code for the function

        :param function: the python ast function definition node
        """
        method = self.symbols[function.name]
        if isinstance(method, Method):
            self.current_method = method
            self.generator.convert_begin_method(method)

            for stmt in function.body:
                self.visit_to_map(stmt)

            self.generator.convert_end_method(function.name)
            self.current_method = None

    def visit_arguments(self, arguments: ast.arguments) -> Dict[str, Variable]:
        """
        Visitor of the function arguments node

        :param arguments: the python ast function arguments node
        :return: a dictionary that maps each argument to its identifier
        """
        args: Dict[str, Variable] = {}

        for arg in arguments.args:
            var_id, var = self.visit_arg(arg)   # type:str, Variable
            args[var_id] = var
        return args

    def visit_arg(self, arg: ast.arg) -> Tuple[str, Variable]:
        """
        Visitor of a function argument node

        :param arg: the python ast arg node
        :return: a tuple with the identifier and the argument
        """
        var_id = arg.arg
        var_type = self.visit(arg.annotation)

        return var_id, Variable(var_type)

    def visit_Return(self, ret: ast.Return):
        """
        Visitor of a function return node

        :param ret: the python ast return node
        """
        if self.generator.stack_size > 0:
            self.generator.clear_stack(True)
        if self.current_method.return_type is not Type.none:
            result = self.visit_to_generate(ret.value)
            if result is Type.none and not self.generator.is_none_inserted():
                self.generator.convert_literal(None)
        self.generator.insert_return()

    def store_variable(self, *var_ids: Tuple[str, Optional[ast.AST]], value: ast.AST):
        # if the value is None, it is a variable declaration
        if value is not None:
            if len(var_ids) == 1:
                # it's a simple assignment
                var_id, index = var_ids[0]
                if index is None:
                    # if index is None, then it is a variable assignment
                    result_type = self.visit_to_generate(value)

                    if result_type is Type.none and not self.generator.is_none_inserted():
                        self.generator.convert_literal(None)
                    self.generator.convert_store_variable(var_id)
                else:
                    # if not, it is an array assignment
                    self.generator.convert_load_symbol(var_id)
                    self.visit_to_generate(index)

                    aux_index = VMCodeMapping.instance().bytecode_size
                    value_address = self.visit_to_generate(value)
                    if isinstance(value, ast.Name):
                        value_address = aux_index

                    self.generator.convert_set_item(value_address)

            elif len(var_ids) > 0:
                # it's a chained assignment
                self.visit_to_generate(value)
                for pos, (var_id, index) in enumerate(reversed(var_ids)):
                    if index is None:
                        # if index is None, then it is a variable assignment
                        if pos < len(var_ids) - 1:
                            self.generator.duplicate_stack_top_item()
                        self.generator.convert_store_variable(var_id)
                    else:
                        # if not, it is an array assignment
                        if pos < len(var_ids) - 1:
                            self.generator.convert_load_symbol(var_id)
                            self.visit_to_generate(index)
                            fix_index = VMCodeMapping.instance().bytecode_size
                            self.generator.duplicate_stack_item(3)
                        else:
                            self.visit_to_generate(index)
                            fix_index = VMCodeMapping.instance().bytecode_size
                            self.generator.convert_load_symbol(var_id)
                            self.generator.swap_reverse_stack_items(3)
                        self.generator.convert_set_item(fix_index)

    def visit_AnnAssign(self, ann_assign: ast.AnnAssign):
        """
        Visitor of an annotated assignment node

        :param ann_assign: the python ast variable assignment node
        """
        var_id = self.visit(ann_assign.target)
        self.store_variable((var_id, None), value=ann_assign.value)

    def visit_Assign(self, assign: ast.Assign):
        """
        Visitor of an assignment node

        :param assign: the python ast variable assignment node
        """
        vars_ids: List[Tuple[str, Optional[ast.AST]]] = []
        for target in assign.targets:
            var_index = None
            var_id = self.visit(target)

            # if it is a tuple, then it is an array assignment
            if isinstance(var_id, tuple):
                var_index = var_id[1]
                var_id: str = var_id[0]

            vars_ids.append((var_id, var_index))

        self.store_variable(*vars_ids, value=assign.value)

    def visit_AugAssign(self, aug_assign: ast.AugAssign):
        """
        Visitor of an augmented assignment node

        :param aug_assign: the python ast augmented assignment node
        """
        var_id = self.visit(aug_assign.target)
        self.generator.convert_load_symbol(var_id)
        self.visit_to_generate(aug_assign.value)
        self.generator.convert_operation(aug_assign.op)
        self.generator.convert_store_variable(var_id)

    def visit_Subscript(self, subscript: ast.Subscript):
        """
        Visitor of a subscript node

        :param subscript: the python ast subscript node
        """
        if isinstance(subscript.slice, ast.Slice):
            return self.visit_Subscript_Slice(subscript)

        return self.visit_Subscript_Index(subscript)

    def visit_Subscript_Index(self, subscript: ast.Subscript):
        """
        Visitor of a subscript node with index

        :param subscript: the python ast subscript node
        """
        if isinstance(subscript.ctx, ast.Load):
            # get item
            self.visit_to_generate(subscript.value)
            value = subscript.slice.value if isinstance(subscript.slice, ast.Index) else subscript.slice
            self.visit_to_generate(value)
            self.generator.convert_get_item()
        else:
            # set item
            var_id = self.visit(subscript.value)
            return var_id, subscript.slice.value

    def visit_Subscript_Slice(self, subscript: ast.Subscript):
        """
        Visitor of a subscript node with slice

        :param subscript: the python ast subscript node
        """
        lower_omitted = subscript.slice.lower is None
        upper_omitted = subscript.slice.upper is None

        self.visit_to_generate(subscript.value)
        # if both are explicit
        if not lower_omitted and not upper_omitted:
            addresses = [VMCodeMapping.instance().bytecode_size]
            self.visit_to_generate(subscript.slice.lower)

            # length of slice
            addresses.append(VMCodeMapping.instance().bytecode_size)
            self.visit_to_generate(subscript.slice.upper)

            self.generator.convert_get_sub_array(addresses)
        # only one of them is omitted
        elif lower_omitted != upper_omitted:
            # end position is omitted
            if lower_omitted:
                self.visit_to_generate(subscript.slice.upper)
                self.generator.convert_get_array_beginning()
            # start position is omitted
            else:
                self.generator.duplicate_stack_top_item()
                # length of slice
                self.generator.convert_builtin_method_call(Builtin.Len)
                self.visit_to_generate(subscript.slice.lower)
                self.generator.convert_get_array_ending()
        else:
            self.generator.convert_copy()

    def _convert_unary_operation(self, operand, op):
        self.visit_to_generate(operand)
        self.generator.convert_operation(op)

    def _convert_binary_operation(self, left, right, op):
        self.visit_to_generate(left)
        self.visit_to_generate(right)
        self.generator.convert_operation(op)

    def visit_BinOp(self, bin_op: ast.BinOp):
        """
        Visitor of a binary operation node

        :param bin_op: the python ast binary operation node
        """
        if isinstance(bin_op.op, BinaryOperation):
            self._convert_binary_operation(bin_op.left, bin_op.right, bin_op.op)

    def visit_UnaryOp(self, un_op: ast.UnaryOp):
        """
        Visitor of a binary operation node

        :param un_op: the python ast binary operation node
        """
        if isinstance(un_op.op, UnaryOperation):
            self._convert_unary_operation(un_op.operand, un_op.op)

    def visit_Compare(self, compare: ast.Compare):
        """
        Visitor of a compare operation node

        :param compare: the python ast compare operation node
        """
        converted: bool = False
        left = compare.left
        for index, op in enumerate(compare.ops):
            right = compare.comparators[index]
            if isinstance(op, IOperation):
                if isinstance(op, BinaryOperation):
                    self._convert_binary_operation(left, right, op)
                else:
                    operand = left
                    if isinstance(operand, ast.NameConstant) and operand.value is None:
                        operand = right
                    self._convert_unary_operation(operand, op)
                # if it's more than two comparators, must include AND between the operations
                if not converted:
                    converted = True
                else:
                    self.generator.convert_operation(BinaryOp.And)
            left = right

    def visit_BoolOp(self, bool_op: ast.BoolOp):
        """
        Visitor of a compare operation node

        :param bool_op: the python ast boolean operation node
        """
        if isinstance(bool_op.op, BinaryOperation):
            left = bool_op.values[0]
            self.visit_to_generate(left)
            for index, right in enumerate(bool_op.values[1:]):
                self.visit_to_generate(right)
                self.generator.convert_operation(bool_op.op)

    def visit_While(self, while_node: ast.While):
        """
        Visitor of a while statement node

        :param while_node: the python ast while statement node
        """
        start_addr: int = self.generator.convert_begin_while()
        for stmt in while_node.body:
            self.visit_to_map(stmt, generate=True)

        test_address: int = VMCodeMapping.instance().bytecode_size
        self.visit_to_map(while_node.test, generate=True)
        self.generator.convert_end_while(start_addr, test_address)

        else_begin_address: int = self.generator.last_code_start_address
        for stmt in while_node.orelse:
            self.visit_to_map(stmt, generate=True)

        self.generator.convert_end_loop_else(start_addr, else_begin_address, len(while_node.orelse) > 0)

    def visit_For(self, for_node: ast.For):
        """
        Visitor of for statement node

        :param for_node: the python ast for node
        """
        self.visit_to_generate(for_node.iter)
        start_address = self.generator.convert_begin_for()

        if isinstance(for_node.target, tuple):
            for target in for_node.target:
                var_id = self.visit_to_map(target)
                self.generator.convert_store_variable(var_id)
        else:
            var_id = self.visit(for_node.target)
            self.generator.convert_store_variable(var_id)

        for stmt in for_node.body:
            self.visit_to_map(stmt, generate=True)

        # TODO: remove when optimizing for generation
        if self.current_method is not None:
            self.current_method.remove_instruction(for_node.lineno, for_node.col_offset)

        condition_address = self.generator.convert_end_for(start_address)
        self.include_instruction(for_node, condition_address)
        else_begin = self.generator.last_code_start_address

        for stmt in for_node.orelse:
            self.visit_to_map(stmt, generate=True)

        self.generator.convert_end_loop_else(start_address,
                                             else_begin,
                                             has_else=len(for_node.orelse) > 0,
                                             is_for=True)

    def visit_If(self, if_node: ast.If):
        """
        Visitor of if statement node

        :param if_node: the python ast if statement node
        """
        self.visit_to_map(if_node.test, generate=True)

        start_addr: int = self.generator.convert_begin_if()
        for stmt in if_node.body:
            self.visit_to_map(stmt, generate=True)

        ends_with_if = len(if_node.body) > 0 and isinstance(if_node.body[-1], ast.If)

        if len(if_node.orelse) > 0:
            start_addr = self.generator.convert_begin_else(start_addr, ends_with_if)
            for stmt in if_node.orelse:
                self.visit_to_map(stmt, generate=True)

        self.generator.convert_end_if(start_addr)

    def visit_Expr(self, expr: ast.Expr, generate: bool = False):
        """
        Visitor of an expression node

        :param expr: the python ast expression node
        :param generate: if it should convert the value
        """
        last_stack = self.generator.stack_size
        if generate:
            value = self.visit_to_generate(expr.value)
        else:
            value = self.visit(expr.value)

        new_stack = self.generator.stack_size
        for x in range(last_stack, new_stack):
            self.generator.remove_stack_top_item()

        return value

    def visit_IfExp(self, if_node: ast.IfExp):
        """
        Visitor of if expression node

        :param if_node: the python ast if statement node
        """
        self.visit_to_map(if_node.test, generate=True)

        start_addr: int = self.generator.convert_begin_if()
        self.visit_to_map(if_node.body, generate=True)

        start_addr = self.generator.convert_begin_else(start_addr)
        self.visit_to_map(if_node.orelse, generate=True)

        self.generator.convert_end_if(start_addr)

    def visit_Assert(self, assert_node: ast.Assert):
        """
        Visitor of the assert node

        :param assert_node: the python ast assert node
        """
        self.visit_to_generate(assert_node.test)
        self.generator.convert_assert()

    def visit_Call(self, call: ast.Call) -> IType:
        """
        Visitor of a function call node

        :param call: the python ast function call node
        :returns: The called function return type
        """
        # the parameters are included into the stack in the reversed order
        last_address = VMCodeMapping.instance().bytecode_size
        last_stack = self.generator.stack_size

        function_id = self.visit(call.func)
        if not isinstance(function_id, str):
            if not isinstance(function_id, tuple) or len(function_id) != 2:
                return Type.none

            class_type, identifier = function_id
            if (isinstance(class_type, ClassType) and identifier in class_type.symbols
                    and isinstance(class_type.symbols[identifier], IExpression)):
                symbol = class_type.symbols[identifier]
                function_id = identifier
            else:
                return Type.none
        else:
            is_internal = hasattr(call, 'is_internal_call') and call.is_internal_call
            symbol = self.generator.get_symbol(function_id, is_internal=is_internal)

        if isinstance(symbol, ClassType):
            symbol = symbol.constructor_method()
        args_addresses: List[int] = []

        if VMCodeMapping.instance().bytecode_size > last_address:
            # remove opcodes inserted during the evaluation of the symbol
            VMCodeMapping.instance().remove_opcodes(last_address, VMCodeMapping.instance().bytecode_size)
        if last_stack < self.generator.stack_size:
            # remove any additional values pushed to the stack during the evalution of the symbol
            for _ in range(self.generator.stack_size - last_stack):
                self.generator._stack_pop()

        if isinstance(symbol, Method):
            args_to_generate = [arg for index, arg in enumerate(call.args) if index in symbol.args_to_be_generated()]
        else:
            args_to_generate = call.args

        if isinstance(symbol, IBuiltinMethod):
            reordered_args = []
            for index in symbol.generation_order:
                if 0 <= index < len(args_to_generate):
                    reordered_args.append(args_to_generate[index])

            args = reordered_args
        else:
            args = reversed(args_to_generate)

        for arg in args:
            args_addresses.append(
                VMCodeMapping.instance().bytecode_size
            )
            self.visit_to_generate(arg)

        if self.is_exception_name(function_id):
            self.generator.convert_new_exception(len(call.args))
        elif isinstance(symbol, IBuiltinMethod):
            self.generator.convert_builtin_method_call(symbol, args_addresses)
        else:
            self.generator.convert_load_symbol(function_id, args_addresses)

        return symbol.type if isinstance(symbol, IExpression) else symbol

    def visit_Raise(self, raise_node: ast.Raise):
        """
        Visitor of the raise node

        :param raise_node: the python ast raise node
        """
        self.visit_to_map(raise_node.exc, generate=True)
        self.generator.convert_raise_exception()

    def visit_Try(self, try_node: ast.Try):
        """
        Visitor of the try node

        :param try_node: the python ast try node
        """
        try_address: int = self.generator.convert_begin_try()
        try_end: Optional[int] = None
        for stmt in try_node.body:
            self.visit_to_map(stmt, generate=True)

        if len(try_node.handlers) == 1:
            handler = try_node.handlers[0]
            try_end = self.generator.convert_try_except(handler.name)
            for stmt in handler.body:
                self.visit_to_map(stmt, generate=True)

        except_end = self.generator.convert_end_try(try_address, try_end)
        for stmt in try_node.finalbody:
            self.visit_to_map(stmt, generate=True)
        self.generator.convert_end_try_finally(except_end, try_address, len(try_node.finalbody) > 0)

    def visit_Name(self, name: ast.Name) -> str:
        """
        Visitor of a name node

        :param name: the python ast name identifier node
        :return: the identifier of the name
        """
        return name.id

    def visit_Attribute(self, attribute: ast.Attribute) -> str:
        """
        Visitor of a attribute node

        :param attribute: the python ast attribute node
        :return: the identifier of the attribute
        """
        if self.generator.get_symbol(attribute.attr) is not Type.none and not hasattr(attribute, 'generate_value'):
            return attribute.attr

        value = attribute.value
        if isinstance(value, ast.Attribute):
            value = self.visit(value)
        elif hasattr(attribute, 'generate_value') and attribute.generate_value:
            result = self.visit_to_generate(attribute.value)
            if isinstance(result, str):
                x = self.generator.get_symbol(result)
                result = x.type if isinstance(x, IExpression) else x
            if isinstance(result, ClassType):
                index = self.generator.convert_class_symbol(result, attribute.attr, isinstance(attribute.ctx, ast.Load))
                return result, index

        if isinstance(value, (ast.Name, str)):
            value_id = value.id if isinstance(value, ast.Name) else value
            return '{0}.{1}'.format(value_id, attribute.attr)

        return attribute.attr

    def visit_Continue(self, continue_node: ast.Continue):
        """
        :param continue_node: the python ast continue statement node
        """
        self.generator.convert_loop_continue()

    def visit_Break(self, break_node: ast.Break):
        """
        :param break_node: the python ast break statement node
        """
        self.generator.convert_loop_break()

    def visit_Constant(self, constant: ast.Constant):
        """
        Visitor of constant values node

        :param constant: the python ast constant value node
        """
        return self.generator.convert_literal(constant.value)

    def visit_NameConstant(self, constant: ast.NameConstant):
        """
        Visitor of constant names node

        :param constant: the python ast name constant node
        """
        return self.generator.convert_literal(constant.value)

    def visit_Num(self, num: ast.Num):
        """
        Visitor of literal number node

        :param num: the python ast number node
        """
        return self.generator.convert_literal(num.n)

    def visit_Str(self, string: ast.Str):
        """
        Visitor of literal string node

        :param string: the python ast string node
        """
        return self.generator.convert_literal(string.s)

    def visit_Bytes(self, bts: ast.Bytes):
        """
        Visitor of literal bytes node

        :param bts: the python ast bytes node
        """
        return self.generator.convert_literal(bts.s)

    def visit_Tuple(self, tup_node: ast.Tuple):
        """
        Visitor of literal tuple node

        :param tup_node: the python ast tuple node
        """
        self._create_array(tup_node.elts, Type.tuple)

    def visit_List(self, list_node: ast.List):
        """
        Visitor of literal list node

        :param list_node: the python ast list node
        """
        self._create_array(list_node.elts, Type.list)

    def visit_Dict(self, dict_node: ast.Dict):
        """
        Visitor of literal dict node

        :param dict_node: the python ast dict node
        """
        length = min(len(dict_node.keys), len(dict_node.values))
        self.generator.convert_new_map(Type.dict)
        for key_value in range(length):
            self.generator.duplicate_stack_top_item()
            self.visit_to_generate(dict_node.keys[key_value])
            value_address = self.visit_to_generate(dict_node.values[key_value])
            self.generator.convert_set_item(value_address)

    def _create_array(self, values: List[ast.AST], array_type: IType):
        """
        Creates a new array from a literal sequence

        :param values: list of values of the new array items
        """
        length = len(values)
        if length > 0:
            for value in reversed(values):
                self.visit_to_generate(value)
        self.generator.convert_new_array(length, array_type)
