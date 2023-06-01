from typing import Dict

from boa3.internal.model.builtin.method.strmethod import StrMethod
from boa3.internal.model.variable import Variable


class StrBoolMethod(StrMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        args: Dict[str, Variable] = {
            'object': Variable(Type.bool),
        }

        super().__init__(args)

    def generate_internal_opcodes(self, code_generator):
        # if object == True:
        if_address = code_generator.convert_begin_if()
        #   result = 'True'
        code_generator.convert_literal(str(True))

        # else:
        if_address = code_generator.convert_begin_else(if_address, is_internal=True)
        #   result = 'False'
        code_generator.convert_literal(str(False))

        code_generator.convert_end_if(if_address, is_internal=True)
