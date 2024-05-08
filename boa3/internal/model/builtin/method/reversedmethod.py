from collections.abc import Iterable
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ReversedMethod(IBuiltinMethod):
    def __init__(self, args_type: SequenceType = None):
        from boa3.internal.model.type.type import Type
        identifier = 'reversed'
        if not isinstance(args_type, SequenceType):
            args_type = Type.sequence

        args: dict[str, Variable] = {'sequence': Variable(args_type)}

        super().__init__(identifier, args, return_type=Type.reversed)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self.args['sequence'].type is Type.sequence:
            return self.raw_identifier
        return '-{0}_from_{1}'.format(self._identifier, self.args['sequence'].type.identifier)

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, Iterable) and len(value) > 0:
            value = value[0]

        if not isinstance(value, SequenceType):
            return ReversedMethod()

        if type(value) == type(self.args['sequence'].type):
            return self

        return ReversedMethod(value)

    @property
    def _body(self) -> str | None:
        return

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        # if isinstance(arg1, (str, bytes)):
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.ByteString)
        is_byte_str = code_generator.convert_begin_if()

        #     list_aux = []
        code_generator.convert_new_empty_array(length=0, array_type=self.return_type)
        #     limit = len(arg)
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        #     index = 0
        code_generator.convert_literal(0)

        #     while index < limit:
        while_index_is_valid = code_generator.convert_begin_while()
        #         list_aux.append(arg[index])
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.convert_cast(Type.int if Type.bytes.is_type_of(self.args['sequence'].type)
                                    else Type.str, is_internal=True)
        code_generator.convert_builtin_method_call(Builtin.SequenceAppend, is_internal=True)
        #         index += 1
        code_generator.insert_opcode(Opcode.INC)

        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(3)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)
        code_generator.convert_end_while(while_index_is_valid, while_condition, is_internal=True)

        for _ in range(3):
            code_generator.remove_stack_top_item()

        # else:
        else_is_bytes_str = code_generator.convert_begin_else(is_byte_str, is_internal=True)
        #     list_aux = arg.copy()
        code_generator.convert_copy()

        # list_aux.reverse()
        code_generator.convert_end_if(else_is_bytes_str, is_internal=True)

        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.REVERSEITEMS)
