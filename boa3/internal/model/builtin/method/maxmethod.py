from typing import Any, Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.collection.sequence.tupletype import TupleType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class MaxMethod(IBuiltinMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type
        identifier = 'max'

        self._allowed_types = [Type.int, Type.str, Type.bytes]
        default_type = Type.int
        if not self._is_valid_type(arg_value):
            arg_value = default_type

        args: Dict[str, Variable] = {
            'args1': Variable(arg_value),
            'args2': Variable(arg_value)
        }
        vararg = ('values', Variable(arg_value))
        super().__init__(identifier, args, return_type=arg_value, vararg=vararg)

    def _is_valid_type(self, arg_type: Optional[IType]) -> bool:
        return (isinstance(arg_type, IType) and
                any(allowed_type.is_type_of(arg_type) for allowed_type in self._allowed_types))

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self._arg_values.type is Type.int:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._arg_values.type._identifier)

    @property
    def _arg_values(self) -> Variable:
        return self._vararg[1]

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, SequenceType)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.MAX)

    def generate_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.type.type import Type

        # if len(stack) == 2:
        code_generator.insert_opcode(Opcode.DEPTH, add_to_stack=[Type.int])
        code_generator.convert_literal(2)
        if_stack_size_equals_2 = code_generator.convert_begin_if()
        code_generator.change_jump(if_stack_size_equals_2, Opcode.JMPNE)

        #   aux_list = [arg1, arg2]
        code_generator.convert_literal(2)

        # else:
        else_stack_size_equals_3 = code_generator.convert_begin_else(if_stack_size_equals_2, is_internal=True)
        #   aux_list = [arg1, arg2, *values]
        code_generator.swap_reverse_stack_items(3)
        code_generator.insert_opcode(Opcode.UNPACK)
        code_generator.insert_opcode(Opcode.INC)
        code_generator.insert_opcode(Opcode.INC)
        code_generator.convert_end_if(else_stack_size_equals_3, is_internal=True)
        code_generator.insert_opcode(Opcode.PACK)

        # index = len(aux_list) - 1
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        # current_max = aux_list[index]
        code_generator.convert_get_item(index_inserted_internally=True, test_is_negative_index=False)

        # while (index != 0):
        start_while = code_generator.convert_begin_while()

        #   index -= 1
        code_generator.swap_reverse_stack_items(2)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_get_item(index_inserted_internally=True, test_is_negative_index=False)

        #   current_max = max(current_max, aux_list[index])
        self._compare_values(code_generator)

        # while condition and end
        condition_address = code_generator.bytecode_size
        code_generator.duplicate_stack_item(2)
        code_generator.insert_opcode(Opcode.SIGN)
        code_generator.convert_end_while(start_while, condition_address, is_internal=True)

        # return max
        code_generator.swap_reverse_stack_items(3)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

    def _compare_values(self, code_generator):
        """
        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator
        """
        self.generate_internal_opcodes(code_generator)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and len(value) > 0:
            value = value[0]
        if isinstance(value, TupleType):
            value = value.value_type
        if type(value) == type(self._arg_values.type):
            return self

        from boa3.internal.model.builtin.method.maxbytestringmethod import MaxByteStringMethod
        from boa3.internal.model.builtin.method.maxintmethod import MaxIntMethod
        from boa3.internal.model.type.type import Type

        if Type.str.is_type_of(value) or Type.bytes.is_type_of(value):
            return MaxByteStringMethod(value)

        return MaxIntMethod(value)
