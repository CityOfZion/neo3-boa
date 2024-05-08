from collections.abc import Sized
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class AppendMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        if not isinstance(sequence_type, MutableSequenceType):
            from boa3.internal.model.type.type import Type
            self_arg = Variable(Type.mutableSequence)
            item_arg = Variable(Type.any)
        else:
            self_arg = Variable(sequence_type)
            item_arg = Variable(sequence_type.value_type)

        identifier = 'append'
        args: dict[str, Variable] = {'self': self_arg, 'item': item_arg}
        super().__init__(identifier, args)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def stores_on_slot(self) -> bool:
        return True

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

    def generate_opcodes(self, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        code_generator.duplicate_stack_item(2)
        code_generator.insert_type_check(StackItemType.Buffer)  # append opcode only works for array
        # if self is bytes
        if_bytes = code_generator.convert_begin_if()
        #   result = self + arg     # when it's bytearray, concatenates the value
        code_generator.convert_operation(BinaryOp.Concat.build(Type.bytearray, Type.bytearray))

        # else:
        else_bytes = code_generator.convert_begin_else(if_bytes, is_internal=True)
        #   self.append()
        super().generate_opcodes(code_generator)

        code_generator.convert_end_if(else_bytes, is_internal=True)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.APPEND)

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, Sized) and len(value) > 0:
            value = value[0]
        if value == self.args['self'].type:
            return self
        if isinstance(value, MutableSequenceType):
            return AppendMethod(value)
        return super().build(value)
