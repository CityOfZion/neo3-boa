import ast
import os.path
from inspect import isclass
from typing import Dict, List, Optional, Tuple

from boa3 import constants
from boa3.analyser.astanalyser import IAstAnalyser
from boa3.compiler.codegenerator.codegenerator import CodeGenerator
from boa3.compiler.codegenerator.generatordata import GeneratorData
from boa3.compiler.codegenerator.vmcodemapping import VMCodeMapping
from boa3.constants import SYS_VERSION_INFO
from boa3.model.builtin.builtin import Builtin
from boa3.model.builtin.interop.interop import Interop
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.imports.package import Package
from boa3.model.method import Method
from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.binaryop import BinaryOp
from boa3.model.operation.operation import IOperation
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.property import Property
from boa3.model.symbol import ISymbol
from boa3.model.type.classes.classtype import ClassType
from boa3.model.type.classes.userclass import UserClass
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.type import IType, Type
from boa3.model.variable import Variable


class VisitorCodeGenerator(IAstAnalyser):
    """
    This class is responsible for walk through the ast.

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    :ivar generator:
    """

    def __init__(self, generator: CodeGenerator, filename: str = None):
        super().__init__(ast.parse(""), filename=filename, log=True)

        self.generator = generator
        self.current_method: Optional[Method] = None
        self.current_class: Optional[UserClass] = None
        self.symbols = generator.symbol_table

        self.global_stmts: List[ast.AST] = []
        self._is_generating_initialize = False
        self._root_module: ast.AST = self._tree

    @property
    def _symbols(self) -> Dict[str, ISymbol]:
        symbol_table = self.symbols.copy()

        if isinstance(self.current_class, UserClass):
            symbol_table.update(self.current_class.symbols)

        return symbol_table

    def include_instruction(self, node: ast.AST, address: int):
        if self.current_method is not None and address in VMCodeMapping.instance().code_map:
            bytecode = VMCodeMapping.instance().code_map[address]
            from boa3.model.debuginstruction import DebugInstruction
            self.current_method.include_instruction(DebugInstruction.build(node, bytecode))

    def build_data(self, origin_node: Optional[ast.AST],
                   symbol_id: Optional[str] = None,
                   symbol: Optional[ISymbol] = None,
                   result_type: Optional[IType] = None,
                   index: Optional[int] = None,
                   already_generated: bool = False) -> GeneratorData:

        if isinstance(symbol, IType) and result_type is None:
            result_type = symbol
            symbol = None

        if symbol is None and symbol_id is not None:
            # try to find the symbol if the id is known
            if symbol_id in self._symbols:
                found_symbol = self._symbols[symbol_id]
            else:
                _, found_symbol = self.generator.get_symbol(symbol_id)
                if found_symbol is Type.none:
                    # generator get_symbol returns Type.none if the symbol is not found
                    found_symbol = None

            if found_symbol is not None:
                symbol = found_symbol

        return GeneratorData(origin_node, symbol_id, symbol, result_type, index, already_generated)

    def visit(self, node: ast.AST) -> GeneratorData:
        result = super().visit(node)
        if not isinstance(result, GeneratorData):
            result = self.build_data(node)
        return result

    def visit_to_map(self, node: ast.AST, generate: bool = False) -> GeneratorData:
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

    def visit_to_generate(self, node) -> GeneratorData:
        """
        Visitor to generate the nodes that the primary visitor is used to retrieve value

        :param node: an ast node
        """
        if isinstance(node, ast.AST):
            result = self.visit(node)

            if not result.already_generated and result.symbol_id is not None:
                if self.is_exception_name(result.symbol_id):
                    self.generator.convert_new_exception()
                else:
                    # TODO: validate function calls
                    is_internal = hasattr(node, 'is_internal_call') and node.is_internal_call
                    class_type = result.type

                    if (self.is_implemented_class_type(result.type)
                            and len(result.symbol_id.split(constants.ATTRIBUTE_NAME_SEPARATOR)) > 1):
                        # if the symbol id has the attribute separator and the top item on the stack is a user class,
                        # then this value is an attribute from that class
                        # change the id for correct generation
                        result.symbol_id = result.symbol_id.split(constants.ATTRIBUTE_NAME_SEPARATOR)[-1]

                    elif isinstance(result.index, Package):
                        class_type = None

                    self.generator.convert_load_symbol(result.symbol_id, is_internal=is_internal, class_type=class_type)

                result.already_generated = True

            return result
        else:
            index = self.generator.convert_literal(node)
            return self.build_data(node, index=index)

    def is_exception_name(self, exc_id: str) -> bool:
        global_symbols = globals()
        if exc_id in global_symbols or exc_id in global_symbols['__builtins__']:
            symbol = (global_symbols[exc_id]
                      if exc_id in global_symbols
                      else global_symbols['__builtins__'][exc_id])
            if isclass(symbol) and issubclass(symbol, BaseException):
                return True
        return False

    def _remove_inserted_opcodes_since(self, last_address: int, last_stack_size: Optional[int] = None):
        if VMCodeMapping.instance().bytecode_size > last_address:
            # remove opcodes inserted during the evaluation of the symbol
            VMCodeMapping.instance().remove_opcodes(last_address, VMCodeMapping.instance().bytecode_size)

        if isinstance(last_stack_size, int) and last_stack_size < self.generator.stack_size:
            # remove any additional values pushed to the stack during the evalution of the symbol
            for _ in range(self.generator.stack_size - last_stack_size):
                self.generator._stack_pop()

    def _get_unique_name(self, name_id: str, node: ast.AST) -> str:
        return '{0}{2}{1}'.format(node.__hash__(), name_id, constants.VARIABLE_NAME_SEPARATOR)

    def set_filename(self, filename: str):
        if isinstance(filename, str) and os.path.isfile(filename):
            if constants.PATH_SEPARATOR != os.path.sep:
                self.filename = filename.replace(constants.PATH_SEPARATOR, os.path.sep)
            else:
                self.filename = filename

    def visit_Module(self, module: ast.Module) -> GeneratorData:
        """
        Visitor of the module node

        Fills module symbol table

        :param module:
        """
        global_stmts = [node for node in module.body if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        function_stmts = module.body[len(global_stmts):]
        mandatory_global_stmts = []
        for stmt in global_stmts:
            if isinstance(stmt, ast.ClassDef):
                class_symbol = self.get_symbol(stmt.name)
                if isinstance(class_symbol, UserClass) and len(class_symbol.class_variables) > 0:
                    mandatory_global_stmts.append(stmt)
            elif not isinstance(stmt, (ast.Import, ast.ImportFrom)):
                mandatory_global_stmts.append(stmt)

        for stmt in function_stmts:
            self.visit(stmt)

        if self.generator.initialize_static_fields():
            last_symbols = self.symbols  # save to revert in the end and not compromise consequent visits
            class_non_static_stmts = []

            for node in global_stmts.copy():
                if isinstance(node, ast.ClassDef):
                    class_origin_module = None
                    if hasattr(node, 'origin'):
                        class_origin_module = node.origin
                        if (node.origin is not self._root_module
                                and hasattr(node.origin, 'symbols')):
                            # symbols unique to imports are not included in the symbols
                            self.symbols = node.origin.symbols

                    class_variables = []
                    class_functions = []
                    for stmt in node.body:
                        if isinstance(stmt, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                            class_variables.append(stmt)
                        else:
                            class_functions.append(stmt)

                    if len(class_functions) > 0:
                        if class_origin_module is not None and not hasattr(node, 'origin'):
                            node.origin = class_origin_module

                        cls_fun = node
                        if len(class_variables) > 0:
                            cls_var = node
                            cls_fun = self.clone(node)
                            cls_fun.body = class_functions
                            cls_var.body = class_variables
                        else:
                            global_stmts.remove(cls_fun)

                        class_non_static_stmts.append(cls_fun)

            # to generate the 'initialize' method for Neo
            self._log_info(f"Compiling '{constants.INITIALIZE_METHOD_ID}' function")
            self._is_generating_initialize = True
            for stmt in global_stmts:
                cur_tree = self._tree
                cur_filename = self.filename
                if hasattr(stmt, 'origin'):
                    if hasattr(stmt.origin, 'filename'):
                        self.set_filename(stmt.origin.filename)
                    self._tree = stmt.origin

                self.visit(stmt)
                self.filename = cur_filename
                self._tree = cur_tree

            self._is_generating_initialize = False
            self.generator.end_initialize()

            # generate any symbol inside classes that's not variables AFTER generating 'initialize' method
            for stmt in class_non_static_stmts:
                cur_tree = self._tree
                if hasattr(stmt, 'origin'):
                    self._tree = stmt.origin
                self.visit(stmt)
                self._tree = cur_tree

            self.symbols = last_symbols  # revert in the end to not compromise consequent visits
            self.generator.additional_symbols = None

        elif len(function_stmts) > 0 or len(mandatory_global_stmts) > 0:
            # to organize syntax tree nodes from other modules
            for stmt in global_stmts:
                if not hasattr(stmt, 'origin'):
                    stmt.origin = module

            module.symbols = self._symbols
            self.global_stmts.extend(global_stmts)
        else:
            # to generate objects when there are no static variables to generate 'initialize'
            for stmt in global_stmts:
                self.visit(stmt)

        return self.build_data(module)

    def visit_ClassDef(self, node: ast.ClassDef) -> GeneratorData:
        if node.name in self.symbols:
            class_symbol = self.symbols[node.name]
            if isinstance(class_symbol, UserClass):
                self.current_class = class_symbol

            if self._is_generating_initialize:
                address = self.generator.bytecode_size
                self.generator.convert_new_empty_array(len(class_symbol.class_variables), class_symbol)
                self.generator.convert_store_variable(node.name, address)
            else:
                init_method = class_symbol.constructor_method()
                if isinstance(init_method, Method) and init_method.start_address is None:
                    self.generator.generate_implicit_init_user_class(init_method)

        for stmt in node.body:
            self.visit(stmt)

        self.current_class = None
        return self.build_data(node)

    def visit_FunctionDef(self, function: ast.FunctionDef) -> GeneratorData:
        """
        Visitor of the function definition node

        Generates the Neo VM code for the function

        :param function: the python ast function definition node
        """
        method = self._symbols[function.name]

        if isinstance(method, Property):
            method = method.getter

        if isinstance(method, Method):
            self.current_method = method
            if isinstance(self.current_class, ClassType):
                function_name = self.current_class.identifier + constants.ATTRIBUTE_NAME_SEPARATOR + function.name
            else:
                function_name = function.name

            self._log_info(f"Compiling '{function_name}' function")

            if method.is_public or method.is_called:
                if not isinstance(self.current_class, ClassType) or not self.current_class.is_interface:
                    self.generator.convert_begin_method(method)

                    for stmt in function.body:
                        self.visit_to_map(stmt)

                    self.generator.convert_end_method(function.name)

            self.current_method = None

        return self.build_data(function, symbol=method, symbol_id=function.name)

    def visit_Return(self, ret: ast.Return) -> GeneratorData:
        """
        Visitor of a function return node

        :param ret: the python ast return node
        """
        if self.generator.stack_size > 0:
            self.generator.clear_stack(True)
        if self.current_method.return_type is not Type.none:
            result = self.visit_to_generate(ret.value)
            if result.type is Type.none and not self.generator.is_none_inserted():
                self.generator.convert_literal(None)
        self.generator.insert_return()

        return self.build_data(ret)

    def store_variable(self, *var_ids: Tuple[str, Optional[ast.AST], int], value: ast.AST):
        # if the value is None, it is a variable declaration
        if value is not None:
            if len(var_ids) == 1:
                # it's a simple assignment
                var_id, index, address = var_ids[0]
                if index is None:
                    # if index is None, then it is a variable assignment
                    result_data = self.visit_to_generate(value)

                    if result_data.type is Type.none and not self.generator.is_none_inserted():
                        self.generator.convert_literal(None)
                    self.generator.convert_store_variable(var_id, address, self.current_class)
                else:
                    # if not, it is an array assignment
                    self.generator.convert_load_symbol(var_id)
                    self.visit_to_generate(index)

                    aux_index = VMCodeMapping.instance().bytecode_size
                    value_data = self.visit_to_generate(value)
                    value_address = value_data.index if value_data.index is not None else aux_index

                    self.generator.convert_set_item(value_address)

            elif len(var_ids) > 0:
                # it's a chained assignment
                self.visit_to_generate(value)
                for pos, (var_id, index, address) in enumerate(reversed(var_ids)):
                    if index is None:
                        # if index is None, then it is a variable assignment
                        if pos < len(var_ids) - 1:
                            self.generator.duplicate_stack_top_item()
                        self.generator.convert_store_variable(var_id, address)
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

    def visit_AnnAssign(self, ann_assign: ast.AnnAssign) -> GeneratorData:
        """
        Visitor of an annotated assignment node

        :param ann_assign: the python ast variable assignment node
        """
        var_value_address = self.generator.bytecode_size
        var_data = self.visit(ann_assign.target)
        var_id = var_data.symbol_id
        # filter to find the imported variables
        if (var_id not in self.generator.symbol_table
                and hasattr(ann_assign, 'origin')
                and isinstance(ann_assign.origin, ast.AST)):
            var_id = self._get_unique_name(var_id, ann_assign.origin)
        self.store_variable((var_id, None, var_value_address), value=ann_assign.value)
        return self.build_data(ann_assign)

    def visit_Assign(self, assign: ast.Assign) -> GeneratorData:
        """
        Visitor of an assignment node

        :param assign: the python ast variable assignment node
        """
        vars_ids: List[Tuple[str, Optional[ast.AST], int]] = []
        for target in assign.targets:
            var_value_address = self.generator.bytecode_size
            target_data: GeneratorData = self.visit(target)

            var_id = target_data.symbol_id
            var_index = target_data.index

            # filter to find the imported variables
            if (var_id not in self.generator.symbol_table
                    and hasattr(assign, 'origin')
                    and isinstance(assign.origin, ast.AST)):
                var_id = self._get_unique_name(var_id, assign.origin)
            vars_ids.append((var_id, var_index, var_value_address))

        self.store_variable(*vars_ids, value=assign.value)
        return self.build_data(assign)

    def visit_AugAssign(self, aug_assign: ast.AugAssign) -> GeneratorData:
        """
        Visitor of an augmented assignment node

        :param aug_assign: the python ast augmented assignment node
        """
        var_data = self.visit(aug_assign.target)
        var_id = var_data.symbol_id
        # filter to find the imported variables
        if (var_id not in self.generator.symbol_table
                and hasattr(aug_assign, 'origin')
                and isinstance(aug_assign.origin, ast.AST)):
            var_id = self._get_unique_name(var_id, aug_assign.origin)

        if isinstance(var_data.type, UserClass):
            self.generator.duplicate_stack_top_item()

        self.generator.convert_load_symbol(var_id)
        value_address = self.generator.bytecode_size
        self.visit_to_generate(aug_assign.value)
        self.generator.convert_operation(aug_assign.op)
        self.generator.convert_store_variable(var_id, value_address)
        return self.build_data(aug_assign)

    def visit_Subscript(self, subscript: ast.Subscript) -> GeneratorData:
        """
        Visitor of a subscript node

        :param subscript: the python ast subscript node
        """
        if isinstance(subscript.slice, ast.Slice):
            return self.visit_Subscript_Slice(subscript)

        return self.visit_Subscript_Index(subscript)

    def visit_Subscript_Index(self, subscript: ast.Subscript) -> GeneratorData:
        """
        Visitor of a subscript node with index

        :param subscript: the python ast subscript node
        """
        index = None
        symbol_id = None
        if isinstance(subscript.ctx, ast.Load):
            # get item
            value_data = self.visit_to_generate(subscript.value)
            slice = subscript.slice.value if isinstance(subscript.slice, ast.Index) else subscript.slice
            self.visit_to_generate(slice)
            self.generator.convert_get_item()

            value_type = value_data.type
        else:
            # set item
            var_data = self.visit(subscript.value)

            index = subscript.slice.value if isinstance(subscript.slice, ast.Index) else subscript.slice
            symbol_id = var_data.symbol_id
            value_type = var_data.type

        result_type = value_type.item_type if isinstance(value_type, SequenceType) else value_type
        return self.build_data(subscript, result_type=result_type,
                               symbol_id=symbol_id, index=index)

    def visit_Subscript_Slice(self, subscript: ast.Subscript) -> GeneratorData:
        """
        Visitor of a subscript node with slice

        :param subscript: the python ast subscript node
        """
        lower_omitted = subscript.slice.lower is None
        upper_omitted = subscript.slice.upper is None
        step_omitted = subscript.slice.step is None

        self.visit_to_generate(subscript.value)

        step_negative = True if not step_omitted and subscript.slice.step.n < 0 else False
        # if step is negative, then consider the value reversed
        if step_negative:
            self.generator.convert_array_negative_stride()

        # if both are explicit
        if not lower_omitted and not upper_omitted:
            addresses = [VMCodeMapping.instance().bytecode_size]
            self.visit_to_generate(subscript.slice.lower)

            # length of slice
            addresses.append(VMCodeMapping.instance().bytecode_size)
            self.visit_to_generate(subscript.slice.upper)

            self.generator.convert_get_sub_array(addresses, step_negative)
        # only one of them is omitted
        elif lower_omitted != upper_omitted:
            # start position is omitted
            if lower_omitted:
                self.visit_to_generate(subscript.slice.upper)
                self.generator.convert_get_array_beginning(step_negative)
            # end position is omitted
            else:
                self.generator.duplicate_stack_top_item()
                # length of slice
                self.generator.convert_builtin_method_call(Builtin.Len)
                self.visit_to_generate(subscript.slice.lower)
                self.generator.convert_get_array_ending(step_negative)
        else:
            self.generator.convert_copy()

        if not step_omitted:
            self.visit_to_generate(subscript.slice.step)
            self.generator.convert_get_stride()

        return self.build_data(subscript)

    def _convert_unary_operation(self, operand, op):
        self.visit_to_generate(operand)
        self.generator.convert_operation(op)

    def _convert_binary_operation(self, left, right, op):
        self.visit_to_generate(left)
        self.visit_to_generate(right)
        self.generator.convert_operation(op)

    def visit_BinOp(self, bin_op: ast.BinOp) -> GeneratorData:
        """
        Visitor of a binary operation node

        :param bin_op: the python ast binary operation node
        """
        if isinstance(bin_op.op, BinaryOperation):
            self._convert_binary_operation(bin_op.left, bin_op.right, bin_op.op)

        return self.build_data(bin_op)

    def visit_UnaryOp(self, un_op: ast.UnaryOp) -> GeneratorData:
        """
        Visitor of a binary operation node

        :param un_op: the python ast binary operation node
        """
        if isinstance(un_op.op, UnaryOperation):
            self._convert_unary_operation(un_op.operand, un_op.op)

        return self.build_data(un_op)

    def visit_Compare(self, compare: ast.Compare) -> GeneratorData:
        """
        Visitor of a compare operation node

        :param compare: the python ast compare operation node
        """
        operation_symbol: IOperation = BinaryOp.And
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
                    operation_symbol = op
                else:
                    operation_symbol = BinaryOp.And
                    self.generator.convert_operation(BinaryOp.And)
            left = right

        return self.build_data(compare, symbol=operation_symbol, result_type=operation_symbol.result)

    def visit_BoolOp(self, bool_op: ast.BoolOp) -> GeneratorData:
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

        return self.build_data(bool_op)

    def visit_While(self, while_node: ast.While) -> GeneratorData:
        """
        Visitor of a while statement node

        :param while_node: the python ast while statement node
        """
        start_addr: int = self.generator.convert_begin_while()
        for stmt in while_node.body:
            self.visit_to_map(stmt, generate=True)

        test_address: int = VMCodeMapping.instance().bytecode_size
        test_data = self.visit_to_map(while_node.test, generate=True)
        self.generator.convert_end_while(start_addr, test_address)

        else_begin_address: int = self.generator.last_code_start_address
        for stmt in while_node.orelse:
            self.visit_to_map(stmt, generate=True)

        self.generator.convert_end_loop_else(start_addr, else_begin_address, len(while_node.orelse) > 0)
        return self.build_data(while_node, index=start_addr)

    def visit_For(self, for_node: ast.For) -> GeneratorData:
        """
        Visitor of for statement node

        :param for_node: the python ast for node
        """
        self.visit_to_generate(for_node.iter)
        start_address = self.generator.convert_begin_for()

        if isinstance(for_node.target, tuple):
            for target in for_node.target:
                var_data = self.visit_to_map(target)
                self.generator.convert_store_variable(var_data.symbol_id)
        else:
            var_data = self.visit(for_node.target)
            self.generator.convert_store_variable(var_data.symbol_id)

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
        return self.build_data(for_node)

    def visit_If(self, if_node: ast.If) -> GeneratorData:
        """
        Visitor of if statement node

        :param if_node: the python ast if statement node
        """
        test = self.visit_to_map(if_node.test, generate=True)

        if not Type.bool.is_type_of(test.type) and test.type is not None:
            self.generator.convert_builtin_method_call(Builtin.Bool)

        start_addr: int = self.generator.convert_begin_if()
        for stmt in if_node.body:
            self.visit_to_map(stmt, generate=True)

        ends_with_if = len(if_node.body) > 0 and isinstance(if_node.body[-1], ast.If)

        if len(if_node.orelse) > 0:
            start_addr = self.generator.convert_begin_else(start_addr, ends_with_if)
            for stmt in if_node.orelse:
                self.visit_to_map(stmt, generate=True)

        self.generator.convert_end_if(start_addr)
        return self.build_data(if_node)

    def visit_Expr(self, expr: ast.Expr, generate: bool = False) -> GeneratorData:
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

    def visit_IfExp(self, if_node: ast.IfExp) -> GeneratorData:
        """
        Visitor of if expression node

        :param if_node: the python ast if statement node
        """
        self.visit_to_map(if_node.test, generate=True)

        start_addr: int = self.generator.convert_begin_if()
        body_data = self.visit_to_map(if_node.body, generate=True)

        start_addr = self.generator.convert_begin_else(start_addr)
        else_data = self.visit_to_map(if_node.orelse, generate=True)

        self.generator.convert_end_if(start_addr)
        return self.build_data(if_node, result_type=Type.union.build([body_data.type, else_data.type]))

    def visit_Assert(self, assert_node: ast.Assert) -> GeneratorData:
        """
        Visitor of the assert node

        :param assert_node: the python ast assert node
        """
        self.visit_to_generate(assert_node.test)

        if assert_node.msg is not None:
            self.generator.duplicate_stack_top_item()
            self.generator.insert_not()

            # if assert is false, log the message
            start_addr: int = self.generator.convert_begin_if()

            self.visit_to_generate(assert_node.msg)
            self.generator.convert_builtin_method_call(Interop.Log)

            self.generator.convert_end_if(start_addr)

        self.generator.convert_assert()
        return self.build_data(assert_node)

    def visit_Call(self, call: ast.Call) -> GeneratorData:
        """
        Visitor of a function call node

        :param call: the python ast function call node
        :returns: The called function return type
        """
        # the parameters are included into the stack in the reversed order
        last_address = VMCodeMapping.instance().bytecode_size
        last_stack = self.generator.stack_size

        func_data = self.visit(call.func)
        function_id = func_data.symbol_id
        # if the symbol is not a method, check if it is a class method
        if (isinstance(func_data.type, ClassType) and func_data.symbol_id in func_data.type.symbols
                and isinstance(func_data.type.symbols[func_data.symbol_id], IExpression)):
            symbol = func_data.type.symbols[func_data.symbol_id]
        else:
            symbol = func_data.symbol

        if not isinstance(symbol, Method):
            is_internal = hasattr(call, 'is_internal_call') and call.is_internal_call
            _, symbol = self.generator.get_symbol(function_id, is_internal=is_internal)

        if self.is_implemented_class_type(symbol):
            self.generator.convert_init_user_class(symbol)
            symbol = symbol.constructor_method()
        args_addresses: List[int] = []

        has_cls_or_self_argument = isinstance(symbol, Method) and symbol.has_cls_or_self
        if not has_cls_or_self_argument:
            self._remove_inserted_opcodes_since(last_address, last_stack)

        if isinstance(symbol, Method):
            # self or cls is already generated
            call_args = (call.args[1:]
                         if has_cls_or_self_argument and len(call.args) == len(symbol.args)
                         else call.args)
            args_to_generate = [arg for index, arg in enumerate(call_args) if index in symbol.args_to_be_generated()]
            keywords_dict = {keyword.arg: keyword.value for keyword in call.keywords}
            keywords_with_index = {index: keywords_dict[arg_name]
                                   for index, arg_name in enumerate(symbol.args)
                                   if arg_name in keywords_dict}

            for index in keywords_with_index:
                if index < len(args_to_generate):
                    # override default values
                    args_to_generate[index] = keywords_with_index[index]
                else:
                    # put keywords
                    args_to_generate.append(keywords_with_index[index])

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

        args_begin_address = self.generator.last_code_start_address
        for arg in args:
            args_addresses.append(
                VMCodeMapping.instance().bytecode_size
            )
            self.visit_to_generate(arg)
        if has_cls_or_self_argument:
            num_args = len(args_addresses)
            if self.generator.stack_size > num_args:
                value = self.generator._stack_pop(-num_args - 1)
                self.generator._stack_append(value)
            end_address = VMCodeMapping.instance().move_to_end(last_address, args_begin_address)
            if not symbol.is_init:
                args_addresses.append(end_address)

        if self.is_exception_name(function_id):
            self.generator.convert_new_exception(len(call.args))
        elif isinstance(symbol, type(Builtin.Super)) and len(args_to_generate) == 0:
            self_or_cls_id = list(self.current_method.args)[0]
            self.generator.convert_load_symbol(self_or_cls_id)
        elif isinstance(symbol, IBuiltinMethod):
            self.generator.convert_builtin_method_call(symbol, args_addresses)
        else:
            self.generator.convert_load_symbol(function_id, args_addresses)

        return self.build_data(call, symbol=symbol, symbol_id=function_id,
                               result_type=symbol.type if isinstance(symbol, IExpression) else symbol,
                               already_generated=True)

    def visit_Raise(self, raise_node: ast.Raise) -> GeneratorData:
        """
        Visitor of the raise node

        :param raise_node: the python ast raise node
        """
        self.visit_to_map(raise_node.exc, generate=True)
        self.generator.convert_raise_exception()
        return self.build_data(raise_node)

    def visit_Try(self, try_node: ast.Try) -> GeneratorData:
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

        else_address = None
        if len(try_node.orelse) > 0:
            else_start_address = self.generator.convert_begin_else(try_end)
            else_address = self.generator.bytecode_size
            for stmt in try_node.orelse:
                self.visit_to_map(stmt, generate=True)
            self.generator.convert_end_if(else_start_address)

        except_end = self.generator.convert_end_try(try_address, try_end, else_address)
        for stmt in try_node.finalbody:
            self.visit_to_map(stmt, generate=True)
        self.generator.convert_end_try_finally(except_end, try_address, len(try_node.finalbody) > 0)

        return self.build_data(try_node)

    def visit_Name(self, name_node: ast.Name) -> GeneratorData:
        """
        Visitor of a name node

        :param name_node: the python ast name identifier node
        :return: the identifier of the name
        """
        name = name_node.id
        if name not in self._symbols:
            hashed_name = self._get_unique_name(name, self._tree)
            if hashed_name not in self._symbols and hasattr(name_node, 'origin'):
                hashed_name = self._get_unique_name(name, name_node.origin)

            if hashed_name in self._symbols:
                name = hashed_name
        return self.build_data(name_node, name)

    def visit_Starred(self, starred: ast.Starred) -> GeneratorData:
        value_data = self.visit_to_generate(starred.value)
        self.generator.convert_starred_variable()

        starred_data = value_data.copy(starred)
        starred_data.already_generated = True
        return starred_data

    def visit_Attribute(self, attribute: ast.Attribute) -> GeneratorData:
        """
        Visitor of a attribute node

        :param attribute: the python ast attribute node
        :return: the identifier of the attribute
        """
        last_address = VMCodeMapping.instance().bytecode_size
        last_stack = self.generator.stack_size

        _, attr = self.generator.get_symbol(attribute.attr)
        value = attribute.value
        value_symbol = None
        value_type = None
        value_data = self.visit(value)
        need_to_visit_again = True

        if value_data.symbol_id is not None and not value_data.already_generated:
            value_id = value_data.symbol_id
            if value_data.symbol is not None:
                value_symbol = value_data.symbol
            else:
                _, value_symbol = self.generator.get_symbol(value_id)
            value_type = value_symbol.type if hasattr(value_symbol, 'type') else value_symbol

            if hasattr(value_type, 'symbols') and attribute.attr in value_type.symbols:
                attr = value_type.symbols[attribute.attr]
            elif isinstance(value_type, Package) and attribute.attr in value_type.inner_packages:
                attr = value_type.inner_packages[attribute.attr]

            if isinstance(value_symbol, UserClass):
                if isinstance(attr, Method) and attr.has_cls_or_self:
                    self.generator.convert_load_symbol(value_id)
                    need_to_visit_again = False

                if isinstance(attr, Variable):
                    self.visit_to_generate(attribute.value)
                    self.generator.convert_load_symbol(attribute.attr, class_type=value_symbol)
                    return self.build_data(attribute, symbol=attr)
        else:
            need_to_visit_again = value_data.already_generated
            self._remove_inserted_opcodes_since(last_address, last_stack)

        # the verification above only verify variables, this one will should work with literals and constants
        if isinstance(value, (ast.Constant if SYS_VERSION_INFO >= (3, 8) else (ast.Num, ast.Str, ast.Bytes))) \
                and len(attr.args) > 0 and isinstance(attr, IBuiltinMethod) and attr.has_self_argument:
            attr = attr.build(value_data.type)

        if attr is not Type.none and not hasattr(attribute, 'generate_value'):
            value_symbol_id = (value_symbol.identifier
                               if self.is_implemented_class_type(value_symbol)
                               else value_data.symbol_id)
            attribute_id = f'{value_symbol_id}{constants.ATTRIBUTE_NAME_SEPARATOR}{attribute.attr}'
            index = value_type if isinstance(value_type, Package) else None
            return self.build_data(attribute, symbol_id=attribute_id, symbol=attr, index=index)

        if isinstance(value, ast.Attribute):
            value_data = self.visit(value)
        elif hasattr(attribute, 'generate_value') and attribute.generate_value:
            current_bytecode_size = self.generator.bytecode_size
            if need_to_visit_again:
                value_data = self.visit_to_generate(attribute.value)

            result = value_data.type
            generation_result = value_data.symbol
            if result is None and value_data.symbol_id is not None:
                _, result = self.generator.get_symbol(value_data.symbol_id)
                if isinstance(result, IExpression):
                    generation_result = result
                    result = result.type

            if self.is_implemented_class_type(result):
                class_attr_id = f'{result.identifier}.{attribute.attr}'
                symbol_id = class_attr_id
                symbol = None
                result_type = None
                symbol_index = None

                if self.generator.bytecode_size > current_bytecode_size and isinstance(result, UserClass):
                    # it was generated already, don't convert again
                    generated = False
                    symbol_id = attribute.attr if isinstance(generation_result, Variable) else class_attr_id
                    result_type = result
                else:
                    index = self.generator.convert_class_symbol(result,
                                                                attribute.attr,
                                                                isinstance(attribute.ctx, ast.Load))
                    generated = True
                    symbol = result
                    if not isinstance(result, UserClass):
                        if isinstance(index, int):
                            symbol_index = index
                        else:
                            symbol_id = index

                return self.build_data(attribute,
                                       symbol_id=symbol_id, symbol=symbol,
                                       result_type=result_type, index=symbol_index,
                                       already_generated=generated)

        if value_data is not None and value_symbol is None:
            value_symbol = value_data.symbol_id

        if value_data is not None and value_data.symbol_id is not None:
            value_id = f'{value_data.symbol_id}{constants.ATTRIBUTE_NAME_SEPARATOR}{attribute.attr}'
        else:
            value_id = attribute.attr

        return self.build_data(attribute, symbol_id=value_id, symbol=value_symbol)

    def visit_Continue(self, continue_node: ast.Continue) -> GeneratorData:
        """
        :param continue_node: the python ast continue statement node
        """
        self.generator.convert_loop_continue()
        return self.build_data(continue_node)

    def visit_Break(self, break_node: ast.Break) -> GeneratorData:
        """
        :param break_node: the python ast break statement node
        """
        self.generator.convert_loop_break()
        return self.build_data(break_node)

    def visit_Constant(self, constant: ast.Constant) -> GeneratorData:
        """
        Visitor of constant values node

        :param constant: the python ast constant value node
        """
        index = self.generator.convert_literal(constant.value)
        result_type = self.get_type(constant.value)
        return self.build_data(constant, result_type=result_type, index=index, already_generated=True)

    def visit_NameConstant(self, constant: ast.NameConstant) -> GeneratorData:
        """
        Visitor of constant names node

        :param constant: the python ast name constant node
        """
        index = self.generator.convert_literal(constant.value)
        result_type = self.get_type(constant.value)
        return self.build_data(constant, result_type=result_type, index=index, already_generated=True)

    def visit_Num(self, num: ast.Num) -> GeneratorData:
        """
        Visitor of literal number node

        :param num: the python ast number node
        """
        index = self.generator.convert_literal(num.n)
        result_type = self.get_type(num.n)
        return self.build_data(num, result_type=result_type, index=index, already_generated=True)

    def visit_Str(self, string: ast.Str) -> GeneratorData:
        """
        Visitor of literal string node

        :param string: the python ast string node
        """
        index = self.generator.convert_literal(string.s)
        result_type = self.get_type(string.s)
        return self.build_data(string, result_type=result_type, index=index, already_generated=True)

    def visit_Bytes(self, bts: ast.Bytes) -> GeneratorData:
        """
        Visitor of literal bytes node

        :param bts: the python ast bytes node
        """
        index = self.generator.convert_literal(bts.s)
        result_type = self.get_type(bts.s)
        return self.build_data(bts, result_type=result_type, index=index, already_generated=True)

    def visit_Tuple(self, tup_node: ast.Tuple) -> GeneratorData:
        """
        Visitor of literal tuple node

        :param tup_node: the python ast tuple node
        """
        result_type = Type.tuple
        self._create_array(tup_node.elts, result_type)
        return self.build_data(tup_node, result_type=result_type, already_generated=True)

    def visit_List(self, list_node: ast.List) -> GeneratorData:
        """
        Visitor of literal list node

        :param list_node: the python ast list node
        """
        result_type = Type.list
        self._create_array(list_node.elts, result_type)
        return self.build_data(list_node, result_type=result_type, already_generated=True)

    def visit_Dict(self, dict_node: ast.Dict) -> GeneratorData:
        """
        Visitor of literal dict node

        :param dict_node: the python ast dict node
        """
        result_type = Type.dict
        length = min(len(dict_node.keys), len(dict_node.values))
        self.generator.convert_new_map(result_type)
        for key_value in range(length):
            self.generator.duplicate_stack_top_item()
            self.visit_to_generate(dict_node.keys[key_value])
            value_data = self.visit_to_generate(dict_node.values[key_value])
            self.generator.convert_set_item(value_data.index)

        return self.build_data(dict_node, result_type=result_type, already_generated=True)

    def visit_Pass(self, pass_node: ast.Pass) -> GeneratorData:
        """
        Visitor of pass node

        :param pass_node: the python ast dict node
        """
        # only generates if the scope is a function
        result_type = None
        generated = False

        if isinstance(self.current_method, Method):
            self.generator.insert_nop()
            generated = True

        return self.build_data(pass_node, result_type=result_type, already_generated=generated)

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
