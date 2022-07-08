from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from boa3 import constants
from boa3.analyser.analyser import Analyser
from boa3.analyser.model.symbolscope import SymbolScope
from boa3.compiler import codegenerator
from boa3.compiler.codegenerator.stackmemento import NeoStack, StackMemento
from boa3.compiler.codegenerator.vmcodemapping import VMCodeMapping
from boa3.model.builtin.builtin import Builtin
from boa3.model.builtin.internal.innerdeploymethod import InnerDeployMethod
from boa3.model.builtin.interop.interop import Interop
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.event import Event
from boa3.model.imports.importsymbol import Import
from boa3.model.imports.package import Package
from boa3.model.method import Method
from boa3.model.operation.binaryop import BinaryOp
from boa3.model.operation.operation import IOperation
from boa3.model.operation.unaryop import UnaryOp
from boa3.model.property import Property
from boa3.model.symbol import ISymbol
from boa3.model.type.classes.classtype import ClassType
from boa3.model.type.classes.contractinterfaceclass import ContractInterfaceClass
from boa3.model.type.classes.userclass import UserClass
from boa3.model.type.collection.icollection import ICollectionType
from boa3.model.type.collection.sequence.buffertype import Buffer as BufferType
from boa3.model.type.collection.sequence.mutable.listtype import ListType
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.primitive.bytestype import BytesType
from boa3.model.type.primitive.primitivetype import PrimitiveType
from boa3.model.type.primitive.strtype import StrType
from boa3.model.type.type import IType, Type
from boa3.model.variable import Variable
from boa3.neo.vm.TryCode import TryCode
from boa3.neo.vm.VMCode import VMCode
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.opcode.OpcodeInfo import OpcodeInfo, OpcodeInformation
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.StackItem import StackItemType


class CodeGenerator:
    """
    This class is responsible for generating the Neo VM bytecode

    :ivar symbol_table: a dictionary that maps the global symbols.
    """

    @staticmethod
    def generate_code(analyser: Analyser) -> bytes:
        """
        Generates the Neo VM bytecode using of the analysed Python code

        :param analyser: semantic analyser of the Python code
        :return: the Neo VM bytecode
        """
        VMCodeMapping.reset()
        analyser.update_symbol_table_with_imports()
        import ast
        from boa3.compiler.codegenerator.codegeneratorvisitor import VisitorCodeGenerator

        all_imports = CodeGenerator._find_all_imports(analyser)
        generator = CodeGenerator(analyser.symbol_table)
        deploy_method = (analyser.symbol_table[constants.DEPLOY_METHOD_ID]
                         if constants.DEPLOY_METHOD_ID in analyser.symbol_table
                         else None)
        deploy_origin_module = analyser.ast_tree

        if hasattr(deploy_method, 'origin') and deploy_method.origin in analyser.ast_tree.body:
            analyser.ast_tree.body.remove(deploy_method.origin)

        visitor = VisitorCodeGenerator(generator, analyser.filename)
        visitor._root_module = analyser.ast_tree
        visitor.visit(analyser.ast_tree)

        analyser.update_symbol_table(generator.symbol_table)
        generator.symbol_table.clear()
        generator.symbol_table.update(analyser.symbol_table.copy())

        for symbol in all_imports.values():
            generator.symbol_table.update(symbol.all_symbols)

            if hasattr(deploy_method, 'origin') and deploy_method.origin in symbol.ast.body:
                symbol.ast.body.remove(deploy_method.origin)
                deploy_origin_module = symbol.ast

            visitor.set_filename(symbol.origin)
            visitor.visit(symbol.ast)

            analyser.update_symbol_table(symbol.all_symbols)
            generator.symbol_table.clear()
            generator.symbol_table.update(analyser.symbol_table.copy())

        if len(generator._globals) > 0:
            from boa3.compiler.codegenerator.initstatementsvisitor import InitStatementsVisitor
            deploy_stmts, static_stmts = InitStatementsVisitor.separate_global_statements(analyser.symbol_table,
                                                                                          visitor.global_stmts)

            deploy_method = deploy_method if deploy_method is not None else InnerDeployMethod.instance().copy()

            if len(deploy_stmts) > 0:
                if_update_body = ast.parse(f"if not {list(deploy_method.args)[1]}: pass").body[0]
                if_update_body.body = deploy_stmts
                if_update_body.test.op = UnaryOp.Not
                deploy_method.origin.body.insert(0, if_update_body)

            visitor.global_stmts = static_stmts

        if hasattr(deploy_method, 'origin'):
            deploy_ast = ast.parse("")
            deploy_ast.body = [deploy_method.origin]

            generator.symbol_table[constants.DEPLOY_METHOD_ID] = deploy_method
            analyser.symbol_table[constants.DEPLOY_METHOD_ID] = deploy_method
            visitor._tree = deploy_origin_module
            visitor.visit(deploy_ast)

            generator.symbol_table.clear()
            generator.symbol_table.update(analyser.symbol_table.copy())

        visitor.set_filename(analyser.filename)
        generator.can_init_static_fields = True
        if len(visitor.global_stmts) > 0:
            global_ast = ast.parse("")
            global_ast.body = visitor.global_stmts
            visitor.visit(global_ast)
            generator.initialized_static_fields = True

        analyser.update_symbol_table(generator.symbol_table)
        bytecode = generator.bytecode
        return bytecode

    @staticmethod
    def _find_all_imports(analyser: Analyser) -> Dict[str, Import]:
        imports = {}
        for key, symbol in analyser.symbol_table.copy().items():
            if isinstance(symbol, Import):
                importing = symbol
            elif isinstance(symbol, Package) and isinstance(symbol.origin, Import):
                importing = symbol.origin
                analyser.symbol_table[symbol.origin.origin] = symbol.origin
            else:
                importing = None

            if importing is not None and importing.origin not in imports:
                imports[importing.origin] = importing

        return imports

    def __init__(self, symbol_table: Dict[str, ISymbol]):
        self.symbol_table: Dict[str, ISymbol] = symbol_table.copy()
        self.additional_symbols: Optional[Dict[str, ISymbol]] = None

        self._current_method: Method = None
        self._current_class: Method = None

        self._missing_target: Dict[int, List[VMCode]] = {}  # maps targets with address not included yet
        self._can_append_target: bool = True

        self._scope_stack: List[SymbolScope] = []
        self._global_scope = SymbolScope()

        self._current_loop: List[int] = []  # a stack with the converting loops' start addresses
        self._current_for: List[int] = []
        self._jumps_to_loop_condition: Dict[int, List[int]] = {}

        self._jumps_to_loop_break: Dict[int, List[int]] = {}
        # the indexes of boolean insertion values indicating if the jmp is from a break
        self._inserted_loop_breaks: Dict[int, List[int]] = {}

        self._opcodes_to_remove: List[int] = []
        self._stack_states: StackMemento = StackMemento()  # simulates neo execution stack

        self.can_init_static_fields: bool = False
        self.initialized_static_fields: bool = False

        self._static_vars: Optional[list] = None
        self._global_vars: Optional[list] = None

    @property
    def bytecode(self) -> bytes:
        """
        Gets the bytecode of the translated code

        :return: the generated bytecode
        """
        opcodes = VMCodeMapping.instance().get_opcodes(self._opcodes_to_remove)
        self.set_code_targets()
        VMCodeMapping.instance().remove_opcodes_by_code(opcodes)
        self._opcodes_to_remove.clear()
        return VMCodeMapping.instance().bytecode()

    @property
    def last_code(self) -> Optional[VMCode]:
        """
        Gets the last code in the bytecode

        :return: the last code. If the bytecode is empty, returns None
        :rtype: VMCode or None
        """
        if len(VMCodeMapping.instance().codes) > 0:
            return VMCodeMapping.instance().codes[-1]
        else:
            return None

    @property
    def _stack(self) -> NeoStack:
        return self._stack_states.current_stack

    @property
    def stack_size(self) -> int:
        """
        Gets the size of the stack

        :return: the size of the stack of converted values
        """
        return len(self._stack)

    def _stack_append(self, value_type: IType):
        self._stack_states.append(value_type, self.last_code)

    def _stack_pop(self, index: int = -1) -> IType:
        if len(self._stack) > 0:
            return self._stack.pop(index)

    @property
    def last_code_start_address(self) -> int:
        """
        Gets the first address from last code in the bytecode

        :return: the last code's first address
        """
        instance = VMCodeMapping.instance()
        if len(instance.codes) > 0:
            return instance.get_start_address(instance.codes[-1])
        else:
            return 0

    @property
    def bytecode_size(self) -> int:
        """
        Gets the current bytecode size

        :return: the current bytecode size
        """
        return VMCodeMapping.instance().bytecode_size

    @property
    def _args(self) -> List[str]:
        """
        Gets a list with the arguments names of the current method

        :return: A list with the arguments names
        """
        return [] if self._current_method is None else list(self._current_method.args.keys())

    @property
    def _locals(self) -> List[str]:
        """
        Gets a list with the variables names in the scope of the current method

        :return: A list with the variables names
        """
        return [] if self._current_method is None else list(self._current_method.locals.keys())

    @property
    def _globals(self) -> List[str]:
        return self._module_variables(True)

    @property
    def _statics(self) -> List[str]:
        return self._module_variables(False)

    def _module_variables(self, modified_variable: bool) -> List[str]:
        """
        Gets a list with the variables name in the global scope

        :return: A list with the variables names
        """
        if modified_variable:
            vars_map = self._global_vars
        else:
            vars_map = self._static_vars

        module_global_variables = []
        module_global_ids = []
        result_global_vars = []
        for var_id, var in self.symbol_table.items():
            if isinstance(var, Variable) and var.is_reassigned == modified_variable:
                module_global_variables.append((var_id, var))
                module_global_ids.append(var_id)
                result_global_vars.append(var)

        class_with_class_variables = []
        class_with_variables_ids = []
        for class_id, class_symbol in self.symbol_table.items():
            if isinstance(class_symbol, UserClass) and len(class_symbol.class_variables) > 0:
                class_with_class_variables.append((class_id, class_symbol))
                class_with_variables_ids.append(class_id)

        if not self.can_init_static_fields:
            for imported in self.symbol_table.values():
                if isinstance(imported, Import):
                    # tried to use set and just update, but we need the variables to be ordered
                    for var_id, var in imported.variables.items():
                        if (isinstance(var, Variable)
                                and var.is_reassigned == modified_variable
                                and var_id not in module_global_ids
                                and var not in result_global_vars):
                            module_global_variables.append((var_id, var))
                            module_global_ids.append(var_id)
                            result_global_vars.append(var)

                    # TODO: include user class from imported symbols as well

        if modified_variable:
            result_map = module_global_variables
            result = module_global_ids
        else:
            result_map = module_global_variables + class_with_class_variables
            result_global_vars = result_global_vars + [classes for (class_id, classes) in class_with_class_variables]
            result = module_global_ids + class_with_variables_ids

        original_ids = []
        for value in result:
            split = value.split(constants.VARIABLE_NAME_SEPARATOR)
            if len(split) > 1:
                new_index = split[-1]
            else:
                new_index = value
            original_ids.append(new_index)

        if vars_map != result_map:
            if vars_map is None:
                # save to keep the same order in future accesses
                if modified_variable:
                    self._global_vars = result_map
                else:
                    self._static_vars = result_map

            else:
                # reorder to keep the same order as the first access
                pre_reordered_ids = [var_id for (var_id, var) in vars_map]
                for index, (value, var) in enumerate(vars_map):
                    if value not in result:
                        if var in result_global_vars:
                            var_index = result_global_vars.index(var)
                            new_value = result_map[var_index]
                        else:
                            var_index = original_ids.index(value)
                            new_value = result_map[var_index]

                        vars_map[index] = new_value

                # add new symbols at the end always
                reordered_ids = [var_id for (var_id, var) in vars_map]
                additional_items = []
                for index, var_id in enumerate(result):
                    if var_id not in reordered_ids and var_id not in pre_reordered_ids:
                        additional_items.append(var_id)
                        vars_map.append(result_map[index])

                result = reordered_ids + additional_items

        return result

    @property
    def _current_scope(self) -> SymbolScope:
        return self._scope_stack[-1] if len(self._scope_stack) > 0 else self._global_scope

    def is_none_inserted(self) -> bool:
        """
        Checks whether the last insertion is null

        :return: whether the last value is null
        """
        return (self.last_code.opcode is Opcode.PUSHNULL or
                (len(self._stack) > 0 and self._stack[-1] is Type.none))

    def get_symbol(self, identifier: str, scope: Optional[ISymbol] = None, is_internal: bool = False) -> Tuple[str, ISymbol]:
        """
        Gets a symbol in the symbol table by its id

        :param identifier: id of the symbol
        :return: the symbol if exists. Symbol None otherwise
        """
        cur_symbol_table = self.symbol_table.copy()
        if isinstance(self.additional_symbols, dict):
            cur_symbol_table.update(self.additional_symbols)

        if len(self._scope_stack) > 0:
            for symbol_scope in self._scope_stack:
                if identifier in symbol_scope:
                    return identifier, symbol_scope[identifier]

        if scope is not None and hasattr(scope, 'symbols') and isinstance(scope.symbols, dict):
            if identifier in scope.symbols and isinstance(scope.symbols[identifier], ISymbol):
                return identifier, scope.symbols[identifier]
        else:
            if self._current_method is not None and identifier in self._current_method.symbols:
                return identifier, self._current_method.symbols[identifier]
            elif identifier in cur_symbol_table:
                return identifier, cur_symbol_table[identifier]

            # the symbol may be a built in. If not, returns None
            symbol = Builtin.get_symbol(identifier)
            if symbol is not None:
                return identifier, symbol

            if not isinstance(identifier, str):
                return identifier, symbol
            split = identifier.split(constants.ATTRIBUTE_NAME_SEPARATOR)
            if len(split) > 1:
                attribute, symbol_id = constants.ATTRIBUTE_NAME_SEPARATOR.join(split[:-1]), split[-1]
                another_attr_id, attr = self.get_symbol(attribute, is_internal=is_internal)
                if hasattr(attr, 'symbols') and symbol_id in attr.symbols:
                    return symbol_id, attr.symbols[symbol_id]
                elif isinstance(attr, Package) and symbol_id in attr.inner_packages:
                    return symbol_id, attr.inner_packages[symbol_id]

            if is_internal:
                from boa3.model import imports
                found_symbol = imports.builtin.get_internal_symbol(identifier)
                if isinstance(found_symbol, ISymbol):
                    return identifier, found_symbol
        return identifier, Type.none

    def initialize_static_fields(self) -> bool:
        """
        Converts the signature of the method

        :return: whether there are static fields to be initialized
        """
        if not self.can_init_static_fields:
            return False
        if self.initialized_static_fields:
            return False

        num_static_fields = len(self._statics)
        if num_static_fields > 0:
            init_data = bytearray([num_static_fields])
            self.__insert1(OpcodeInfo.INITSSLOT, init_data)

            if constants.INITIALIZE_METHOD_ID in self.symbol_table:
                from boa3.helpers import get_auxiliary_name
                method = self.symbol_table.pop(constants.INITIALIZE_METHOD_ID)
                new_id = get_auxiliary_name(constants.INITIALIZE_METHOD_ID, method)
                self.symbol_table[new_id] = method

            init_method = Method(is_public=True)
            init_method.init_bytecode = self.last_code
            self.symbol_table[constants.INITIALIZE_METHOD_ID] = init_method

        return num_static_fields > 0

    def end_initialize(self):
        """
        Converts the signature of the method
        """
        self.insert_return()
        self.initialized_static_fields = True

        if constants.INITIALIZE_METHOD_ID in self.symbol_table:
            init_method = self.symbol_table[constants.INITIALIZE_METHOD_ID]
            init_method.end_bytecode = self.last_code

    def convert_begin_method(self, method: Method):
        """
        Converts the signature of the method

        :param method: method that is being converted
        """
        new_variable_scope = self._scope_stack[-1].copy() if len(self._scope_stack) > 0 else SymbolScope()
        self._scope_stack.append(new_variable_scope)

        num_args: int = len(method.args)
        num_vars: int = len(method.locals)

        method.init_address = VMCodeMapping.instance().bytecode_size
        if num_args > 0 or num_vars > 0:
            init_data = bytearray([num_vars, num_args])
            self.__insert1(OpcodeInfo.INITSLOT, init_data)
            method.init_bytecode = self.last_code
        self._current_method = method

    def convert_end_method(self, method_id: Optional[str] = None):
        """
        Converts the end of the method
        """
        if (self._current_method.init_bytecode is None
                and self._current_method.init_address in VMCodeMapping.instance().code_map):
            self._current_method.init_bytecode = VMCodeMapping.instance().code_map[self._current_method.init_address]

        if self.last_code.opcode is not Opcode.RET:
            if self._current_method.is_init:
                # return the built object if it's a constructor
                self_id, self_value = list(self._current_method.args.items())[0]
                self.convert_load_variable(self_id, self_value)

            self.insert_return()

        self._current_method.end_bytecode = self.last_code
        self._current_method = None
        self._stack.clear()

        function_variable_scope = self._scope_stack.pop()

    def insert_return(self):
        """
        Insert the return statement
        """
        self.__insert1(OpcodeInfo.RET)

    def insert_not(self):
        """
        Insert a `not` to change the value of a bool
        """
        self.__insert1(OpcodeInfo.NOT)

    def insert_nop(self):
        """
        Insert a NOP opcode
        """
        self.__insert1(OpcodeInfo.NOP)

    def convert_begin_while(self, is_for: bool = False) -> int:
        """
        Converts the beginning of the while statement

        :param is_for: whether the loop is a for loop or not
        :return: the address of the while first opcode
        """
        # it will be updated when the while ends
        self._insert_jump(OpcodeInfo.JMP)

        start_address = self.last_code_start_address
        self._current_loop.append(start_address)
        if is_for:
            self._current_for.append(start_address)

        return start_address

    def convert_end_while(self, start_address: int, test_address: int):
        """
        Converts the end of the while statement

        :param start_address: the address of the while first opcode
        :param test_address: the address of the while test fist opcode
        """
        self.convert_end_loop(start_address, test_address, False)

    def convert_begin_for(self) -> int:
        """
        Converts the beginning of the for statement

        :return: the address of the for first opcode
        """
        self.convert_literal(0)
        address = self.convert_begin_while(True)

        self.duplicate_stack_item(2)  # duplicate for sequence
        self.duplicate_stack_item(2)  # duplicate for index
        self.convert_get_item()
        return address

    def convert_end_for(self, start_address: int) -> int:
        """
        Converts the end of the for statement

        :param start_address: the address of the for first opcode
        :return: the address of the loop condition
        """
        self.__insert1(OpcodeInfo.INC)      # index += 1
        if len(self._stack) < 1 or self._stack[-1] is not Type.int:
            self._stack_append(Type.int)
        for_increment = self.last_code_start_address
        test_address = VMCodeMapping.instance().bytecode_size
        self._update_continue_jumps(start_address, for_increment)

        self.duplicate_stack_top_item()     # dup index and sequence
        self.duplicate_stack_item(3)
        self.convert_builtin_method_call(Builtin.Len)
        self.convert_operation(BinaryOp.Lt)  # continue loop condition: index < len(sequence)

        self.convert_end_loop(start_address, test_address, True)

        return test_address

    def convert_end_loop(self, start_address: int, test_address: int, is_for: bool):
        """
        Converts the end of a loop statement

        :param start_address: the address of the while first opcode
        :param test_address: the address of the while test fist opcode
        :param is_for: whether the loop is a for loop or not
        """
        # updates the begin jmp with the target address
        self._update_jump(start_address, test_address)
        self._update_continue_jumps(start_address, test_address)

        # inserts end jmp
        while_begin: VMCode = VMCodeMapping.instance().code_map[start_address]
        while_body: int = VMCodeMapping.instance().get_end_address(while_begin) + 1
        end_jmp_to: int = while_body - VMCodeMapping.instance().bytecode_size
        self._insert_jump(OpcodeInfo.JMPIF, end_jmp_to)

        self._current_loop.pop()

        is_break_pos = self.bytecode_size
        self.convert_literal(False)  # is not break
        is_break_end = self.last_code_start_address
        self._update_break_jumps(start_address)

        if is_for:
            self._current_for.pop()
            reverse_to_drop_pos = self.last_code_start_address
            self.swap_reverse_stack_items(3)
            reverse_to_drop_end = self.last_code_start_address

            self.remove_stack_top_item()    # removes index and sequence from stack
            self.remove_stack_top_item()

            self._insert_loop_break_addresses(start_address, reverse_to_drop_pos, reverse_to_drop_end, self.bytecode_size)

        self._insert_loop_break_addresses(start_address, is_break_pos, is_break_end, self.bytecode_size)
        self._insert_jump(OpcodeInfo.JMPIF)

    def convert_end_loop_else(self, start_address: int, else_begin: int, has_else: bool = False, is_for: bool = False):
        """
        Updates the break loops jumps

        :param start_address: the address of the loop first opcode
        :param else_begin: the address of the else first opcode. Equals to code size if has_else is False
        :param has_else: whether this loop has an else branch
        :param is_for: whether the loop is a for loop or not
        """
        if start_address in self._jumps_to_loop_break:
            is_loop_insertions = []
            if start_address in self._inserted_loop_breaks:
                is_loop_insertions = self._inserted_loop_breaks.pop(start_address)
            is_loop_insertions.append(else_begin)

            if not has_else:
                self._opcodes_to_remove.extend(is_loop_insertions)
            else:
                min_break_addresses = 5 if is_for else 4
                if (start_address in self._jumps_to_loop_break
                        and len(self._jumps_to_loop_break[start_address]) < 2
                        and len(is_loop_insertions) < min_break_addresses):
                    # if len is less than 2, it means it has no breaks or the only break is else branch begin
                    # so it can remove the jump in the beginning of else branch
                    self._opcodes_to_remove.extend(is_loop_insertions)
                self._update_jump(else_begin, VMCodeMapping.instance().bytecode_size)

    def convert_begin_if(self) -> int:
        """
        Converts the beginning of the if statement

        :return: the address of the if first opcode
        """
        # it will be updated when the if ends
        self._insert_jump(OpcodeInfo.JMPIFNOT)
        return VMCodeMapping.instance().get_start_address(self.last_code)

    def convert_begin_else(self, start_address: int, insert_jump: bool = False) -> int:
        """
        Converts the beginning of the if else statement

        :param start_address: the address of the if first opcode
        :param insert_jump: whether should be included a jump to the end before the else branch
        :return: the address of the if else first opcode
        """
        # it will be updated when the if ends
        self._insert_jump(OpcodeInfo.JMP, insert_jump=insert_jump)

        # updates the begin jmp with the target address
        self._update_jump(start_address, VMCodeMapping.instance().bytecode_size)

        return self.last_code_start_address

    def convert_end_if(self, start_address: int):
        """
        Converts the end of the if statement

        :param start_address: the address of the if first opcode
        """
        # updates the begin jmp with the target address
        self._update_jump(start_address, VMCodeMapping.instance().bytecode_size)

    def convert_begin_try(self) -> int:
        """
        Converts the beginning of the try statement

        :return: the address of the try first opcode
        """
        # it will be updated when the while ends
        self.__insert_code(TryCode())

        return self.last_code_start_address

    def convert_try_except(self, exception_id: Optional[str]) -> int:
        """
        Converts the end of the try statement

        :param exception_id: the name identifier of the exception
        :type exception_id: str or None

        :return: the last address from try body
        """
        self._insert_jump(OpcodeInfo.JMP)
        last_try_code = self.last_code_start_address

        self._stack_append(Type.exception)  # when reaching the except body, an exception was raised
        if exception_id is None:
            self.remove_stack_top_item()

        return last_try_code

    def convert_end_try(self, start_address: int,
                        end_address: Optional[int] = None,
                        else_address: Optional[int] = None) -> int:
        """
        Converts the end of the try statement

        :param start_address: the address of the try first opcode
        :param end_address: the address of the try last opcode. If it is None, there's no except body.
        :param else_address: the address of the try else. If it is None, there's no else body.
        :return: the last address of the except body
        """
        self.__insert1(OpcodeInfo.ENDTRY)
        if end_address is not None:
            vmcode_mapping_instance = VMCodeMapping.instance()

            try_vm_code = vmcode_mapping_instance.get_code(start_address)
            try_jump = vmcode_mapping_instance.get_code(end_address)

            except_start_address = vmcode_mapping_instance.get_end_address(try_jump) + 1
            except_start_code = vmcode_mapping_instance.get_code(except_start_address)

            if isinstance(try_vm_code, TryCode):
                try_vm_code.set_except_code(except_start_code)
            self._update_jump(else_address if else_address is not None else end_address, self.last_code_start_address)

        return self.last_code_start_address

    def convert_end_try_finally(self, last_address: int, start_address: int, has_try_body: bool = False):
        """
        Converts the end of the try finally statement

        :param last_address: the address of the try except last opcode.
        :param start_address: the address of the try first opcode
        :param has_try_body: whether this try statement has a finally body.
        :return: the last address of the except body
        """
        if has_try_body:
            self.__insert1(OpcodeInfo.ENDFINALLY)
            vmcode_mapping_instance = VMCodeMapping.instance()

            try_vm_code = vmcode_mapping_instance.get_code(start_address)
            try_last_code = vmcode_mapping_instance.get_code(last_address)

            finally_start_address = vmcode_mapping_instance.get_end_address(try_last_code) + 1
            finally_start_code = vmcode_mapping_instance.get_code(finally_start_address)

            if isinstance(try_vm_code, TryCode):
                try_vm_code.set_finally_code(finally_start_code)
            self._update_jump(vmcode_mapping_instance.bytecode_size, self.last_code_start_address)

        self._update_jump(last_address, VMCodeMapping.instance().bytecode_size)

    def fix_negative_index(self, value_index: int = None):
        self._can_append_target = not self._can_append_target

        value_code = self.last_code_start_address
        size = VMCodeMapping.instance().bytecode_size

        self.duplicate_stack_top_item()
        self.__insert1(OpcodeInfo.SIGN)
        self.convert_literal(-1)

        jmp_address = VMCodeMapping.instance().bytecode_size
        self._insert_jump(OpcodeInfo.JMPNE)     # if index < 0

        state = self._stack_states.get_state(value_index) if isinstance(value_index, int) else self._stack
        # get position of collection relative to top
        index_of_last = -1
        for index, value in reversed(list(enumerate(state))):
            if isinstance(value, ICollectionType):
                index_of_last = index
                break

        if index_of_last >= 0:
            pos_from_top = len(state) - index_of_last
        else:
            pos_from_top = 2

        self.duplicate_stack_item(pos_from_top)     # index += len(array)
        self.convert_builtin_method_call(Builtin.Len)
        self.convert_operation(BinaryOp.Add)

        if not isinstance(value_index, int):
            value_index = VMCodeMapping.instance().bytecode_size
        jmp_target = value_index if value_index < size else VMCodeMapping.instance().bytecode_size
        self._update_jump(jmp_address, jmp_target)

        VMCodeMapping.instance().move_to_end(value_index, value_code)

        self._can_append_target = not self._can_append_target

    def fix_index_negative_stride(self):
        """
        If stride is negative, then the array was reversed, thus, lower and upper should be changed
        accordingly.
        The Opcodes below will only fix 1 index.
        array[lower:upper:-1] == reversed_array[len(array)-lower-1:len(array)-upper-1]
        If lower or upper was None, then it's not necessary to change its values.
        """
        # top array should be: len(array), index
        self.convert_builtin_method_call(Builtin.Len)
        self.swap_reverse_stack_items(2)
        self.convert_operation(BinaryOp.Sub)
        self.__insert1(OpcodeInfo.DEC)

    def convert_loop_continue(self):
        loop_start = self._current_loop[-1]
        self._insert_jump(OpcodeInfo.JMP)
        continue_address = self.last_code_start_address

        if loop_start not in self._jumps_to_loop_condition:
            self._jumps_to_loop_condition[loop_start] = [continue_address]
        else:
            self._jumps_to_loop_condition[loop_start].append(continue_address)

    def _update_continue_jumps(self, loop_start_address, loop_test_address):
        if loop_start_address in self._jumps_to_loop_condition:
            jump_addresses = self._jumps_to_loop_condition.pop(loop_start_address)
            for address in jump_addresses:
                self._update_jump(address, loop_test_address)

    def convert_loop_break(self):
        loop_start = self._current_loop[-1]
        is_break_pos = self.bytecode_size
        self.convert_literal(True)  # is break
        self._stack_pop()
        is_break_end = self.last_code_start_address
        self._insert_jump(OpcodeInfo.JMP)
        break_address = self.last_code_start_address

        self._insert_loop_break_addresses(loop_start, is_break_pos, is_break_end, break_address)

    def _insert_loop_break_addresses(self, loop_start: int, is_break_start: int, is_break_end: int, break_address: int):
        if loop_start not in self._jumps_to_loop_condition:
            self._jumps_to_loop_break[loop_start] = [break_address]
        elif break_address not in self._jumps_to_loop_break[loop_start]:
            self._jumps_to_loop_break[loop_start].append(break_address)

        is_break_instructions = VMCodeMapping.instance().get_addresses(is_break_start, is_break_end)

        if loop_start not in self._inserted_loop_breaks:
            self._inserted_loop_breaks[loop_start] = is_break_instructions
        else:
            loop_breaks_list = self._inserted_loop_breaks[loop_start]
            for address in is_break_instructions:
                # don't include duplicated addresses
                if address not in loop_breaks_list:
                    loop_breaks_list.append(address)

    def _update_break_jumps(self, loop_start_address) -> int:
        jump_target = VMCodeMapping.instance().bytecode_size

        if loop_start_address in self._jumps_to_loop_break:
            jump_addresses = self._jumps_to_loop_break.pop(loop_start_address)
            for address in jump_addresses:
                self._update_jump(address, jump_target)

    def convert_literal(self, value: Any) -> int:
        """
        Converts a literal value

        :param value: the value to be converted
        :return: the converted value's start address in the bytecode
        """
        start_address = VMCodeMapping.instance().bytecode_size
        if isinstance(value, bool):
            self.convert_bool_literal(value)
        elif isinstance(value, int):
            self.convert_integer_literal(value)
        elif isinstance(value, str):
            self.convert_string_literal(value)
        elif value is None:
            self.insert_none()
        elif isinstance(value, (bytes, bytearray)):
            self.convert_byte_array(value)
        elif isinstance(value, Sequence):
            self.convert_sequence_literal(value)
        elif isinstance(value, dict):
            self.convert_dict_literal(value)
        else:
            # it's not a type that is supported by neo-boa
            raise NotImplementedError
        return start_address

    def convert_integer_literal(self, value: int):
        """
        Converts an integer literal value

        :param value: the value to be converted
        """
        opcode = Opcode.get_literal_push(value)
        if opcode is not None:
            op_info: OpcodeInformation = OpcodeInfo.get_info(opcode)
            self.__insert1(op_info)
            self._stack_append(Type.int)
        else:
            opcode = Opcode.get_literal_push(-value)
            if opcode is not None:
                op_info: OpcodeInformation = OpcodeInfo.get_info(opcode)
                self.__insert1(op_info)
                self._stack_append(Type.int)
                self.convert_operation(UnaryOp.Negative)
            else:
                opcode, data = Opcode.get_push_and_data(value)
                op_info: OpcodeInformation = OpcodeInfo.get_info(opcode)
                self.__insert1(op_info, data)
                self._stack_append(Type.int)

    def convert_string_literal(self, value: str):
        """
        Converts an string literal value

        :param value: the value to be converted
        """
        array = bytes(value, constants.ENCODING)
        self.insert_push_data(array)
        self.convert_cast(Type.str)

    def convert_bool_literal(self, value: bool):
        """
        Converts an boolean literal value

        :param value: the value to be converted
        """
        if value:
            self.__insert1(OpcodeInfo.PUSH1)
        else:
            self.__insert1(OpcodeInfo.PUSH0)
        self._stack_append(Type.int)  # don't add bool to stack directly for optimizations
        self.convert_cast(Type.bool)

    def convert_sequence_literal(self, sequence: Sequence):
        """
        Converts a sequence value

        :param sequence: the value to be converted
        """
        if isinstance(sequence, tuple):
            value_type = Type.tuple.build(sequence)
        else:
            value_type = Type.list.build(list(sequence))

        for inner_value in reversed(sequence):
            self.convert_literal(inner_value)

        self.convert_new_array(len(sequence), value_type)

    def convert_dict_literal(self, dictionary: dict):
        """
        Converts a dict value

        :param dictionary: the value to be converted
        """
        value_type = Type.dict.build(dictionary)
        self.convert_new_map(value_type)

        for key, value in dictionary.items():
            self.duplicate_stack_top_item()
            self.convert_literal(key)
            value_start = self.convert_literal(value)
            self.convert_set_item(value_start)

    def convert_byte_array(self, array: bytes):
        """
        Converts a byte value

        :param array: the value to be converted
        """
        self.insert_push_data(array)
        self.convert_cast(Type.bytes)

    def insert_push_data(self, data: bytes):
        """
        Inserts a push data value

        :param data: the value to be converted
        """
        data_len: int = len(data)
        if data_len <= OpcodeInfo.PUSHDATA1.max_data_len:
            op_info = OpcodeInfo.PUSHDATA1
        elif data_len <= OpcodeInfo.PUSHDATA2.max_data_len:
            op_info = OpcodeInfo.PUSHDATA2
        else:
            op_info = OpcodeInfo.PUSHDATA4

        data = Integer(data_len).to_byte_array(min_length=op_info.data_len) + data
        self.__insert1(op_info, data)
        self._stack_append(Type.str)  # push data pushes a ByteString value in the stack

    def insert_none(self):
        """
        Converts None literal
        """
        self.__insert1(OpcodeInfo.PUSHNULL)
        self._stack_append(Type.none)

    def convert_cast(self, value_type: IType):
        """
        Converts casting types in Neo VM
        """
        stack_top_type: IType = self._stack[-1]
        if (not value_type.is_generic
                and not stack_top_type.is_generic
                and value_type.stack_item is not Type.any.stack_item):

            if value_type.stack_item != stack_top_type.stack_item:
                # converts only if the stack types are different
                self.__insert1(OpcodeInfo.CONVERT, value_type.stack_item)

            # but changes the value internally
            self._stack_pop()
            self._stack_append(value_type)

    def convert_new_map(self, map_type: IType):
        """
        Converts the creation of a new map

        :param map_type: the Neo Boa type of the map
        """
        self.__insert1(OpcodeInfo.NEWMAP)
        self._stack_append(map_type)

    def convert_new_empty_array(self, length: int, array_type: IType):
        """
        Converts the creation of a new empty array

        :param length: the size of the new array
        :param array_type: the Neo Boa type of the array
        """
        if length <= 0:
            self.__insert1(OpcodeInfo.NEWARRAY0)
        else:
            self.convert_literal(length)
            self._stack_pop()
            self.__insert1(OpcodeInfo.NEWARRAY)
        self._stack_append(array_type)

    def convert_new_array(self, length: int, array_type: IType = Type.list):
        """
        Converts the creation of a new array

        :param length: the size of the new array
        :param array_type: the Neo Boa type of the array
        """
        if length <= 0:
            self.convert_new_empty_array(length, array_type)
        else:
            self.convert_literal(length)
            self.__insert1(OpcodeInfo.PACK)
            self._stack_pop()  # array size
            for x in range(length):
                self._stack_pop()
            self._stack_append(array_type)

    def _set_array_item(self, value_start_address: int, check_for_negative_index: bool = True):
        """
        Converts the end of setting af a value in an array
        """
        index_type: IType = self._stack[-2]  # top: index
        if index_type is Type.int and check_for_negative_index:
            self.fix_negative_index(value_start_address)

    def convert_set_item(self, value_start_address: int, index_inserted_internally: bool = False):
        """
        Converts the end of setting af a value in an array
        """
        item_type: IType = self._stack[-3]  # top: index, 2nd-to-top: value, 3nd-to-top: array or map
        if item_type.stack_item is not StackItemType.Map:
            self._set_array_item(value_start_address, check_for_negative_index=not index_inserted_internally)

        self.__insert1(OpcodeInfo.SETITEM)
        self._stack_pop()  # value
        self._stack_pop()  # index
        self._stack_pop()  # array or map

    def _get_array_item(self, check_for_negative_index: bool = True):
        """
        Converts the end of get a value in an array
        """
        index_type: IType = self._stack[-1]  # top: index
        if index_type is Type.int and check_for_negative_index:
            self.fix_negative_index()

    def convert_get_item(self, index_inserted_internally: bool = False):
        array_or_map_type: IType = self._stack[-2]  # second-to-top: array or map
        if array_or_map_type.stack_item is not StackItemType.Map:
            self._get_array_item(check_for_negative_index=not index_inserted_internally)

        if array_or_map_type is Type.str:
            self.convert_literal(1)  # length of substring
            self.convert_get_substring()
        else:
            self.__insert1(OpcodeInfo.PICKITEM)
            self._stack_pop()

    def convert_get_substring(self):
        """
        Converts the end of get a substring
        """
        # if given substring size is negative, return empty string
        self.duplicate_stack_top_item()
        self.convert_literal(0)
        self.convert_operation(BinaryOp.GtE)

        self._insert_jump(OpcodeInfo.JMPIF)
        jmp_address = self.last_code_start_address
        self.remove_stack_top_item()
        self.convert_literal(0)

        self._stack_pop()  # length
        self._stack_pop()  # start
        original = self._stack_pop()  # original string

        self.__insert1(OpcodeInfo.SUBSTR)
        self._update_jump(jmp_address, self.last_code_start_address)
        self._stack_append(BufferType)  # substr returns a buffer instead of a bytestring
        self.convert_cast(original)

    def convert_get_array_slice(self, array: SequenceType):
        """
        Converts the end of get a substring
        """
        # if lower is still negative, then it should be 0
        self.duplicate_stack_item(2)
        self.__insert1(OpcodeInfo.SIGN)
        self.convert_literal(-1)
        jmp_address = VMCodeMapping.instance().bytecode_size
        self._insert_jump(OpcodeInfo.JMPNE)         # if lower < 0, then lower = 0

        self.swap_reverse_stack_items(2)
        self.remove_stack_top_item()
        self.convert_literal(0)
        self.swap_reverse_stack_items(2)
        jmp_target = VMCodeMapping.instance().bytecode_size
        self._update_jump(jmp_address, jmp_target)

        self.convert_new_empty_array(0, array)      # slice = []
        self.duplicate_stack_item(3)                # index = slice_start

        start_jump = self.convert_begin_while()  # while index < slice_end
        self.duplicate_stack_top_item()             # if index >= slice_start
        self.duplicate_stack_item(5)
        self.convert_operation(BinaryOp.GtE)
        is_valid_index = self.convert_begin_if()

        self.duplicate_stack_item(2)                    # slice.append(array[index])
        self.duplicate_stack_item(6)
        self.duplicate_stack_item(3)
        self.convert_get_item()
        self.convert_builtin_method_call(Builtin.SequenceAppend)
        self.convert_end_if(is_valid_index)

        self.__insert1(OpcodeInfo.INC)              # index += 1

        condition_address = VMCodeMapping.instance().bytecode_size
        self.duplicate_stack_top_item()         # end while index < slice_end
        self.duplicate_stack_item(4)
        self.convert_operation(BinaryOp.Lt)
        self.convert_end_while(start_jump, condition_address)

        self.convert_end_loop_else(start_jump, self.last_code_start_address, False)
        self.remove_stack_top_item()        # removes from the stack the arguments and the index
        self.swap_reverse_stack_items(4)    # doesn't use CLEAR opcode because this would delete
        self.remove_stack_top_item()        # data from external scopes
        self.remove_stack_top_item()
        self.remove_stack_top_item()

    def convert_get_sub_array(self, value_addresses: List[int] = None, negative_stride: bool = False):
        """
        Converts the end of get a slice in the beginning of an array

        :param value_addresses: the start and end values addresses
        :param negative_stride: whether stride is negative or not
        """
        # top: length, index, array
        if len(self._stack) > 2 and isinstance(self._stack[-3], SequenceType):
            if value_addresses is not None:
                # use the next value address to found where the opcodes to fix the value sign should be
                end_value_opcodes = value_addresses[1:]
                for code in reversed(end_value_opcodes):
                    self.fix_negative_index(code)
                self.fix_negative_index()  # fix the last value sign

                if negative_stride:
                    """
                    If stride is negative, then the array was reversed, thus, lower and upper should be changed 
                    accordingly.
                    array[lower:upper:-1] == reversed_array[len(array)-lower-1:len(array)-upper-1]
                    """
                    # calculates corresponding upper
                    # upper = len(array)-upper-1
                    self.duplicate_stack_item(3)
                    self.fix_index_negative_stride()

                    # puts lower at the top of the stack
                    self.swap_reverse_stack_items(2)

                    # calculates corresponding lower
                    # lower = len(array)-lower-1
                    self.duplicate_stack_item(3)
                    self.fix_index_negative_stride()

                    # reverts lower to its correct place
                    self.swap_reverse_stack_items(2)

            if self._stack[-3].stack_item in (StackItemType.ByteString,
                                              StackItemType.Buffer):

                # if lower is still negative, then it should be 0
                self.duplicate_stack_item(2)
                self.__insert1(OpcodeInfo.SIGN)
                self.convert_literal(-1)
                jmp_address = VMCodeMapping.instance().bytecode_size
                self._insert_jump(OpcodeInfo.JMPNE)     # if lower < 0, then lower = 0

                self.swap_reverse_stack_items(2)
                self.remove_stack_top_item()
                self.convert_literal(0)
                self.swap_reverse_stack_items(2)
                jmp_target = VMCodeMapping.instance().bytecode_size
                self._update_jump(jmp_address, jmp_target)

                # lower can not be greater than len(string)
                self.swap_reverse_stack_items(2)
                self.duplicate_stack_item(3)
                self.convert_builtin_method_call(Builtin.Len)
                self.__insert1(OpcodeInfo.MIN)  # the builtin MinMethod accepts more than 2 arguments, that's why this Opcode is being directly inserted
                self._stack_pop()
                # reverts lower to its correct place
                self.swap_reverse_stack_items(2)

                # upper can not be greater than len(string)
                self.duplicate_stack_item(3)
                self.convert_builtin_method_call(Builtin.Len)
                self.__insert1(OpcodeInfo.MIN)  # the builtin MinMethod accepts more than 2 arguments, that's why this Opcode is being directly inserted
                self._stack_pop()

                self.duplicate_stack_item(2)
                self.convert_operation(BinaryOp.Sub)
                self.convert_get_substring()
            else:
                array = self._stack[-3]
                self.duplicate_stack_item(3)
                self.convert_builtin_method_call(Builtin.Len)

                # if slice end is greater than the array size, fixes them
                self.__insert1(OpcodeInfo.MIN)  # the builtin MinMethod accepts more than 2 arguments, that's why this Opcode is being directly inserted
                self._stack_pop()
                self.convert_get_array_slice(array)

    def convert_get_array_beginning(self, negative_stride: bool = False):
        """
        Converts the end of get a slice in the beginning of an array

        :param negative_stride: whether stride is negative or not
        """
        if len(self._stack) > 1 and isinstance(self._stack[-2], SequenceType):
            self.fix_negative_index()

            if negative_stride:
                # calculates corresponding upper
                # upper = len(array)-upper-1
                self.duplicate_stack_item(2)
                self.fix_index_negative_stride()

            if self._stack[-2].stack_item in (StackItemType.ByteString,
                                              StackItemType.Buffer):
                # if upper is still negative, then it should be 0
                self.duplicate_stack_top_item()
                self.__insert1(OpcodeInfo.SIGN)
                self.convert_literal(-1)
                jmp_address = VMCodeMapping.instance().bytecode_size
                self._insert_jump(OpcodeInfo.JMPNE)     # if upper < 0, then upper = 0

                self.remove_stack_top_item()
                self.convert_literal(0)
                jmp_target = VMCodeMapping.instance().bytecode_size
                self._update_jump(jmp_address, jmp_target)

                # upper can not be greater than len(string)
                self.duplicate_stack_item(2)
                self.convert_builtin_method_call(Builtin.Len)
                self.__insert1(OpcodeInfo.MIN)  # the builtin MinMethod accepts more than 2 arguments, that's why this Opcode is being directly inserted
                self._stack_pop()

                self.__insert1(OpcodeInfo.LEFT)
                self._stack_pop()  # length
                original_type = self._stack_pop()  # original array
                self._stack_append(BufferType)  # left returns a buffer instead of a bytestring
                self.convert_cast(original_type)
            else:
                array = self._stack[-2]

                self.duplicate_stack_item(2)
                self.convert_builtin_method_call(Builtin.Len)

                # if slice end is greater than the array size, fixes them
                self.__insert1(OpcodeInfo.MIN)  # the builtin MinMethod accepts more than 2 arguments, that's why this Opcode is being directly inserted
                self._stack_pop()

                self.convert_literal(0)
                self.swap_reverse_stack_items(2)
                self.convert_get_array_slice(array)

    def convert_get_array_ending(self, negative_stride: bool = False):
        """
        Converts the end of get a slice in the ending of an array

        :param negative_stride: whether stride is negative or not
        """
        # top: start_slice, array_length, array
        if len(self._stack) > 2 and isinstance(self._stack[-3], SequenceType):
            self.fix_negative_index()

            if negative_stride:
                # calculates corresponding lower
                # lower = len(array)-lower-1
                self.duplicate_stack_item(3)
                self.fix_index_negative_stride()

            if self._stack[-3].stack_item in (StackItemType.ByteString,
                                              StackItemType.Buffer):
                # if lower is still negative, then it should be 0
                self.duplicate_stack_top_item()
                self.__insert1(OpcodeInfo.SIGN)
                self.convert_literal(-1)
                jmp_address = VMCodeMapping.instance().bytecode_size
                self._insert_jump(OpcodeInfo.JMPNE)     # if lower < 0, then lower = 0

                self.remove_stack_top_item()
                self.convert_literal(0)
                jmp_target = VMCodeMapping.instance().bytecode_size
                self._update_jump(jmp_address, jmp_target)

                # lower can not be greater than len(string)
                self.duplicate_stack_item(3)
                self.convert_builtin_method_call(Builtin.Len)
                self.__insert1(OpcodeInfo.MIN)  # the builtin MinMethod accepts more than 2 arguments, that's why this Opcode is being directly inserted
                self._stack_pop()

                self.convert_operation(BinaryOp.Sub)
                self.__insert1(OpcodeInfo.RIGHT)
                self._stack_pop()  # length
                original_type = self._stack_pop()  # original array
                self._stack_append(BufferType)     # right returns a buffer instead of a bytestring
                self.convert_cast(original_type)
            else:
                array = self._stack[-3]
                self.swap_reverse_stack_items(2)
                self.convert_get_array_slice(array)

    def convert_copy(self):
        if self._stack[-1].stack_item is StackItemType.Array:
            self.__insert1(OpcodeInfo.UNPACK)
            self.__insert1(OpcodeInfo.PACK)    # creates a new array with the values

    def convert_get_stride(self):
        if len(self._stack) > 1 and isinstance(self._stack[-2], SequenceType):
            if self._stack[-2].stack_item in (StackItemType.ByteString, StackItemType.Buffer):
                self.convert_get_substring_stride()
            else:
                self.convert_get_array_stride()

    def convert_array_negative_stride(self):
        """
        Converts an array to its reverse, to be able to scroll through the reversed list
        """
        # The logic on this function only do variable[::-z]

        original = self._stack[-1]
        self.convert_builtin_method_call(Builtin.Reversed)
        self.convert_cast(ListType())
        if isinstance(original, (StrType, BytesType)):        # if self was a string/bytes, then concat the values in the array
            self.duplicate_stack_top_item()
            self.convert_builtin_method_call(Builtin.Len)       # index = len(array) - 1
            self.convert_literal('')                            # string = ''

            start_jump = self.convert_begin_while()
            self.duplicate_stack_item(3)
            self.duplicate_stack_item(3)
            str_type = self._stack[-3]
            self.__insert1(OpcodeInfo.PICKITEM)
            self._stack_pop()
            self._stack_pop()
            self._stack_append(str_type)
            self.swap_reverse_stack_items(2)
            self.convert_operation(BinaryOp.Concat)             # string = string + array[index]

            condition_address = VMCodeMapping.instance().bytecode_size
            self.swap_reverse_stack_items(2)
            self.__insert1(OpcodeInfo.DEC)                      # index--
            self.swap_reverse_stack_items(2)
            self.duplicate_stack_item(2)
            self.convert_literal(0)
            self.convert_operation(BinaryOp.GtE)                # if index <= 0, stop loop
            self.convert_end_while(start_jump, condition_address)
            self.convert_end_loop_else(start_jump, self.last_code_start_address, False)

            # remove auxiliary values
            self.swap_reverse_stack_items(3)
            self.remove_stack_top_item()
            self.remove_stack_top_item()

    def convert_get_substring_stride(self):
        # initializing auxiliary variables
        self.duplicate_stack_item(2)
        self.convert_builtin_method_call(Builtin.Len)
        self.convert_literal(0)                         # index = 0
        self.convert_literal('')                        # substr = ''

        # logic verifying if substr[index] should be concatenated or not
        start_jump = self.convert_begin_while()
        self.duplicate_stack_item(2)
        self.duplicate_stack_item(5)
        self.convert_operation(BinaryOp.Mod)
        self.convert_literal(0)
        self.convert_operation(BinaryOp.NumEq)
        is_mod_0 = self.convert_begin_if()              # if index % stride == 0, then concatenate it

        # concatenating substr[index] with substr
        self.duplicate_stack_item(5)
        self.duplicate_stack_item(3)
        self.convert_literal(1)
        self._stack_pop()  # length
        self._stack_pop()  # start
        str_type = self._stack_pop()
        self.__insert1(OpcodeInfo.SUBSTR)
        self._stack_append(BufferType)                  # SUBSTR returns a buffer instead of a bytestring
        self.convert_cast(str_type)
        self.convert_operation(BinaryOp.Concat)         # substr = substr + string[index]
        self.convert_end_if(is_mod_0)

        # increment the index by 1
        self.swap_reverse_stack_items(2)
        self.__insert1(OpcodeInfo.INC)                  # index++
        self.swap_reverse_stack_items(2)

        # verifying if it should still be in the while
        condition_address = VMCodeMapping.instance().bytecode_size
        self.duplicate_stack_item(2)
        self.duplicate_stack_item(4)
        self.convert_operation(BinaryOp.Lt)             # stop the loop when index >= len(str)
        self.convert_end_while(start_jump, condition_address)
        self.convert_end_loop_else(start_jump, self.last_code_start_address, False)

        # removing auxiliary values
        self.swap_reverse_stack_items(5)
        self.remove_stack_top_item()
        self.remove_stack_top_item()
        self.remove_stack_top_item()
        self.remove_stack_top_item()

    def convert_get_array_stride(self):
        # initializing auxiliary variable
        self.duplicate_stack_item(2)
        self.convert_builtin_method_call(Builtin.Len)
        self.__insert1(OpcodeInfo.DEC)                      # index = len(array) - 1

        # logic verifying if array[index] should be removed or not
        start_jump = self.convert_begin_while()
        self.duplicate_stack_item(2)
        self.duplicate_stack_item(2)
        self.swap_reverse_stack_items(2)
        self.convert_operation(BinaryOp.Mod)
        self.convert_literal(0)
        self.convert_operation(BinaryOp.NumNotEq)
        is_not_mod_0 = self.convert_begin_if()              # if index % stride != 0, then remove it

        # removing element from array
        self.duplicate_stack_item(3)
        self.duplicate_stack_item(2)
        self.__insert1(OpcodeInfo.REMOVE)                   # array.pop(index)
        self._stack_pop()
        self._stack_pop()
        self.convert_end_if(is_not_mod_0)

        # decrement 1 from index
        self.__insert1(OpcodeInfo.DEC)

        # verifying if it should still be in the while
        condition_address = VMCodeMapping.instance().bytecode_size
        self.duplicate_stack_top_item()
        self.__insert1(OpcodeInfo.SIGN)
        self.convert_literal(-1)
        self.convert_operation(BinaryOp.NumNotEq)       # stop the loop when index < 0
        self.convert_end_while(start_jump, condition_address)
        self.convert_end_loop_else(start_jump, self.last_code_start_address, False)

        # removing auxiliary values
        self.remove_stack_top_item()                    # removed index from stack
        self.remove_stack_top_item()                    # removed stride from stack

    def convert_starred_variable(self):
        top_stack_item = self._stack[-1].stack_item
        if top_stack_item is StackItemType.Array:
            self.convert_copy()
        elif top_stack_item is StackItemType.Map:
            self.convert_builtin_method_call(Builtin.DictKeys)
        else:
            return

        self.convert_cast(Type.tuple)

    def convert_load_symbol(self, symbol_id: str, params_addresses: List[int] = None, is_internal: bool = False,
                            class_type: Optional[UserClass] = None):
        """
        Converts the load of a symbol

        :param symbol_id: the symbol identifier
        :param params_addresses: a list with each function arguments' first addresses
        """
        if class_type is None and len(self._stack) > 0 and isinstance(self._stack[-1], UserClass):
            class_type = self._stack[-1]

        another_symbol_id, symbol = self.get_symbol(symbol_id, is_internal=is_internal)

        if class_type is not None and symbol_id in class_type.symbols:
            symbol = class_type.symbols[symbol_id]

        if symbol is not Type.none:
            if isinstance(symbol, Property):
                symbol = symbol.getter
                params_addresses = []
            elif isinstance(symbol, ClassType) and params_addresses is not None:
                symbol = symbol.constructor_method()

            if not params_addresses:
                params_addresses = []

            if isinstance(symbol, Variable):
                symbol_id = another_symbol_id
                self.convert_load_variable(symbol_id, symbol, class_type)
            elif isinstance(symbol, IBuiltinMethod) and symbol.body is None:
                self.convert_builtin_method_call(symbol, params_addresses)
            elif isinstance(symbol, Event):
                self.convert_event_call(symbol)
            elif isinstance(symbol, Method):
                self.convert_method_call(symbol, len(params_addresses))
            elif isinstance(symbol, UserClass):
                self.convert_class_symbol(symbol, symbol_id)

    def convert_load_variable(self, var_id: str, var: Variable, class_type: Optional[UserClass] = None):
        """
        Converts the assignment of a variable

        :param var_id: the value to be converted
        :param var: the actual variable to be loaded
        """
        index, local, is_arg = self._get_variable_info(var_id)
        if index >= 0:
            opcode = Opcode.get_load(index, local, is_arg)
            op_info = OpcodeInfo.get_info(opcode)

            if op_info.data_len > 0:
                self.__insert1(op_info, Integer(index).to_byte_array())
            else:
                self.__insert1(op_info)
            self._stack_append(var.type)

        elif hasattr(var.type, 'get_value'):
            # the variable is a type constant
            # TODO: change this when implement class conversion
            value = var.type.get_value(var_id.split(constants.ATTRIBUTE_NAME_SEPARATOR)[-1])
            if value is not None:
                self.convert_literal(value)

        elif var_id in self._globals:
            another_var_id, var = self.get_symbol(var_id)
            storage_key = codegenerator.get_storage_key_for_variable(var)
            self._convert_builtin_storage_get_or_put(True, storage_key)

        elif class_type:
            if var_id in class_type.variables:
                index = list(class_type.variables).index(var_id)
                self.convert_literal(index)
                self.convert_get_item(index_inserted_internally=True)
                self._stack_pop()             # pop class type
                self._stack_append(var.type)  # push variable type

    def convert_store_variable(self, var_id: str, value_start_address: int = None, user_class: UserClass = None):
        """
        Converts the assignment of a variable

        :param var_id: the value to be converted
        """
        inner_index = None
        index, local, is_arg = self._get_variable_info(var_id)

        if user_class is None and len(self._stack) > 1 and isinstance(self._stack[-2], UserClass):
            user_class = self._stack[-2]

        if isinstance(user_class, UserClass) and var_id in user_class.variables:
            index, local, is_arg = self._get_variable_info(user_class.identifier)
            inner_index = list(user_class.variables).index(var_id)

        if isinstance(inner_index, int):
            # it's a variable from a class
            self.convert_literal(inner_index)
            index_address = self.bytecode_size

            if var_id in user_class.class_variables:
                # it's a class variable
                self.convert_load_variable(user_class.identifier, Variable(user_class))
                no_stack_items_to_swap = 3
            else:
                no_stack_items_to_swap = 2

            self.swap_reverse_stack_items(no_stack_items_to_swap)
            self.convert_set_item(index_address, index_inserted_internally=True)
            return

        if index >= 0:
            opcode = Opcode.get_store(index, local, is_arg)
            if opcode is not None:
                op_info = OpcodeInfo.get_info(opcode)

                if op_info.data_len > 0:
                    self.__insert1(op_info, Integer(index).to_byte_array())
                else:
                    self.__insert1(op_info)
                stored_type = self._stack_pop()

                from boa3.analyser.model.optimizer import UndefinedType
                if (var_id in self._current_scope.symbols or
                        (var_id in self._locals and self._current_method.locals[var_id].type is UndefinedType)):
                    another_symbol_id, symbol = self.get_symbol(var_id)
                    if isinstance(symbol, Variable):
                        var = symbol.copy()
                        var.set_type(stored_type)
                        self._current_scope.include_symbol(var_id, var)

        elif var_id in self._globals:
            another_var_id, var = self.get_symbol(var_id)
            storage_key = codegenerator.get_storage_key_for_variable(var)
            if value_start_address is None:
                value_start_address = self.bytecode_size
            self._convert_builtin_storage_get_or_put(False, storage_key, value_start_address)

    def _convert_builtin_storage_get_or_put(self, is_get: bool, storage_key: bytes, arg_address: int = None):
        addresses = [arg_address] if arg_address is not None else [self.bytecode_size]
        if not is_get:
            # must serialized before storing the value
            self.convert_builtin_method_call(Interop.Serialize, addresses)

        self.convert_literal(storage_key)
        self.convert_builtin_method_call(Interop.StorageGetContext)

        builtin_method = Interop.StorageGet if is_get else Interop.StoragePut
        self.convert_builtin_method_call(builtin_method)

        if is_get:
            # once the value is retrieved, it must be deserialized
            self.convert_builtin_method_call(Interop.Deserialize, addresses)

    def _get_variable_info(self, var_id: str) -> Tuple[int, bool, bool]:
        """
        Gets the necessary information about the variable to get the correct opcode

        :param var_id: the name id of the
        :return: returns the index of the variable in its scope and two boolean variables for representing the
        variable scope:
            `local` is True if it is a local variable and
            `is_arg` is True only if the variable is a parameter of the function.
        If the variable is not found, returns (-1, False, False)
        """
        is_arg: bool = False
        local: bool = False
        scope = None

        if var_id in self._args:
            is_arg: bool = True
            local: bool = True
            scope = self._args
        elif var_id in self._locals:
            is_arg = False
            local: bool = True
            scope = self._locals
        elif var_id in self._statics:
            scope = self._statics

        if scope is not None:
            index: int = scope.index(var_id) if var_id in scope else -1
        else:
            index = -1

        return index, local, is_arg

    def convert_builtin_method_call(self, function: IBuiltinMethod, args_address: List[int] = None):
        """
        Converts a builtin method function call

        :param function: the function to be converted
        :param args_address: a list with each function arguments' first addresses
        """
        if args_address is None:
            args_address = []
        store_opcode: OpcodeInformation = None
        store_data: bytes = b''

        if function.pack_arguments:
            self.convert_new_array(len(args_address))

        if function.stores_on_slot and 0 < len(function.args) <= len(args_address):
            address = args_address[-len(function.args)]
            load_instr = VMCodeMapping.instance().code_map[address]
            if load_instr.opcode.is_load_slot:
                store: Opcode = Opcode.get_store_from_load(load_instr.opcode)
                store_opcode = OpcodeInfo.get_info(store)
                store_data = load_instr.data

        fix_negatives = function.validate_negative_arguments()
        if len(fix_negatives) > 0:
            args_end_addresses = args_address[1:]
            args_end_addresses.append(self.bytecode_size)

            if function.push_self_first():
                addresses = args_end_addresses[:1] + list(reversed(args_end_addresses[1:]))
            else:
                addresses = list(reversed(args_end_addresses))

            for arg in sorted(fix_negatives, reverse=True):
                if len(addresses) > arg:
                    self.fix_negative_index(addresses[arg])

        for opcode, data in function.opcode:
            op_info = OpcodeInfo.get_info(opcode)
            if opcode is Opcode.CALL and isinstance(data, Method):
                # avoid losing current stack state
                for _ in data.args:
                    self._stack_append(Type.any)
                self.convert_method_call(data, len(data.args) - 1)
            else:
                self.__insert1(op_info, data)

        if store_opcode is not None:
            self._insert_jump(OpcodeInfo.JMP)
            jump = self.last_code_start_address
            self.__insert1(store_opcode, store_data)
            self._update_jump(jump, VMCodeMapping.instance().bytecode_size)

        for _ in range(function.args_on_stack):
            self._stack_pop()
        if function.return_type not in (None, Type.none):
            self._stack_append(function.return_type)

    def convert_method_call(self, function: Method, num_args: int):
        """
        Converts a method function call

        :param function: the function to be converted
        """
        if function.is_init:
            if num_args == len(function.args):
                self.remove_stack_top_item()
                num_args -= 1

            if num_args == len(function.args) - 1:
                # if this method is a constructor and only the self argument is missing
                function_result = function.type
                size = len(function_result.variables) if isinstance(function_result, UserClass) else 0
                if self.stack_size < 1 or not self._stack[-1].is_type_of(function_result):
                    self.convert_new_empty_array(size, function_result)

        if isinstance(function.origin_class, ContractInterfaceClass):
            if function.external_name is not None:
                function_id = function.external_name
            else:
                function_id = next((symbol_id
                                    for symbol_id, symbol in function.origin_class.symbols.items()
                                    if symbol is function),
                                   None)

            if isinstance(function_id, str):
                self.convert_new_array(len(function.args))
                self.convert_literal(Interop.CallFlagsType.default_value)
                self.convert_literal(function_id)
                self.convert_literal(function.origin_class.contract_hash.to_array())
                self.convert_builtin_method_call(Interop.CallContract)
                self._stack_pop()  # remove call contract 'any' result from the stack
        else:
            from boa3.neo.vm.CallCode import CallCode
            call_code = CallCode(function)
            self.__insert_code(call_code)
            self._update_codes_with_target(call_code)

        for arg in range(num_args):
            self._stack_pop()
        if function.is_init:
            self._stack_pop()  # pop duplicated result if it's init

        if function.return_type is not Type.none:
            self._stack_append(function.return_type)

    def convert_event_call(self, event: Event):
        """
        Converts an event call

        :param event_id: called event identifier
        :param event: called event
        """
        self.convert_new_array(len(event.args_to_generate), Type.list)
        if event.generate_name:
            self.convert_literal(event.name)
        else:
            self.swap_reverse_stack_items(2)

        from boa3.model.builtin.interop.interop import Interop
        for opcode, data in Interop.Notify.opcode:
            info = OpcodeInfo.get_info(opcode)
            self.__insert1(info, data)
            self._stack_pop()
            self._stack_pop()

    def convert_class_symbol(self, class_type: ClassType, symbol_id: str, load: bool = True) -> Optional[int]:
        """
        Converts an class symbol

        :param class_type:
        :param symbol_id:
        :param load:
        """
        method: Method

        if symbol_id in class_type.variables:
            return self.convert_class_variable(class_type, symbol_id, load)
        elif symbol_id in class_type.properties:
            symbol = class_type.properties[symbol_id]
            method = symbol.getter if load else symbol.setter
        elif symbol_id in class_type.instance_methods:
            method = class_type.instance_methods[symbol_id]
        elif symbol_id in class_type.class_methods:
            method = class_type.class_methods[symbol_id]
        elif isinstance(class_type, UserClass):
            return self.convert_user_class(class_type, symbol_id)
        else:
            return

        if isinstance(method, IBuiltinMethod):
            self.convert_builtin_method_call(method)
        else:
            self.convert_method_call(method, 0)
        return symbol_id

    def convert_user_class(self, class_type: UserClass, symbol_id: str) -> Optional[int]:
        """
        Converts an class symbol

        :param class_type:
        :param symbol_id:
        """
        start_address = self.bytecode_size

        if symbol_id in self._statics:
            self.convert_load_variable(symbol_id, Variable(class_type))
        else:
            # TODO: change to create an array with the class variables' default values when they are implemented
            self.convert_new_empty_array(len(class_type.class_variables), class_type)

        return start_address

    def convert_class_variable(self, class_type: ClassType, symbol_id: str, load: bool = True):
        """
        Converts an class variable

        :param class_type:
        :param symbol_id:
        :param load:
        """
        if symbol_id in class_type.variables:
            index = list(class_type.variables).index(symbol_id)

            if load:
                self.convert_literal(index)
                self.convert_get_item()

            return index

    def convert_operation(self, operation: IOperation):
        """
        Converts an operation

        :param operation: the operation that will be converted
        """
        for opcode, data in operation.opcode:
            op_info: OpcodeInformation = OpcodeInfo.get_info(opcode)
            self.__insert1(op_info, data)

        for op in range(operation.op_on_stack):
            self._stack_pop()
        self._stack_append(operation.result)

    def convert_assert(self):
        asserted_type = self._stack[-1] if len(self._stack) > 0 else Type.any

        if not isinstance(asserted_type, PrimitiveType):
            len_pos = VMCodeMapping.instance().bytecode_size
            # if the value is an array, a map or a struct, asserts it is not empty
            self.convert_builtin_method_call(Builtin.Len)
            len_code = VMCodeMapping.instance().code_map[len_pos]

            if asserted_type is Type.any:
                # need to check in runtime
                self.duplicate_stack_top_item()
                self.__insert1(OpcodeInfo.ISTYPE, StackItemType.Array)
                self._insert_jump(OpcodeInfo.JMPIF, len_code)

                self.duplicate_stack_top_item()
                self.__insert1(OpcodeInfo.ISTYPE, StackItemType.Map)
                self._insert_jump(OpcodeInfo.JMPIF, len_code)

                self.duplicate_stack_top_item()
                self.__insert1(OpcodeInfo.ISTYPE, StackItemType.Struct)
                self._insert_jump(OpcodeInfo.JMPIFNOT, 2)

                VMCodeMapping.instance().move_to_end(len_pos, len_pos)

        self.__insert1(OpcodeInfo.ASSERT)

    def convert_new_exception(self, exception_args_len: int = 0):
        if exception_args_len == 0 or len(self._stack) == 0:
            self.convert_literal(Builtin.Exception.default_message)

        if exception_args_len > 1:
            self.convert_new_array(exception_args_len)

        self._stack_pop()
        self._stack_append(Type.exception)

    def convert_raise_exception(self):
        if len(self._stack) == 0:
            self.convert_literal(Builtin.Exception.default_message)

        self._stack_pop()
        self.__insert1(OpcodeInfo.THROW)

    def __insert1(self, op_info: OpcodeInformation, data: bytes = None):
        """
        Inserts one opcode into the bytecode

        :param op_info: info of the opcode  that will be inserted
        :param data: data of the opcode, if needed
        """
        vm_code = VMCode(op_info, data)

        if op_info.opcode.has_target():
            data = vm_code.raw_data
            relative_address: int = Integer.from_bytes(data, signed=True)
            actual_address = VMCodeMapping.instance().bytecode_size + relative_address
            if (self._can_append_target
                    and relative_address != 0
                    and actual_address in VMCodeMapping.instance().code_map):
                vm_code.set_target(VMCodeMapping.instance().code_map[actual_address])
            else:
                self._include_missing_target(vm_code, actual_address)

        self.__insert_code(vm_code)
        self._update_codes_with_target(vm_code)

    def __insert_code(self, vm_code: VMCode):
        """
        Inserts one vmcode into the bytecode

        :param vm_code: the opcode that will be inserted
        """
        VMCodeMapping.instance().insert_code(vm_code)

    def _include_missing_target(self, vmcode: VMCode, target_address: int = 0):
        """
        Includes a instruction which parameter is another instruction that wasn't converted yet

        :param vmcode: instruction with incomplete parameter
        :param target_address: target instruction expected address
        :return:
        """
        if vmcode.opcode.has_target():
            if target_address == VMCodeMapping.instance().bytecode_size:
                target_address = None
            else:
                self._remove_missing_target(vmcode)

            if target_address not in self._missing_target:
                self._missing_target[target_address] = []
            if vmcode not in self._missing_target[target_address]:
                self._missing_target[target_address].append(vmcode)

    def _remove_missing_target(self, vmcode: VMCode):
        """
        Removes a instruction from the missing target list

        :param vmcode: instruction with incomplete parameter
        :return:
        """
        if vmcode.opcode.has_target():
            for target_address, opcodes in self._missing_target.copy().items():
                if vmcode in opcodes:
                    opcodes.remove(vmcode)
                    if len(opcodes) == 0:
                        self._missing_target.pop(target_address)
                    break

    def _update_codes_with_target(self, vm_code: VMCode):
        """
        Verifies if there are any instructions targeting the code. If it exists, updates each instruction found

        :param vm_code: targeted instruction
        """
        instance = VMCodeMapping.instance()
        vm_code_start_address = instance.get_start_address(vm_code)
        for target_address, codes in list(self._missing_target.items()):
            if target_address is not None and target_address <= vm_code_start_address:
                for code in codes:
                    code.set_target(vm_code)
                self._missing_target.pop(target_address)

    def set_code_targets(self):
        for target, vmcodes in self._missing_target.copy().items():
            if target is None:
                for code in vmcodes.copy():
                    relative_address: int = Integer.from_bytes(code.raw_data, signed=True)
                    code_address: int = VMCodeMapping.instance().get_start_address(code)
                    absolute_address = code_address + relative_address
                    code.set_target(VMCodeMapping.instance().get_code(absolute_address))

                    vmcodes.remove(code)
            else:
                for code in vmcodes.copy():
                    code.set_target(VMCodeMapping.instance().get_code(target))
                    vmcodes.remove(code)

            if len(vmcodes) == 0:
                self._missing_target.pop(target)

    def _insert_jump(self, op_info: OpcodeInformation, jump_to: Union[int, VMCode] = 0, insert_jump: bool = False):
        """
        Inserts a jump opcode into the bytecode

        :param op_info: info of the opcode  that will be inserted
        :param jump_to: data of the opcode
        :param insert_jump: whether should be included a jump to the end before the else branch
        """
        if isinstance(jump_to, VMCode):
            jump_to = VMCodeMapping.instance().get_start_address(jump_to) - VMCodeMapping.instance().bytecode_size

        if self.last_code.opcode is not Opcode.RET or insert_jump:
            data: bytes = self._get_jump_data(op_info, jump_to)
            self.__insert1(op_info, data)
        for x in range(op_info.stack_items):
            self._stack_pop()

    def _update_jump(self, jump_address: int, updated_jump_to: int):
        """
        Updates the data of a jump code in the bytecode

        :param jump_address: jump code start address
        :param updated_jump_to: new data of the code
        """
        vmcode: VMCode = VMCodeMapping.instance().get_code(jump_address)
        if vmcode is not None:
            if updated_jump_to in VMCodeMapping.instance().code_map:
                self._remove_missing_target(vmcode)
                target: VMCode = VMCodeMapping.instance().get_code(updated_jump_to)
                vmcode.set_target(target)
            else:
                data: bytes = self._get_jump_data(vmcode.info, updated_jump_to - jump_address)
                VMCodeMapping.instance().update_vm_code(vmcode, vmcode.info, data)
                if updated_jump_to not in VMCodeMapping.instance().code_map:
                    self._include_missing_target(vmcode, updated_jump_to)

    def _get_jump_data(self, op_info: OpcodeInformation, jump_to: int) -> bytes:
        return Integer(jump_to).to_byte_array(min_length=op_info.data_len, signed=True)

    def duplicate_stack_top_item(self):
        self.duplicate_stack_item(1)

    def duplicate_stack_item(self, pos: int = 0):
        """
        Duplicates the item n back in the stack

        :param pos: index of the variable
        """
        # n = 1 -> duplicates stack top item
        # n = 0 -> value varies in runtime
        if pos >= 0:
            opcode: Opcode = Opcode.get_dup(pos)
            if opcode is Opcode.PICK and pos > 0:
                self.convert_literal(pos - 1)
                self._stack_pop()
            op_info = OpcodeInfo.get_info(opcode)
            self.__insert1(op_info)
            self._stack_append(self._stack[-pos])

    def clear_stack(self, clear_if_in_loop: bool = False):
        if not clear_if_in_loop or len(self._current_for) > 0:
            self.__insert1(OpcodeInfo.CLEAR)

    def remove_stack_top_item(self):
        self.remove_stack_item(1)

    def remove_stack_item(self, pos: int = 0):
        """
        Removes the item n from the stack

        :param pos: index of the variable
        """
        # n = 1 -> removes stack top item
        if pos > 0:
            opcode: Opcode = Opcode.get_drop(pos)
            if opcode is Opcode.XDROP:
                self.convert_literal(pos - 1)
                self._stack_pop()
            op_info = OpcodeInfo.get_info(opcode)
            self.__insert1(op_info)
            if pos > 0 and len(self._stack) > 0:
                self._stack_pop(-pos)

    def swap_reverse_stack_items(self, no_items: int = 0):
        # n = 0 -> value varies in runtime
        if 0 <= no_items != 1:
            opcode: Opcode = Opcode.get_reverse(no_items)
            if opcode is Opcode.REVERSEN and no_items > 0:
                self.convert_literal(no_items)
            op_info = OpcodeInfo.get_info(opcode)
            self.__insert1(op_info)
            if opcode is Opcode.REVERSEN and no_items > 0:
                self._stack_pop()
            if no_items > 0:
                self._stack.reverse(-no_items)

    def convert_init_user_class(self, class_type: ClassType):
        # TODO: refactor when instance variables are implemented
        if isinstance(class_type, UserClass):
            # create an none-filled array with the size of the instance variables
            no_instance_variables = len(class_type.instance_variables)
            self.convert_new_empty_array(no_instance_variables, class_type)

            self.__insert1(OpcodeInfo.UNPACK)  # unpack for array concatenation
            value = self._stack_pop()
            self._stack_append(Type.int)
            self.remove_stack_top_item()

            # copy the array that stores the class variables from that class
            self.convert_user_class(class_type, class_type.identifier)

            self.__insert1(OpcodeInfo.UNPACK)  # unpack for array concatenation
            self._stack_append(value)
            self.convert_literal(no_instance_variables)
            self.convert_operation(BinaryOp.Add)

            self.__insert1(OpcodeInfo.PACK)  # packs everything together
            self._stack_pop()

    def generate_implicit_init_user_class(self, init_method: Method):
        if not init_method.is_called:
            return

        self.convert_begin_method(init_method)
        class_type = init_method.return_type
        for base in class_type.bases:
            base_constructor = base.constructor_method()
            num_args = len(base_constructor.args)

            for arg_id, arg_var in reversed(list(init_method.args.items())):
                self.convert_load_variable(arg_id, arg_var)

            args_to_call = num_args - 1 if num_args > 0 else num_args
            self.convert_method_call(base_constructor, args_to_call)
            self.remove_stack_top_item()

        self.convert_end_method()
