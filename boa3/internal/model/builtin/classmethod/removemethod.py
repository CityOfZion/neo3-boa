from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.variable import Variable


class RemoveMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        if not isinstance(sequence_type, MutableSequenceType):
            from boa3.internal.model.type.type import Type
            sequence_type = Type.mutableSequence

        self_arg = Variable(sequence_type)
        item_arg = Variable(sequence_type.value_type)

        identifier = 'remove'
        args: dict[str, Variable] = {'self': self_arg,
                                     '__value': item_arg}
        super().__init__(identifier, args)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 2:
            return False
        if not all(isinstance(param, IExpression) for param in params):
            return False

        from boa3.internal.model.type.itype import IType
        sequence_type: IType = params[0].type
        value_type: IType = params[1].type

        if not isinstance(sequence_type, MutableSequenceType):
            return False
        return sequence_type.value_type.is_type_of(value_type)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.neo.vm.opcode.Opcode import Opcode

        # index = 0
        # need to find the index to use REMOVE opcode
        code_generator.convert_literal(0)

        # while index < len(array):
        while_begin = code_generator.convert_begin_while()

        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)
        code_generator.duplicate_stack_item(3)
        #   if array[index] == value
        if_found = code_generator.convert_begin_if()
        code_generator.change_jump(if_found, Opcode.JMPNE)

        #       break
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_found)

        #   index += 1
        code_generator.insert_opcode(Opcode.INC)

        # while condition
        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)

        code_generator.convert_end_while(while_begin, while_condition, is_internal=True)

        # clean stack and remove item from collection
        code_generator.remove_stack_item(2)
        code_generator.insert_opcode(Opcode.REMOVE)

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, MutableSequenceType):
            return RemoveMethod(value)
        return super().build(value)
