from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ExtendMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        from boa3.internal.model.type.type import Type
        if not isinstance(sequence_type, MutableSequenceType):
            sequence_type = Type.mutableSequence

        self_arg = Variable(sequence_type)
        item_arg = Variable(Type.sequence.build_collection(sequence_type.value_type))

        identifier = 'extend'
        args: dict[str, Variable] = {'self': self_arg, 'item': item_arg}
        super().__init__(identifier, args)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def _arg_item(self) -> Variable:
        return self.args['item']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 2:
            return False
        if not all(isinstance(param, IExpression) for param in params):
            return False

        from boa3.internal.model.type.itype import IType
        sequence_type: IType = params[0].type
        iterator_type: IType = params[1].type

        if not isinstance(sequence_type, MutableSequenceType):
            return False
        if not isinstance(iterator_type, SequenceType):
            return False
        return sequence_type.value_type.is_type_of(iterator_type.value_type)

    @property
    def stores_on_slot(self) -> bool:
        return True

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        expected_values = self._arg_item.type

        code_generator.duplicate_stack_item(2)
        code_generator.insert_type_check(StackItemType.Buffer)  # append opcode only works for array
        # if self is bytes
        if_bytes = code_generator.convert_begin_if()
        #   result = self + arg     # when it's bytearray, concatenates the value
        code_generator.convert_operation(BinaryOp.Concat.build(Type.bytearray, Type.bytearray))

        # else:
        else_bytes = code_generator.convert_begin_else(if_bytes, is_internal=True)
        #   while len(item) > 0
        code_generator.insert_opcode(Opcode.UNPACK, add_to_stack=[expected_values, Type.int])

        begin_while = code_generator.convert_begin_while()
        #       push the array to the top of the stack
        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.INC)
        code_generator.duplicate_stack_item(expected_stack_item=expected_values)

        #       get the first value that wasn't appended yet
        code_generator.move_stack_item_to_top(3)

        #       self.append(item)
        code_generator.convert_builtin_method_call(Builtin.SequenceAppend, is_internal=True)

        #       update stack control
        code_generator.insert_opcode(Opcode.DEC)

        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        #   while there are items to add

        code_generator.convert_end_while(begin_while, while_condition, is_internal=True)
        #   clear stack
        for _ in self.args:
            code_generator.remove_stack_top_item()

        code_generator.convert_end_if(else_bytes, is_internal=True)

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
            return ExtendMethod(value)
        return super().build(value)
