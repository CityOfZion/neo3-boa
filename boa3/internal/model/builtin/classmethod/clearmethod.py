from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ClearMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        if not isinstance(sequence_type, MutableSequenceType):
            from boa3.internal.model.type.type import Type
            sequence_type = Type.mutableSequence

        identifier = 'clear'
        args: dict[str, Variable] = {'self': Variable(sequence_type)}
        super().__init__(identifier, args)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def stores_on_slot(self) -> bool:
        return True

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        return isinstance(params[0], IExpression) and isinstance(params[0].type, MutableSequenceType)

    def generate_opcodes(self, code_generator):
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.Buffer)
        if_is_bytes = code_generator.convert_begin_if()
        # if arg is bytes:

        code_generator.remove_stack_top_item()
        #   result = bytearray()
        code_generator.convert_literal(bytearray())

        else_is_bytes = code_generator.convert_begin_else(if_is_bytes, is_internal=True)
        # else:
        super().generate_opcodes(code_generator)
        #   arg.clear()

        code_generator.convert_end_if(else_is_bytes, is_internal=True)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.CLEARITEMS)

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
            return ClearMethod(value)
        return super().build(value)
