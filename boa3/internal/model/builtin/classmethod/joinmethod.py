from collections.abc import Iterable
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.collection.mapping.mutable.dicttype import DictType
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class JoinMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None, iterable_type: SequenceType | DictType = None):
        from boa3.internal.model.type.type import Type

        if not isinstance(self_type, IByteStringType):
            self_type = Type.bytes

        if not isinstance(iterable_type, (SequenceType, DictType)):
            iterable_type = Type.sequence.build_collection([self_type])

        identifier = 'join'
        args: dict[str, Variable] = {
            'self': Variable(self_type),
            'iterable': Variable(iterable_type),
        }

        super().__init__(identifier, args, return_type=self_type)

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type

        if Type.dict.is_type_of(self._arg_iterable.type):
            return '-{0}_{1}'.format(self._identifier, Type.dict.identifier)

        return self._identifier  # JoinMethod default value for self

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def _arg_iterable(self) -> Variable:
        return self.args['iterable']

    def push_self_first(self) -> bool:
        return self.has_self_argument

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        code_generator.duplicate_stack_top_item()
        # iterable_size = len(iterable)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        # index = 0
        code_generator.convert_literal(0)
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)

        # if iterable_size >= 0:
        if_iterable_not_empty = code_generator.convert_begin_if()
        code_generator.change_jump(if_iterable_not_empty, Opcode.JMPLE)

        from boa3.internal.model.type.type import Type
        if Type.dict.is_type_of(self._arg_iterable.type):
            code_generator.swap_reverse_stack_items(3)
            code_generator.convert_builtin_method_call(Builtin.DictKeys)
            code_generator.swap_reverse_stack_items(3)

        #   joined = iterable[0]
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)
        code_generator.swap_reverse_stack_items(2)
        #   index += 1
        code_generator.insert_opcode(Opcode.INC)
        code_generator.swap_reverse_stack_items(2)

        #   while index < iterable_size:
        while_start = code_generator.convert_begin_while()

        code_generator.duplicate_stack_item(5)
        #       joined = joined + string
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_get_item(index_inserted_internally=True)
        #       joined = joined + iterable[index]
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.swap_reverse_stack_items(2)
        #       index += 1
        code_generator.insert_opcode(Opcode.INC)
        code_generator.swap_reverse_stack_items(2)

        # # while condition and end
        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_operation(BinaryOp.Lt)
        code_generator.convert_end_while(while_start, while_condition, is_internal=True)

        #   return joined
        code_generator.convert_cast(Type.str, is_internal=True)

        # elif iterable_size < 0:
        else_iterable_is_empty = code_generator.convert_begin_else(if_iterable_not_empty, is_internal=True)
        #   return ""
        code_generator.convert_literal("")
        code_generator.convert_end_if(else_iterable_is_empty)

        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, Iterable):
            value = [value]
        if isinstance(value, list) and len(value) <= 2:
            self_type = self._arg_self.type
            if len(value) < 2:
                value.append(None)
            if isinstance(value[0], type(self_type)) and isinstance(value[1], SequenceType):
                return self
            else:
                return JoinMethod(value[0], value[1])

        return super().build(value)
