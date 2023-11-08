from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from boa3.internal.compiler.codegenerator import get_bytes_count
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType


class ClassType(IType, ABC):
    """
    An abstract class used to represent Python class
    """

    def __init__(self, identifier: str, decorators: list = None,
                 bases: List[ClassType] = None):
        super().__init__(identifier)

        if decorators is None:
            decorators = []
        else:
            # avoid circular import
            from boa3.internal.model.decorator import IDecorator
            decorators = [decorator for decorator in decorators
                          if isinstance(decorator, IDecorator)]

        self.decorators = decorators

        if not isinstance(bases, list):
            bases = []
        self.bases: List[ClassType] = bases

    @property
    @abstractmethod
    def class_variables(self):
        """
        :rtype: Dict[str, boa3.internal.model.variable.Variable]
        """
        class_vars = {}
        for base in self.bases:
            class_vars.update(base.class_variables)
        return class_vars

    @property
    @abstractmethod
    def instance_variables(self):
        """
        :rtype: Dict[str, boa3.internal.model.variable.Variable]
        """
        instance_vars = {}
        for base in self.bases:
            instance_vars.update(base.instance_variables)
        return instance_vars

    @property
    def variables(self):
        """
        :rtype: Dict[str, boa3.internal.model.variable.Variable]
        """
        variables = self.class_variables.copy()
        variables.update(self.instance_variables)
        return variables

    @property
    def _all_variables(self):
        """
        :rtype: Dict[str, boa3.internal.model.variable.Variable]
        """
        return self.variables

    @property
    @abstractmethod
    def properties(self):
        """
        :rtype: Dict[str, boa3.internal.model.property.Property]
        """
        props = {}
        for base in self.bases:
            props.update(base.properties)
        return props

    @property
    @abstractmethod
    def static_methods(self):
        """
        :rtype: Dict[str, boa3.internal.model.method.Method]
        """
        static_funcs = {}
        for base in self.bases:
            static_funcs.update(base.static_methods)
        return static_funcs

    @property
    @abstractmethod
    def class_methods(self):
        """
        :rtype: Dict[str, boa3.internal.model.method.Method]
        """
        class_funcs = {}
        for base in self.bases:
            class_funcs.update(base.class_methods)
        return class_funcs

    @property
    @abstractmethod
    def instance_methods(self):
        """
        :rtype: Dict[str, boa3.internal.model.method.Method]
        """
        instance_funcs = {}
        for base in self.bases:
            instance_funcs.update(base.instance_methods)
        return instance_funcs

    @property
    def methods(self):
        """
        :rtype: Dict[str, boa3.internal.model.method.Method]
        """
        methods = self.static_methods.copy()
        methods.update(self.class_methods)
        methods.update(self.instance_methods)
        return methods

    @abstractmethod
    def constructor_method(self):
        """
        If the class constructor is None, it mustn't allow instantiation of this class

        :rtype: boa3.internal.model.method.Method or None
        """
        pass

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        s = {}
        s.update(self.methods)
        s.update(self.variables)
        s.update(self.properties)
        return s

    @property
    def class_symbols(self) -> Dict[str, ISymbol]:
        s: Dict[str, ISymbol] = {}
        s.update(self.class_methods)  # class methods and variables can be accessed both
        s.update(self.class_variables)  # from class name or instance object
        s.update(self.static_methods)
        return s

    @property
    def instance_symbols(self) -> Dict[str, ISymbol]:
        s: Dict[str, ISymbol] = {}
        s.update(self.class_methods)  # class methods and variables can be accessed both
        s.update(self.class_variables)  # from class name or instance object
        s.update(self.instance_methods)
        s.update(self.instance_variables)
        s.update(self.properties)
        return s

    @property
    @abstractmethod
    def abi_type(self) -> AbiType:
        # must be overwritten, classes cannot be mapped to Any
        return super().abi_type

    @property
    @abstractmethod
    def stack_item(self) -> StackItemType:
        # must be overwritten, classes cannot be mapped to Any
        return super().stack_item

    @property
    def is_interface(self) -> bool:
        from boa3.internal.model.builtin.decorator import ContractDecorator
        return any(isinstance(decorator, ContractDecorator) for decorator in self.decorators)

    def generate_is_instance_type_check(self, code_generator):
        start_address = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()

        begin_generic_type = code_generator.bytecode_size
        super().generate_is_instance_type_check(code_generator)
        generic_type_check_size = code_generator.bytecode_size - begin_generic_type

        # if type check is ok
        begin_if = code_generator.convert_begin_if()
        #   result = specific check
        first_if_code = code_generator.bytecode_size
        inner_jumps = self._generate_specific_class_type_check(code_generator)

        if first_if_code == code_generator.bytecode_size:
            code_generator.convert_end_if(begin_if, is_internal=True)

            from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
            map_instance = VMCodeMapping.instance()
            map_instance.move_to_end(start_address, begin_generic_type - 1)
            map_instance.remove_opcodes(start_address + generic_type_check_size)
            return

        # else
        begin_else = code_generator.convert_begin_else(begin_if, insert_jump=True)
        for validation in inner_jumps:
            code_generator.convert_end_if(validation, is_internal=True)

        #   result = False
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(False)
        code_generator.convert_end_if(begin_else, is_internal=True)

    def _generate_specific_class_type_check(self, code_generator) -> List[int]:
        """
        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator

        :return: list of inner jumps addresses for failed checks
        :rtype: list[int]
        """
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        if self.stack_item not in (StackItemType.Array, StackItemType.Struct, StackItemType.Map):
            return []

        # check variable count
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(len(self._all_variables))
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        # if len(arg) == len(self):
        begin_if = code_generator.convert_begin_if()

        last_index = len(self._all_variables) - 1
        inner_validations = []
        if len(self._all_variables) > 0:
            for var_index, (var_id, var) in list(enumerate(self._all_variables.items())):
                if var.type.stack_item != StackItemType.Any:
                    code_generator.duplicate_stack_top_item()
                    # validate primitive types only to avoid recursive code
                    if self.stack_item == StackItemType.Map:
                        code_generator.convert_literal(var_id)
                    else:
                        code_generator.convert_literal(var_index)
                    code_generator.convert_get_item(index_inserted_internally=True, test_is_negative_index=False)
                    code_generator.insert_type_check(var.type.stack_item)

                    if var_index < last_index:
                        inner_validations.append(code_generator.convert_begin_if())

            code_generator.remove_stack_item(2)

        inner_validations.insert(0, begin_if)
        return inner_validations

    def is_instance_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        is_type_opcodes = [
            (Opcode.DUP, b''),  # if is the same internal type
            (Opcode.ISTYPE, self.stack_item)
        ]

        return_false = [
            (Opcode.DROP, b''),
            (Opcode.PUSH0, b''),  # return False
        ]
        return_false_bytes_size = get_bytes_count(return_false)

        final_instructions = []
        final_jmp = [(Opcode.JMP, Integer(2 + return_false_bytes_size).to_byte_array(min_length=1))]
        validate_type = self._is_instance_inner_opcodes(get_bytes_count(final_jmp))
        if len(validate_type) > 0:
            final_instructions += (validate_type + final_jmp)

            bytes_size = get_bytes_count(final_instructions)
            jmp_opcode, jmp_arg = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, bytes_size + 1)

            final_instructions = (is_type_opcodes +
                                  [(jmp_opcode, jmp_arg)] +
                                  final_instructions +
                                  return_false)
        else:
            is_type_opcodes.remove((Opcode.DUP, b''))
            final_instructions = is_type_opcodes

        return final_instructions

    def _is_instance_inner_opcodes(self, jmp_to_if_false: int = 0) -> List[Tuple[Opcode, bytes]]:
        if self.stack_item not in (StackItemType.Array, StackItemType.Struct, StackItemType.Map):
            return []

        variables_count_is_equal = [
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            OpcodeHelper.get_push_and_data(len(self._all_variables)),
            (Opcode.NUMEQUAL, b''),
        ]

        total_size = jmp_to_if_false
        variables_type_validations = []

        for var_index, (var_id, var) in reversed(list(enumerate(self._all_variables.items()))):

            if var.type.stack_item != StackItemType.Any:

                # validate primitive types only to avoid recursive code
                if self.stack_item == StackItemType.Map:
                    get = OpcodeHelper.get_pushdata_and_data(var_id)
                else:
                    get = OpcodeHelper.get_push_and_data(var_index)

                new_opcodes = [
                    (Opcode.DUP, b''),
                    get,
                    (Opcode.PICKITEM, b''),
                    (Opcode.ISTYPE, var.type.stack_item)
                ]
                if len(variables_type_validations) == 0:
                    new_opcodes.append((Opcode.NIP, b''))
                elif total_size > 0:
                    new_opcodes.append((OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, total_size + 1)))

                variables_type_validations = new_opcodes + variables_type_validations
                total_size += get_bytes_count(new_opcodes)

        if total_size > 0:
            if len(variables_type_validations) > 0:
                final_opcode = (OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, total_size + 1))
            else:
                final_opcode = (Opcode.NIP, b'')
            variables_count_is_equal.append(final_opcode)

        return variables_count_is_equal + variables_type_validations
