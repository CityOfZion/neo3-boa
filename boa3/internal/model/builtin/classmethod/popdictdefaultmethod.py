from typing import Dict, Optional

from boa3.internal.model.builtin.classmethod.popmethod import PopMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PopDictDefaultMethod(PopMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type

        if not Type.dict.is_type_of(arg_value):
            arg_value = Type.dict

        args: Dict[str, Variable] = {
            'self': Variable(arg_value),
            'key': Variable(arg_value.valid_key),
            'default': Variable(Type.any)
        }

        super().__init__(args, return_type=arg_value.value_type)

    def generate_opcodes(self, code_generator):
        from boa3.internal.model.type.type import Type

        # put the `default` value at the bottom of the stack
        code_generator.swap_reverse_stack_items(3)
        code_generator.swap_reverse_stack_items(2)
        code_generator.swap_reverse_stack_items(3)

        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.insert_opcode(Opcode.HASKEY, pop_from_stack=True, add_to_stack=[Type.bool])
        # if the key is in the dictionary:
        if_has_key = code_generator.convert_begin_if()
        #   return the dict[key] and remove pair from dict
        self.generate_internal_opcodes(code_generator)
        code_generator.remove_stack_item(2)

        # else the key is not in the dictionary:
        else_not_has_key = code_generator.convert_begin_else(if_has_key, is_internal=True)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        # return the default value
        code_generator.convert_end_if(else_not_has_key, is_internal=True)
