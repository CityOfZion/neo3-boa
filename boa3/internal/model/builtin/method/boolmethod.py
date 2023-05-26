from typing import Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class BoolMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'bool'

        args: Dict[str, Variable] = {
            'value': Variable(Type.any),
        }
        super().__init__(identifier, args, return_type=Type.bool)

    @property
    def _value(self) -> Variable:
        return self.args['value']

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        # if arg is None
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(None)
        is_null = code_generator.convert_begin_if()
        #   return False
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(False)

        else_is_null = code_generator.convert_begin_else(is_null, is_internal=True)
        # if arg is not int
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.Array)
        if_is_sequence = code_generator.convert_begin_if()
        code_generator.change_jump(if_is_sequence, Opcode.JMPIF)

        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.Map)
        if_is_map = code_generator.convert_begin_if()
        code_generator.change_jump(if_is_map, Opcode.JMPIF)

        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.Struct)
        if_is_struct = code_generator.convert_begin_if()

        code_generator.convert_end_if(if_is_sequence, is_internal=True)
        code_generator.convert_end_if(if_is_map, is_internal=True)
        #   return len(arg) == 0
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        code_generator.convert_end_if(if_is_struct, is_internal=True)
        # else
        #   return arg == 0
        code_generator.convert_end_if(else_is_null, is_internal=True)

        code_generator.insert_opcode(Opcode.NZ)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
